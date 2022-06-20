'''
input parameters
target repository
Abstractions for Data Repository
'''
from abc import ABC, abstractmethod

import os
import json
import requests
from requests import Request, Session
from requests.exceptions import HTTPError
import hashlib
import zipfile

import jupyterfair.config as config


class Client(ABC):
    """ Abstract class for research data repositories"""
    # We use sessions to reuse TCP connection
    session = Session()

    @property
    @abstractmethod
    def TOKEN(cls):
        raise NotImplementedError

    @property
    @abstractmethod
    def BASE_URL(cls):
        raise NotImplementedError        
    
    def raw_issue_request(self, method, url, data=None, binary=False):
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
            print ('Caught an HTTPError: {}'.format(error))
            print ('Body:\n', response.content)
            raise
        return data
    
    def issue_request(self, method, endpoint, *args, **kwargs):
        '''Generic interface to issue different API requests with any method
        GET, POST, PUT, DELETE
        '''
        return self.raw_issue_request(method, self.BASE_URL.format(endpoint=endpoint), *args, **kwargs)
    
    def zip_data_dir(self, dir_path):
        """Here we asume the user has created a directory with data that can be
        zipped to be uploaded in one step
        """
        pass
        
        print("Compression finished")

    def get_file_check_data(self, file_name, chunksize):
        """md5 checksum and file size for a file"""
        with open(file_name, 'rb') as fin:
            md5 = hashlib.md5()
            size = 0
            data = fin.read(chunksize)
            while data:
                size += len(data)
                md5.update(data)
                data = fin.read(chunksize)
            return md5.hexdigest(), size 
    

    # TODO: Must be abstract method
    def make_connection():
        pass
    
    # TODO: Must be abstract method
    def close_connection(self):
        self.session.close()

    # TODO: Must be abstract method
    def get_archive_byId():
        '''
        '''
        pass
    
    @abstractmethod
    def create_archive(self, **kwargs):
        '''
        returns deposition url 
        ''' 
        pass
    
    @abstractmethod
    def del_archive(self, **kwargs):
        '''
        '''
        pass
    
    # TODO: Must be abstract method
    def write_metadata_record_locally():
        '''
        writes yaml file compliant with dublin core metadata standard

        '''
        pass     

    # TODO: Must be abstract method
    def load_local_metadata_record():
        '''
        loads 
        '''
        pass
    
    # TODO: Must be abstract method
    def update_archive():
        '''
        Creates a new version of existing record
        '''
        pass

    @abstractmethod
    def upload_data_to_archive():
        '''
        returns success
        '''
        pass

    # TODO: Must be abstract method
    def publish_archive():
        '''
        Returns publication status and url/doi 
        and stores it locally in a metadata file...
        '''
        pass
