from fairy_pkg.src.client import *

class Zenodo(Client):
    TOKEN = config.ZENODO_TOKEN
    BASE_URL = 'https://zenodo.org/api/{endpoint}'

    def create_deposition(self, **argv):
        pass

    def list_records(self):
        return self.issue_request('GET', 'records')