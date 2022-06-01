# JupyterFAIR
 A jupyterLab extension for seamless integration of Jupyter-based research environments and research data repositories.

## Set up Dev Environment

1. Create a conda environment with
    ```shell
    conda create -n jupyterfair --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=3 cookiecutter nodejs jupyter-packaging git
    ```
2. Clone repository
3. Activate conda environment
4. Create a `.env` file in  the `jupyterfair/jupyterfair/` subfolder, and add a TOKEN (for now only 4TU personal tokens). Such as:
   ```
   TOKEN="Bearer <token-hash>"
   ```
5. Install, activate and build extension
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
6. On a new terminal, start the Jupyter Server
   ```shell
   jupyter server
   ```
7. Open the link in the terminal in a browser. Go to `http://127.0.0.1:8888/jupyterfair/get_example`. You should see the following message:
   ```json
   {"data": "This is /jupyterfair/get_test endpoint... Hoora! It works!!!"}
   ```

    > You will need to re-build the extension with `jlpm run build` and re-start **jupyter server** for changes to the soruce code take effect.

## Testing the communication with 4TU Research Data

If the development environment was successfully set up. You should be able to retrieve the list of articles in your 4TU account at this URL (an empty list will be showned if you have no articles):

```
http://127.0.0.1:8888/jupyterfair/list_articles
```


