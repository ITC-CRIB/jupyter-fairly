import json
from lib2to3.pgen2 import token
from typing import Dict
from urllib import response
import tornado
import os
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from dotenv import load_dotenv
from fairly import client

## FOR TESTING ONLY
load_dotenv()
FOURTU_TOKEN= os.environ['FOURTU_TOKEN']
#######################

_client = client(id="figshare", token=FOURTU_TOKEN)

# serialize properties of fairly.Author class
# TODO: utility functions should be moved to the fairly package.
def serialize_author(author) -> Dict:
    return {
        "name": author.name,
        "surname": author.surname,
        "fullname": author.fullname,
        "email": author.email,
        "institution": author.institution,
        "orcid_id": author.orcid_id
    }

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /jupyterfair/get_test endpoint... Hoora! It works!!!"
        }))


class Client(APIHandler):
    """Handler for interacting with the a fairly.client"""
    @tornado.web.authenticated
    #TODO: implement handlers for configuring client
    def get(self):

        pass


class Datasets(APIHandler):
    """Handler for datasets in a data repository"""
    @tornado.web.authenticated
    def get(self):
        """"List items associated with an account from a repository"""
        # ===================================================
        account_datasets = _client.get_account_datasets() # returns list of objects (RemoteDataset)

        # unwrap metadata
        datasets_metadata = []
        authors_metadata = []
        for dataset in account_datasets:
            metadata = dataset.serialize()
            #serialise authors metadata
            authors = metadata['metadata']['authors'] # list of instances of fairly.Author
            for author in authors:
                authors_metadata.append(serialize_author(author))
            
            # replace authors list in dataset metadata with serialised
            # authors metadata
            metadata['metadata']['authors'] = authors_metadata

            datasets_metadata.append(metadata)

        # handlers shouldn't do any data processing/transformation
        self.finish(json.dumps(datasets_metadata))

    
    # @tornado.web.authenticated
    # def post(self):
    #     """createsf a record in the data repository"""

    #     input_data = self.get_json_body() # input data: dict with a key "name"
        
    #     data_repository = FourTuData()
    #     response=data_repository.create_archive(input_data["title"])

    #     archive_meta = json.loads(response.content)
    #     data = {"New Archive": "".format(archive_meta["location"])}

    #     self.finish(json.dumps(data))

    #     #TODO: CONTINUE HERE 

def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterfair", "get_example")
    route_archives = url_path_join(base_url, "jupyterfair", "datasets")
    
    handlers = [
        (route_pattern, RouteHandler), (route_archives, Datasets)
    ]
    web_app.add_handlers(host_pattern, handlers)
