import json
from jupyterfair.core.four_tu import FourTuData
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

class TUHandler(APIHandler):
    """Handler for the 4TU research data repository"""
    @tornado.web.authenticated
    def get(self):
        """"List articles for in an account"""

        # ===================================================
        data_repository = FourTuData()
        list_of_archives=data_repository.list_my_archives()
        list = json.loads(list_of_archives)
        self.finish(json.dumps(list))



def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterfair", "get_example")
    route_archives = url_path_join(base_url, "jupyterfair", "archives")
    
    handlers = [
        (route_pattern, RouteHandler), (route_archives, TUHandler)
    ]
    web_app.add_handlers(host_pattern, handlers)
