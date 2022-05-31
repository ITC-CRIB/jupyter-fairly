# JupyterFAIR
 A jupyterLab extension for seamless integration of Jupyter-based research environments and research data repositories.

## Set up Dev Environment

1. Create a conda environment with
    ```shell
    conda create -n jupyterfair --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=3 cookiecutter nodejs jupyter-packaging git
    ```
2. Clone repository
3. Activate conda environment
4. Install, activate and build extension
    ```shell
    # Install package in development mode
    pip install -e .
    # Link your development version of the extension with JupyterLab
    jupyter labextension develop . --overwrite
    # Enable the server extension
    jupyter server extension enable jlab_ext_example
    # Rebuild extension Typescript source after making changes
    jlpm run build
    ```

