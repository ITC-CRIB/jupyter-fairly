[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Jupyter Fairly
 A jupyterLab extension for the [fairly](https://github.com/ITC-CRIB/fairly) package, and the seamless integration of Jupyter-based research environments and research data repositories.

This extension is composed of a Python package named `jupyter_fairly`
for the server extension and a NPM package named `jupyter-fairly`
for the frontend extension.

## Requirements

- JupyterLab >= 3.0 < 4
- fairly == 0.4.1 

> This is the last version that supports JupyterLab 3.x. 

## Install

To install the extension, execute:

```bash
pip install jupyter_fairly
```

Configurations are stored in  `.fairly/config.json`  in the user's home directory. This is where the extension stores access tokens for data repositories.

To add an access tokens, use the **Fairly** menu in the JupyterLab main menu bar.

<img src="./img/fairly_menu.png" alt="Fairly Menu" width="450"/>


## Uninstall

To remove the extension, execute:

```bash
pip uninstall jupyter_fairly
```

## Troubleshoot

If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
```

If the server extension is installed and enabled, but you are not seeing
the frontend extension, check the frontend extension is installed:

```bash
jupyter labextension list
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the jupyter_fairly directory
# Install package in development mode
pip install -e ".[test]"
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable jupyter_fairly
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
# Server extension must be manually disabled in develop mode
jupyter server extension disable jupyter_fairly
pip uninstall jupyter_fairly
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `jupyter-fairly` within that folder.

### Testing the extension

#### Server tests

This extension is using [Pytest](https://docs.pytest.org/) for Python code testing.

Install test dependencies (needed only once):

```sh
pip install -e ".[test]"
# Each time you install the Python package, you need to restore the front-end extension link
jupyter labextension develop . --overwrite
```

To execute them, run:

```sh
pytest -vv -r ap --cov jupyter_fairly
```

#### Frontend tests

This extension is using [Jest](https://jestjs.io/) for JavaScript code testing.

To execute them, execute:

```sh
jlpm
jlpm test
```

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro/) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

### Packaging the extension

See [RELEASE](RELEASE.md)


## Citation

Please cite this software using as follows:

  *Garcia Alvarez, M.,  Girgin, S., & Urra Llanusa, J., Jupyter-fairly: a JupyterLab extension for the fairly pacakage [Computer software]*


## Acknowledgements

This research is funded by the [Dutch Research Council (NWO) Open Science Fund](https://www.nwo.nl/en/researchprogrammes/open-science/open-science-fund/), File No. 203.001.114.

Project members:

- [Center of Expertise in Big Geodata Science, University of Twente, Faculty ITC](https://itc.nl/big-geodata/)
- [Digital Competence Centre, TU Delft](https://dcc.tudelft.nl/)
- [4TU.ResearchData](https://data.4tu.nl/)
