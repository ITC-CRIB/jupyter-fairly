import json
import tornado
import os
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from tornado import web
import fairly

############# IMPORTANT #####################################################
# Tokens for fairly clients are read from config.json in the home directory.
# For linux the path is ~/.fairly/config.json
# For Windows the path is [?]
############################################################################

class FairlyAPIHandler(APIHandler):
    """Base handler with helpers shared by the jupyter-fairly endpoints."""

    def get_body(self, *required):
        """Return the JSON request body, validating the required fields.

        Raises HTTPError 400 when the body is missing, is not valid JSON,
        or lacks any of the required fields.
        """
        data = self.get_json_body()
        if data is None:
            raise web.HTTPError(400, "Request body must be valid JSON")
        missing = [field for field in required if field not in data]
        if missing:
            raise web.HTTPError(
                400, f"Missing fields in request body: {', '.join(missing)}"
            )
        return data


class ExampleEndpoint(FairlyAPIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "message": "This is /jupyter-fairly/example endpoint. Jupyter Server is Online!",
            "from": " The JupyterFAIR Team"
        }))


class AccountDatasets(FairlyAPIHandler):
    """Handler for listing datasets in a user account     
    return: JSON array
    """
    
    @tornado.web.authenticated
    def get(self):
        """
        Returns a count and list of datasets an user account as JSON. 
        Datasets are listed as 'id' and 'version'.

        Args:
            client (str): supported client.  'figshare' or 'zenodo'.

        Body example:
            {
                "client": <client name>
            }

        Response example:
        {
            "count": 1,
            "datasets": 
            [
                {
                    "id": "123456",
                    "title": "a title",
                    "version": null,
                    "size": "X MB",
                    "created": "timestamp",
                    "modified": "timestamp",
                    "url": "url"
                }
            ]
        }
        """

        # catch body of the request
        data = self.get_body("client")

        try:
            # tokens are read from .fairly/config.json
            client = fairly.client(id=data["client"])
        except ValueError:
            raise web.HTTPError(400, f"Invalid client id: {data['client']}")

        try:
            # connect to data repository and retrieve list of datasets
            account_datasets = client.get_account_datasets()
        except Exception:
            # TODO: a not too general exception must be raised when authentication fails
            raise web.HTTPError(401, f"Authentication failed for: {data['client']}")
        else:
            datasets = [ {
                "id": dataset.id['id'], 
                "title": dataset.title,
                "version": dataset.id['version'],
                "size": dataset.size,
                "created": dataset.created,
                "modified": dataset.modified,
                "url": dataset.url
                }  for dataset in account_datasets]
    
            self.finish(json.dumps({"count": len(datasets), "datasets": datasets}, default=str))


class InitFairlyDataset(FairlyAPIHandler):
    """
    Handler for initializing a Fairly dataset. By initializing a dataset, a
    manifest.yaml file containing a template for metadata will be created in 
    target directory.
    """

    @tornado.web.authenticated
    def post(self):
        """
        Creates a manifest.yalm file based on a template.

        Args:
            path (str): path to the dataset root directory
            template (str): name of the template to use on manifest.yalm
        
        Body example:
        {
            "path": <path to dataset root directory>,
            "template"": <template name>
        }
        """

        # body of the request
        data = self.get_body("path", "template")

        try:
            fairly.init_dataset(path=data["path"], template=data["template"])
        except (ValueError, PermissionError):
            # fairly < 1 raised ValueError for an already-initialized dataset,
            # fairly >= 2 raises PermissionError
            # TODO, this exception is too general. It should be raised only
            # when the dataset was already initialized
            raise web.HTTPError(403, "Failed to initialize dataset")

        # TODO, implement exception for invalid/unknown template name
        else:
            self.finish(json.dumps({
                "message": 'Dataset initialized',
                }))


class CloneDataset(FairlyAPIHandler):
    """
    Handler for cloning (copying) a remote dataset to a loca directory,
    using a dataset identifier.
    """
    # class attributes will be reused between http calls

    @tornado.web.authenticated
    def post(self):
        """
        Downloads a remote dataset to a local directory

        Args:
            source (str): ID of dataset in  data repository, or dataset URL, or dataset DOI.
            path (str): path to a directory to download the dataset. Raise value error 
            if directory is not empty.
            client (str): supported client.  'figshare' or 'zenodo'.

        Body example as JSON:
        {
            "source": <doi or url of the dataset>,
            "destination": <path to directory>,
            "extract": <boolean>
        }
        """
     
        # body of the request
        data = self.get_body("source", "destination", "extract")

        try:
            # creates lazy object for valid identifier
            dataset = fairly.dataset(data["source"])

        except ValueError:
            # Raised when a url, doi is not known by fairly
            raise web.HTTPError(400, f"Unknown URL or DOI for: {data['source']}")

        try:
            # download files and store them in local directory
            dataset.store(path=data["destination"], extract=data["extract"])
        except ValueError:
            raise web.HTTPError(403, "Can't clone dataset to not-empty directory.")
        except ConnectionError:
            raise web.HTTPError(503, "Can't connect to data repository")
        else:
            self.finish(json.dumps({
                "message": 'completed', 
                "destination": data["destination"],
                }))


class UploadDataset(FairlyAPIHandler):
    """
    Handler for uploading metadata and files to a data reposiotory
    """

    @tornado.web.authenticated
    def post(self):
        """
        Uploads local dataset to a remote data repository.

        Args:
    
            directory (str): path to root directory of initialized fairly dataset
            client (str): supported client.  'figshare' or 'zenodo'.

        Body example as JSON:
        {
            
            "directory": <path to root directory of fairly dataset>,
            "client": <client name>
        }
        """
        
        # body of the request
        data = self.get_body("directory", "client")

        try:
            client = fairly.client(id=data["client"])
        except ValueError:
            raise web.HTTPError(400, f"Invalid client id: {data['client']}")

        try:
            # TODO: fix bug:
            # Error messages:
                # requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://api.figshare.com/v2/account/articles

            local_dataset = fairly.dataset(data["directory"])
        except NotADirectoryError:
            # throws error when path is not a directory
            raise web.HTTPError(404, f"Invalid path to directory: {data['directory']}")

        try:
            local_dataset.upload(client)
        except ValueError as e:
            # generic error, it raises if anything goes wrong with upload
            raise web.HTTPError(500, f'Something went wrong with uploading: {e}')
        except Warning:
            raise web.HTTPError(409, "Dataset already exists in data repository. Use \
                                the update option to update the dataset.")
        else:
            self.finish(json.dumps({ 
                "message": 'completed',
                }))


class PushDataset(FairlyAPIHandler):
    """
    Handler for pushing updates on files and metadata to data repository
    """

    @tornado.web.authenticated
    def patch(self):
        """ Updates files and metadata in existing dataset in data repository
        
        Args:
    
            localdataset (str): path to root directory of initialized fairly dataset
                             witch a remote registered in the manifest.yaml file

        Body example as JSON:
        {
            
            "localdataset": <path to root directory of fairly dataset>
        }
        """

        data = self.get_body("localdataset")

        try:
            local_dataset = fairly.dataset(data["localdataset"])

        except FileNotFoundError as e:
            raise web.HTTPError(404, f"Manifest file is missing from current directory: {e}")
        except NotADirectoryError as e:
            raise web.HTTPError(404, f"Path to dataset is not a directory: {e}")

        try:
            local_dataset.push() # push updates (files and metadata) to remote repository
        except ValueError:
            raise web.HTTPError(405, "The dataset doesn't have a remote. Make sure you're in the right directory or use `upload` option first.")
        except KeyError as e:
            raise web.HTTPError(400, f"Possible malformed manifest file. Missing {e}")
        else:
            self.finish(json.dumps({
                "message": 'remote  dataset is up to date',
                }))


class PullDataset(FairlyAPIHandler):
    """
    Handler for pulling updates on files and metadata to remore repository
    """

    @tornado.web.authenticated
    def patch(self):
        """ Updates files and metadata in local dataset based on changes in data repository.
        
        Args:
    
            localdataset (str): path to root directory of initialized fairly dataset
                             witch a remote registered in the manifest.yaml file

        Body example as JSON:
        {
            
            "localdataset": <path to root directory of fairly dataset>
        }
        """
        # TODO: implement using fairly's pull support: load the local dataset
        # with fairly.dataset(), fetch the remote changes, and save them to
        # manifest.yaml and the local files.
        raise web.HTTPError(501, "Not implemented yet")


class RegisterRepositoryToken(FairlyAPIHandler):
    """ 
    Handler for registring tokens of data repositories a local
    Fairly configuration file.
    """

    @tornado.web.authenticated
    def post(self):
        """
        Registers a new token for a data repository.

        Args:
            client (str): supported client.  'figshare', '4tu' or 'zenodo'.
            token (str): token of the account in data repository.

        Body example as JSON:
            {
                "client": <client name>,
                "token": <token>
            }
        """

        # body of the request
        data = self.get_body("client", "token")

        # Ensure the Fairly config directory exists in the user's home directory
        config_file_directory = os.path.expanduser('~/.fairly')
        os.makedirs(config_file_directory, exist_ok=True)

        # create client
        try:
            client = fairly.client(data["client"]) # repository referst to client name in fairly
        except ValueError:
            raise web.HTTPError(400, f"Invalid name for the client: {data['client']} \
                                Is the requested client supported by Fairly?")

        # add token to client
        client.config['token'] = data['token']
        # save client config to config file
        try:
            client.save_config()
        except FileNotFoundError:
            raise web.HTTPError(500, f"Path to configuration directory wasn't found: \
                                {config_file_directory}")
        
        self.finish(json.dumps({
            "message": "token successfully registered",
            "client": data['client'],
            "from": "The JupyterFAIR Team"
        }))


    
def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    extension_url = url_path_join(base_url, "jupyter-fairly")
    example_url = url_path_join(extension_url, "example")
    datasets_url = url_path_join(extension_url, "datasets")
    initialize_dataset_url = url_path_join(extension_url, "newdataset")
    clone_dataset_url = url_path_join(extension_url, "clone")
    upload_dataset_url = url_path_join(extension_url, "upload")
    push_dataset_url = url_path_join(extension_url, "push")
    pull_dataset_url = url_path_join(extension_url, "pull")
    register_token_url = url_path_join(extension_url, "repo-token")

    
    handlers = [
        (example_url, ExampleEndpoint),
        (datasets_url, AccountDatasets),
        (initialize_dataset_url, InitFairlyDataset),
        (clone_dataset_url, CloneDataset),
        (upload_dataset_url, UploadDataset),
        (push_dataset_url, PushDataset),
        (pull_dataset_url, PullDataset),
        (register_token_url, RegisterRepositoryToken)
    ]

    web_app.add_handlers(host_pattern, handlers)
