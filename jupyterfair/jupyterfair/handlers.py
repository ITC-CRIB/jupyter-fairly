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

## FOR TESTING ONLY
load_dotenv()
FOURTU_TOKEN= os.environ['FOURTU_TOKEN']
#######################

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        # param = self.get_query_argument("param1") # this is how to define query parameters.
        # url query = url/to/extension?<param>=<value>

        self.finish(json.dumps({
            "data": f"This is /jupyterfair/get_test endpoint... Hoora! Jupyter Server is Online!!!"
        }))


class AccountDatasets(APIHandler):
    """Handler for listing datasets in a user account     
    return: JSON array
    """
    
    # class attributes will be reused between http calls
    fourtu_client = fairly.client(id="figshare", token=FOURTU_TOKEN)

    # TODO: this is how to pass parameters to the handlers
    # def __init__(self, *args, **kwargs):
    #     self.extra = kwargs.pop('token')

    @tornado.web.authenticated
    def get(self):
        """
        Returns a count and list of datasets an user account as JSON. 
        Datasets are listed as 'id' and 'version'
        Example:
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

        # TODO: handler return an error:
        #     raise HTTPError(http_error_msg, response=self)
        # requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://api.figshare.com/v2/account/licenses

        # TODO: handler should allow instantiating different clients
        account_datasets = self.fourtu_client.get_account_datasets()

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
    manifest.yaml file containing basic metadata will be created in a root 
    directory.
    """

    @tornado.web.authenticated
    def post(self):
        """
        Creates a manifest.yalm file based on a template.

        Args:
            root (str): path to the dataset directory
            template (str): name of the template to use on manifest.yalm
        
        Body of the request must contain values for root and template 
        as JSON:
        {
            "root": <path to dataset root directory>,
            "template"": <template name>
        }
        """

        # for post the token must be passed in the URL
        # http://127.0.0.1:8888/jupyterfair/newdataset?token=295c3a87c6
        # 
    
        # body of the request
        data = self.get_json_body() # returns dictionary

        try:
            fairly.init_dataset(path=data["path"], template=data["template"])
        except ValueError:
            # TODO, this exception is too general. It should be raised only 
            # when the dataset was already initialized
            raise web.HTTPError(403, "Failed to initialize dataset")

        self.finish(json.dumps({
            "action": 'initialized dataset', 
            "path": data['path'],
            "template": data['template']
            }))


class CloneDataset(APIHandler):
    """
    Handler for cloning (copying) a remote dataset to a directory,
    using a dataset identifier.
    """
    # class attributes will be reused between http calls

    @tornado.web.authenticated
    def post(self):
        """
        Downloads a remote dataset to a local directory

        Args:
            source (str): ID of dataset in repository, or dataset URL, or dataset DOI.
            destination (str): path to a directory to download the dataset. Raise value error 
            if directory is not empty.
            client (str): supported client.  'figshare' or 'zenodo'.

        Body of the request must contain values for dataset_id and directory 
        as JSON:
        {
            "source": <doi or url of the dataset>,
            "destination": <path to directory>,
            "client": <client name>
        }
        """
     
        # body of the request
        data = self.get_json_body() # returns a dictionary
        
        # print(data)
        try:
            # TODO: token should be read from config file
            client = fairly.client(id=data["client"], token=FOURTU_TOKEN)
        except ValueError:
            raise web.HTTPError(400, f"Invalid client id: {data['client']}")
        
        try:
            # TODO: error with possibly the json encoding for the url dataset, or
            # due to cross domain policies: https://www.w3schools.com/js/js_json_jsonp.asp

            print('source', data["source"])
            # connecto to remote dataset and retrieve metadata
            dataset = client.get_dataset(id=data["source"])
        except ValueError:
            # TODO, this exception is too general. It should be raised only 
            # when the dataset was already initialized
            raise web.HTTPError(401, f"Authentification failed for: {data['client']}")
        
        try:
            print("call to store()")
            # download files and store them in local directory
            dataset.store(path=data["destination"])
        except ValueError:
            raise web.HTTPError(403, f"Can't clone dataset to not-empty directory." )
        
        self.finish(json.dumps({
            "action": 'cloning dataset', 
            "destination": data['destination'],
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
    
            directory (str): path to directory 
            client (str): supported client.  'figshare', '4tu or 'zenodo'.

        Body of the request must contain values for dataset_id and directory 
        as JSON:
        {
            
            "directory": <path to directory>,
            "client": <client name>
        }
        """
        
        # body of the request
        data = self.get_json_body() # returns dictionary
        
        try:
            client = fairly.client(id=data["client"], token=FOURTU_TOKEN)
        except ValueError:
            raise web.HTTPError(400, f"Invalid client id: {data['client']}")

        try:
            local_dataset = fairly.dataset(data["directory"])
        except NotADirectoryError:
            # throws error when path is not a directory
            raise web.HTTPError(404, f"Invalid path to directory: {data['directory']}")
        
        try:
            local_dataset.upload(client)
        except ValueError:
            # generic error it raises if anything goes wrong with upload
            raise web.HTTPError(500, f'Something went wrong with uploading')
        
        self.finish(json.dumps({
            "action": 'upload dataset', 
            "status": 'complete',
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
        (example_url, RouteHandler),
        (datasets_url, AccountDatasets),
        (initialize_dataset_url, InitFairlyDataset),
        (clone_dataset_url, CloneDataset),
        (upload_dataset_url, UploadDataset),


    ]

    web_app.add_handlers(host_pattern, handlers)
