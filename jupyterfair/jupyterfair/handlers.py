from distutils import extension
import json
import tornado
import os

from lib2to3.pgen2 import token
from turtle import st
from typing import Dict, List
from typing_extensions import Self
from urllib import response
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from dotenv import load_dotenv
from tornado import web
import fairly

## FOR TESTING ONLY
load_dotenv()
FOURTU_TOKEN= os.environ['FOURTU_TOKEN']
#######################

# dummy creations 
def dummy_dataset(path: str, manifest_file: str='manifest.yalm'):

    with open(os.path.join(path, manifest_file),'rw') as manifest:
        pass



class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        param = self.get_query_argument("param1") # this is how to define query parameters.
        # url query = url/to/extension?<param>=<value>

        self.finish(json.dumps({
            "data": f"This is /jupyterfair/get_test endpoint... Hoora! Jupyter Server is Online. {param}!!!"
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
                    "version": null
                }
            ]
        }
        """
        # TODO: handler return an error:
        #     raise HTTPError(http_error_msg, response=self)
        # requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://api.figshare.com/v2/account/licenses

        account_datasets = self.fourtu_client.get_account_datasets()
        datasets = []
        for dataset in account_datasets:
            datasets.append(dataset.id) # collects metadata: id and version
        self.finish(json.dumps({"count": len(datasets), "datasets": datasets}))


class InitFairlyDataset(APIHandler):
    """
    Handler for initializing a Fairly dataset. By initializing a dataset, a
    manifest.yaml file containing basic metadata will be created in a root 
    directory

    path: path to root directory for the dataset
    template: metadata template
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


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    extension_url = url_path_join(base_url, "jupyterfair")
    example_url = url_path_join(extension_url, "get_example")
    datasets_url = url_path_join(extension_url, "datasets")
    initialize_dataset_url = url_path_join(extension_url, "newdataset")
    

    handlers = [
        (example_url, RouteHandler),
        (datasets_url, AccountDatasets),
        (initialize_dataset_url, InitFairlyDataset),

    ]
    web_app.add_handlers(host_pattern, handlers)
