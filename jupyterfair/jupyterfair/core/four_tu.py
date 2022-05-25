"""Implementation of Data Repository for 4TU Reasearch Data"""


from data_repository import DataRepository
from connection import Connection

class FourTuResearchData(DataRepository):

    def __init__(self, connection) -> None:
        
        if isinstance(connection, Connection):
            self.connection = connection
        else:
            raise TypeError("connection attribute must be an instace of the Connection class")
        return None
        
    def create_entry(self, payload:dict)-> dict:
        """Creates an article in a 4TU.ResearchData account
        
        params:
            payload: metadata required for creating an article
        returns: response as JSON-like
        """
        if payload is None:
            raise ValueError("payload cannot be empty")

        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")

        request_url= self.connection.root_url + '/articles'
        response=self.connection.post(request=request_url, payload=payload)

        return response.json()
        
    def upload_data(self)-> None:
        pass


if __name__ == '__main__':

    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    BASE_URL = "https://api.figshare.com/v2/account"

    
    con = Connection(BASE_URL, TOKEN)

    payload={"title": "python test"}

    repo = FourTuResearchData(con)

    r = repo.create_entry(payload=payload)
    print( r )

   