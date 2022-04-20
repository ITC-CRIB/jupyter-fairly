# JupyterFAIR
JupyterFAIR aims to provide a tool for seamless integration of Jupyter-based research environments and research data repositories.

## Test bench to discover JupyFAIR requirements
Here I am experimetning with several concepts we have discussed:
1. Using figshare api to upload and download document.
2. Experiment with design patterns when possible
3. Explore ORCID to chain it with other events
4. Explore validation mechanisms.
5. Other ideas......

### Dir structure
I am keeping `extension/` and `figshare_example/` separate for the time being.

### Running the code
- I am using python virtual environments:
```sh
# Create environment for project
python3 -m venv .env

# Activate environment
source .env/bin/activate
```
- To reproduce the environment dependencies, I am relying on `setup.py`
- In development mode I install packages using `pip install -e .[dev]`. 
(`[dev]` will install the development dependencies.)

### Running the extension code
You need to have jupyterlab setup in your development environment, currently I added it as a dependency in the `extension/setup.py` file.

For more info on how extensions work go here: https://github.com/jupyterlab/extension-examples/tree/master/hello-world

Use the same environment, navigate to the extension folder and do: 

```sh
# install packages for extension in dev mode
pip install -e .[dev]

# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite

# Build the frontend app
npm run build

# Dont forget to activate environment if you havent
. <my_env>/bin/activate

# Dont forget to spin jupyter lab
jupyter lab
```


