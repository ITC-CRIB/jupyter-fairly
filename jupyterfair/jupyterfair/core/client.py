'''
input parameters
target repository
Abstractions for Data Repository
'''
from abc import ABC, abstractmethod

import json
import requests
from requests import Request, Session
from requests.exceptions import HTTPError
import fairy_pkg.config as config


class Client(ABC):
    """ Abstract class for research data repositories"""
    # Reuse TCP connection
    session = Session()

    @property
    @abstractmethod
    def TOKEN(cls):
        raise NotImplementedError

    @property
    @abstractmethod
    def BASE_URL(cls):
        raise NotImplementedError

    @abstractmethod
    def create_deposition(self, **argv):
        """Creates a new deposition"""
        pass

    # @abstractmethod
    # def upload_data(self, **argv):
    #     """Uploads files to the data repository"""
        
    
    def _raw_issue_request(self, method, url, data=None, binary=False):
        ''' Private method that implements full request including headers, auth, etc
        It allows to reuse the token and base url on every call
        '''
        headers = {'Authorization': 'token ' + self.TOKEN}
        if data is not None and not binary:
            data = json.dumps(data)
        response = self.session.request(method, url, headers=headers, data=data)
        try:
            response.raise_for_status()
            try:
                data = response
            except ValueError:
                data = response
        except HTTPError as error:
            print ('Caught an HTTPError: {}'.format(error.message))
            print ('Body:\n', response.content)
            raise
        return data
    
    def issue_request(self, method, endpoint, *args, **kwargs):
        '''Generic interface to issue different API requests with any method
        GET, POST, PUT, DELETE
        '''
        return self._raw_issue_request(method, self.BASE_URL.format(endpoint=endpoint), *args, **kwargs)

    def make_connection():
        pass

    def close_connection():
        pass

    def get_record():
        '''
        '''
        pass

    def create_record(self, **kwargs):
        '''
        returns deposition url 
        ''' 
        pass
    

    def write_rmetadata_record_locally():
        '''
        writes yaml file compliant with dublin core metadata standard

        '''
        pass     

    # Update
    def load_local_metadata_record():
        '''
        loads 
        '''
        pass
    
    
    def update_record():
        '''
        Creates a new version of existing record
        '''
        pass

    def upload_data():
        '''
        returns success
        '''
        pass

    def publish():
        '''
        Returns publication status and url/doi 
        and stores it locally in a metadata file...
        '''
        pass
