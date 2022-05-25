import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

from jupyterfair.core.connection import Connection
from jupyterfair.four_tu import FourTuResearchData

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /jupyterfair/get_example endpoint!"
        }))

class TUHandler(APIHandler):
    """Handler for the 4TU research data repository"""
    @tornado.web.authenticated
    def get(self, token):
        """"List articles for in an account"""

        TOKEN="Bearer 824bb04e551a8e66d7764ced7b9562504782d458a73b772b4162c553640e4a47bda6a39b84a78e7ae15d049b161799a56928158a03198480d9aa697beec0c095"
        BASE_URL = "https://api.figshare.com/v2/account"
        connection = Connection(BASE_URL, TOKEN)
        repo_api = FourTuResearchData(connection)
        list_of_articles=repo_api.list_articles()
        self.finish(json.dumps(list_of_articles))

def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterfair", "get_example")
    list_articles = url_path_join(base_url, "jupyterfair", "list_articles")
    handlers = [
        (route_pattern, RouteHandler), 
        (list_articles, TUHandler)
    ]
    web_app.add_handlers(host_pattern, handlers)
