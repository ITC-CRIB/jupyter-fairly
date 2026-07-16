"""Tests for the jupyter-fairly server endpoints.

Endpoints that only touch the local filesystem (`newdataset`) are tested
against the real fairly package. Endpoints that would reach a remote data
repository (`clone`, `upload`, `push`, `datasets`, `repo-token`) are tested
with the fairly entry points monkeypatched, so the suite runs offline and
without repository credentials.
"""

import json
from types import SimpleNamespace

import pytest
from tornado.httpclient import HTTPClientError

import jupyter_fairly.handlers as handlers


async def test_example(jp_fetch):
    response = await jp_fetch("jupyter-fairly", "example")

    assert response.code == 200
    payload = json.loads(response.body)
    assert "Jupyter Server is Online" in payload["message"]


# --- newdataset -------------------------------------------------------------

async def test_newdataset_creates_manifest(jp_fetch, tmp_path):
    response = await jp_fetch(
        "jupyter-fairly", "newdataset",
        method="POST",
        body=json.dumps({"path": str(tmp_path), "template": "default"}),
    )

    assert response.code == 200
    assert (tmp_path / "manifest.yaml").exists()


async def test_newdataset_twice_fails(jp_fetch, tmp_path):
    body = json.dumps({"path": str(tmp_path), "template": "default"})
    await jp_fetch("jupyter-fairly", "newdataset", method="POST", body=body)

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch("jupyter-fairly", "newdataset", method="POST", body=body)
    assert excinfo.value.code == 403


async def test_newdataset_missing_field(jp_fetch, tmp_path):
    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "newdataset",
            method="POST",
            body=json.dumps({"path": str(tmp_path)}),  # no "template"
        )
    assert excinfo.value.code == 400


# --- clone ------------------------------------------------------------------

async def test_clone_success(jp_fetch, tmp_path, monkeypatch):
    stored = {}

    class FakeDataset:
        def store(self, path, extract):
            stored["path"] = path
            stored["extract"] = extract

    monkeypatch.setattr(handlers.fairly, "dataset", lambda source: FakeDataset())

    response = await jp_fetch(
        "jupyter-fairly", "clone",
        method="POST",
        body=json.dumps({
            "source": "10.4121/12345",
            "destination": str(tmp_path),
            "extract": False,
        }),
    )

    assert response.code == 200
    assert stored == {"path": str(tmp_path), "extract": False}


async def test_clone_unknown_source(jp_fetch, tmp_path, monkeypatch):
    def raise_value_error(source):
        raise ValueError(f"unknown identifier: {source}")

    monkeypatch.setattr(handlers.fairly, "dataset", raise_value_error)

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "clone",
            method="POST",
            body=json.dumps({
                "source": "not-a-doi",
                "destination": str(tmp_path),
                "extract": False,
            }),
        )
    assert excinfo.value.code == 400


# --- upload -----------------------------------------------------------------

async def test_upload_success(jp_fetch, tmp_path, monkeypatch):
    uploaded = {}

    class FakeLocalDataset:
        def upload(self, client):
            uploaded["client"] = client

    fake_client = object()
    monkeypatch.setattr(handlers.fairly, "client", lambda id: fake_client)
    monkeypatch.setattr(handlers.fairly, "dataset", lambda id: FakeLocalDataset())

    response = await jp_fetch(
        "jupyter-fairly", "upload",
        method="POST",
        body=json.dumps({"directory": str(tmp_path), "client": "zenodo"}),
    )

    assert response.code == 200
    assert uploaded["client"] is fake_client


async def test_upload_invalid_client(jp_fetch, tmp_path, monkeypatch):
    def raise_value_error(id):
        raise ValueError(f"invalid client: {id}")

    monkeypatch.setattr(handlers.fairly, "client", raise_value_error)

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "upload",
            method="POST",
            body=json.dumps({"directory": str(tmp_path), "client": "nope"}),
        )
    assert excinfo.value.code == 400


async def test_upload_failure(jp_fetch, tmp_path, monkeypatch):
    class FakeLocalDataset:
        def upload(self, client):
            raise ValueError("upload went wrong")

    monkeypatch.setattr(handlers.fairly, "client", lambda id: object())
    monkeypatch.setattr(handlers.fairly, "dataset", lambda id: FakeLocalDataset())

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "upload",
            method="POST",
            body=json.dumps({"directory": str(tmp_path), "client": "zenodo"}),
        )
    assert excinfo.value.code == 500


# --- push -------------------------------------------------------------------

async def test_push_success(jp_fetch, tmp_path, monkeypatch):
    pushed = {"called": False}

    class FakeLocalDataset:
        def push(self):
            pushed["called"] = True

    monkeypatch.setattr(handlers.fairly, "dataset", lambda id: FakeLocalDataset())

    response = await jp_fetch(
        "jupyter-fairly", "push",
        method="PATCH",
        body=json.dumps({"localdataset": str(tmp_path)}),
    )

    assert response.code == 200
    assert pushed["called"]


async def test_push_missing_manifest(jp_fetch, tmp_path, monkeypatch):
    def raise_not_found(id):
        raise FileNotFoundError("manifest.yaml")

    monkeypatch.setattr(handlers.fairly, "dataset", raise_not_found)

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "push",
            method="PATCH",
            body=json.dumps({"localdataset": str(tmp_path)}),
        )
    assert excinfo.value.code == 404


async def test_push_without_remote(jp_fetch, tmp_path, monkeypatch):
    class FakeLocalDataset:
        def push(self):
            raise ValueError("no remote")

    monkeypatch.setattr(handlers.fairly, "dataset", lambda id: FakeLocalDataset())

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "push",
            method="PATCH",
            body=json.dumps({"localdataset": str(tmp_path)}),
        )
    assert excinfo.value.code == 405


# --- pull -------------------------------------------------------------------

async def test_pull_not_implemented(jp_fetch, tmp_path):
    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "pull",
            method="PATCH",
            body=json.dumps({"localdataset": str(tmp_path)}),
        )
    assert excinfo.value.code == 501


# --- repo-token -------------------------------------------------------------

async def test_register_token(jp_fetch, tmp_path, monkeypatch):
    # keep the handler's os.makedirs('~/.fairly') away from the real home
    monkeypatch.setenv("HOME", str(tmp_path))

    saved = {"called": False}

    class FakeClient:
        config = {}

        def save_config(self):
            saved["called"] = True

    fake_client = FakeClient()
    monkeypatch.setattr(handlers.fairly, "client", lambda id: fake_client)

    response = await jp_fetch(
        "jupyter-fairly", "repo-token",
        method="POST",
        body=json.dumps({"client": "zenodo", "token": "s3cr3t"}),
    )

    assert response.code == 200
    assert fake_client.config["token"] == "s3cr3t"
    assert saved["called"]
    payload = json.loads(response.body)
    assert payload["client"] == "zenodo"


async def test_register_token_invalid_client(jp_fetch, tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))

    def raise_value_error(id):
        raise ValueError(f"invalid client: {id}")

    monkeypatch.setattr(handlers.fairly, "client", raise_value_error)

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "repo-token",
            method="POST",
            body=json.dumps({"client": "nope", "token": "s3cr3t"}),
        )
    assert excinfo.value.code == 400


# --- datasets ---------------------------------------------------------------

async def test_account_datasets(jp_fetch, monkeypatch):
    fake_datasets = [
        SimpleNamespace(
            id={"id": "123456", "version": "1"},
            title="a title",
            size=42,
            created="2026-01-01",
            modified="2026-01-02",
            url="https://example.org/123456",
        )
    ]

    class FakeClient:
        def get_account_datasets(self):
            return fake_datasets

    monkeypatch.setattr(handlers.fairly, "client", lambda id: FakeClient())

    # the endpoint reads the client name from the body of a GET request
    response = await jp_fetch(
        "jupyter-fairly", "datasets",
        method="GET",
        body=json.dumps({"client": "zenodo"}),
        allow_nonstandard_methods=True,
    )

    assert response.code == 200
    payload = json.loads(response.body)
    assert payload["count"] == 1
    assert payload["datasets"][0]["id"] == "123456"


async def test_account_datasets_auth_failure(jp_fetch, monkeypatch):
    class FakeClient:
        def get_account_datasets(self):
            raise RuntimeError("bad credentials")

    monkeypatch.setattr(handlers.fairly, "client", lambda id: FakeClient())

    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch(
            "jupyter-fairly", "datasets",
            method="GET",
            body=json.dumps({"client": "zenodo"}),
            allow_nonstandard_methods=True,
        )
    assert excinfo.value.code == 401
