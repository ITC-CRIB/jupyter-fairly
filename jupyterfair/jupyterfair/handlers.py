import json
from urllib import response
import tornado
import os
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from dotenv import load_dotenv


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
    """Handler for the 4TU research data repository"""
    @tornado.web.authenticated
    def get(self):

        pass


class Archive(APIHandler):
    """Handler for the 4TU research data repository"""
    @tornado.web.authenticated
    def get(self):
        """"List articles associated with an account"""
        # ===================================================
        data_repository = FourTuData()
        response=data_repository.list_my_archives() # returns bytes
        archives = json.loads(response.content) # decoding 

        # handlers shouldn't do any data processing/transformation
        self.finish(json.dumps(archives))
    
    @tornado.web.authenticated
    def post(self):
        """createsf a record in the data repository"""

        input_data = self.get_json_body() # input data: dict with a key "name"
        
        data_repository = FourTuData()
        response=data_repository.create_archive(input_data["title"])

        archive_meta = json.loads(response.content)
        data = {"New Archive": "".format(archive_meta["location"])}

        self.finish(json.dumps(data))

        #TODO: CONTINUE HERE 



def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterfair", "get_example")
    route_archives = url_path_join(base_url, "jupyterfair", "archive")
    
    handlers = [
        (route_pattern, RouteHandler), (route_archives, Archive)
    ]
    web_app.add_handlers(host_pattern, handlers)
