"""Implementation of Data Repository for 4TU Reasearch Data"""

import requests
from data_repository import DataRepository

class FourTuResearchData(DataRepository):

    def __init__(self) -> None:
        pass

    def create_entry(self)-> None:
        pass
        
    def upload_data(self)-> None:
        pass


if __name__ == '__main__':

    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    BASE_URL = "https://api.figshare.com/v2/articles"

