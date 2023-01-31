from distutils import extension
import json
import tornado
import os

from lib2to3.pgen2 import token
from turtle import st
from typing import Dict, List
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from dotenv import load_dotenv
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
            "message": f"This is /jupyterfair/example endpoint. Jupyter Server is Online!",
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
        # http://127.0.0.1:8888/jupyterfair/newdataset?token=295c3a87c6
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
        }
        """
     
        # body of the request
        data = self.get_json_body() # returns a dictionary
        
        try:
            # creates lazy object for valid identifier
            dataset = fairly.dataset(data["source"])
        
        except ValueError:
            # Raised when a url, doi is not known by fairly
            raise web.HTTPError(400, f"Unknown URL or DOI: {data['source']}")
        
        try:
            # download files and store them in local directory
            dataset.store(path=data["destination"])
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
    
            dataset (str): path to root directory of fairly dataset
            client (str): supported client.  'figshare' or 'zenodo'.

        Body example as JSON:
        {
            
            "dataset": <path to root directory of fairly dataset>,
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
            local_dataset = fairly.dataset(data["dataset"])
        except NotADirectoryError:
            # throws error when path is not a directory
            raise web.HTTPError(404, f"Invalid path to directory: {data['dataset']}")
        
        try:
            local_dataset.upload(client)
        except ValueError:
            # generic error, it raises if anything goes wrong with upload
            raise web.HTTPError(500, f'Something went wrong with uploading')
        else:
            self.finish(json.dumps({ 
                "message": 'completed',
                }))


    def patch(self):
        """ Send updates on files and metadata to remore repository"""

        raise web.HTTPError(501, "Not implemented")

    
def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    extension_url = url_path_join(base_url, "jupyterfair")
    example_url = url_path_join(extension_url, "example")
    datasets_url = url_path_join(extension_url, "datasets")
    initialize_dataset_url = url_path_join(extension_url, "newdataset")
    clone_dataset_url = url_path_join(extension_url, "clone")
    upload_dataset_url = url_path_join(extension_url, "upload")

    
    handlers = [
        (example_url, ExampleEndpoint),
        (datasets_url, AccountDatasets),
        (initialize_dataset_url, InitFairlyDataset),
        (clone_dataset_url, CloneDataset),
        (upload_dataset_url, UploadDataset),
    ]

    web_app.add_handlers(host_pattern, handlers)
