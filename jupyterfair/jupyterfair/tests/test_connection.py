"""
Test for the Connection class
"""

import unittest
import os
import requests
from dotenv import load_dotenv
from jupyterfair.core.connection import Connection

load_dotenv('/home/manuel/Documents/devel/JupyterFAIR/jupyterfair/jupyterfair/core/.env')

# TODO: test connection using mock: https://realpython.com/testing-third-party-apis-with-mocks/
class TestConnection(unittest.TestCase):

    # fixtures
    def setUp(self) -> None:
        # load_dotenv('/home/manuel/Documents/devel/JupyterFAIR/jupyterfair/jupyterfair/core/.env')
        self.token = os.getenv('TOKEN')
        self.base_url = "https://api.figshare.com/v2/account"
        self.connection = Connection(self.base_url, self.token)
        return super().setUp()

    def test_get(self):
        """ Test if the GET returns retuns a Requests response object and a success status code: 200"""
        response = self.connection.get(self.base_url)
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(response.ok)
        
    def test_post(self):
        """ Test if the POST method returns a success status code: 200"""
        pass

    # clean up action
    def tearDown(self) -> None:
        self.connection.close_connection()
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()