from distutils import extension
import json
import tornado
import os

from lib2to3.pgen2 import token
from turtle import st
from typing import Dict, List
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from tornado import web
import fairly

############# IMPORTANT #####################################################
# Tokens for fairly clients are read from config.json in the home directory.
# For linux the path is ~/.fairly/config.json
# For Windows the path is [?]
############################################################################

class ExampleEndpoint(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        # This is how to define query parameters.
        #   param = self.get_query_argument("param1")
        # example query: url/to/extension?<param>=<value>

        # This is how to pass and catch parameters in the handlers
            # def __init__(self, *args, **kwargs):
            # self.extra = kwargs.pop('token')

        self.finish(json.dumps({
            "message": f"This is /jupyterfairly/example endpoint. Jupyter Server is Online!",
            "from": " The JupyterFAIR Team"
        }))


class AccountDatasets(APIHandler):
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
        data = self.get_json_body() # returns a dictionary

        try:
            print(data)
            print('type', type(data))
            # tokens are read from .fairly/config.json
            client = fairly.client(id=data["client"])
        except ValueError:
            raise web.HTTPError(400, f"Invalid client id: {data['client']}")
        
        try:
            # connect to data repository and retrieve list of datasets
            account_datasets = client.get_account_datasets()
        except:
            # TODO: a not too general exception must be raised when authentification fails 
            raise web.HTTPError(401, f"Authentification failed for: {data['client']}")
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


class InitFairlyDataset(APIHandler):
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

        # for POST the token must be passed in the URL
        # http://127.0.0.1:8888/jupyterfairly/newdataset?token=295c3a87c6
        # 
    
        # body of the request
        data = self.get_json_body() # returns dictionary

        try:
            print(data)
            fairly.init_dataset(path=data["path"], template=data["template"])
        except ValueError:
            # TODO, this exception is too general. It should be raised only 
            # when the dataset was already initialized
            raise web.HTTPError(403, "Failed to initialize dataset")

        # TODO, implement exception for invalid/unknown template name
        else:
            self.finish(json.dumps({
                "message": 'Dataset initilized', 
                }))


class CloneDataset(APIHandler):
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
        data = self.get_json_body() # returns a dictionary
        
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
            raise web.HTTPError(403, f"Can't clone dataset to not-empty directory." )
        except ConnectionError:
            raise web.HTTPError(503, f"Can't connect to data repository")
        else:
            self.finish(json.dumps({
                "message": 'completed', 
                "destination": data["destination"],
                }))


class UploadDataset(APIHandler):
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
        data = self.get_json_body() # returns dictionary
        
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
            # print(client["token"])
            print(e)
            raise web.HTTPError(500, f'Something went wrong with uploading: {e}')
        except Warning:
            raise web.HTTPError(409, "Dataset already exists in data repository. Use \
                                the update option to update the dataset.")
        else:
            self.finish(json.dumps({ 
                "message": 'completed',
                }))


class PushDataset(APIHandler):
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

        data = self.get_json_body() 
        print(data)

        try:
            local_dataset = fairly.dataset(data["localdataset"])

        except FileNotFoundError as e:
            raise web.HTTPError(404, f"Manifest file is missing from current directory: {e}")
        except NotADirectoryError as e:
            raise web.HTTPError(404, f"Path to dataset is not a directory: {e}")

        try:
            local_dataset.push() # push updates (files and metadata) to remote repository
        except ValueError:
            raise web.HTTPError(405, f"The dataset doesn't have a remote. Use the upload option first.")
        else:
            self.finish(json.dumps({
                "message": 'remote  dataset is up to date',
                }))


class PullDataset(APIHandler):
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
        raise web.HTTPError(501, "Not implemented yet")

        data = self.get_json_body() 
        print(data)

        try:
            local_dataset = fairly.dataset(data["localdataset"])

        except FileNotFoundError as e:
            raise web.HTTPError(404, f"Manifest file is missing from current directory: {e}")
        except NotADirectoryError as e:
            raise web.HTTPError(404, f"Path to dataset is not a directory: {e}")

        try:
            local_dataset.push() # push updates (files and metadata) to remote repository
        except ValueError:
            raise web.HTTPError(405, f"The dataset doesn't have a remote. Use the upload option first.")
        else:
            # save changes to manifest.yaml
    
            self.finish(json.dumps({
                "message": 'local dataset is up to date',
                }))


class RegisterRepositoryToken(APIHandler):
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
        data = self.get_json_body() # returns dictionary
        
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
            "message": f"token sucessfully registered",
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
