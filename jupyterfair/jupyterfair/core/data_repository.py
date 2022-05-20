"""
Abstractions for Data Repository
"""

from abc import ABC, abstractmethod


class DataRepository(ABC):
    """ Abstaract class for research data repositories"""
    
    @abstractmethod
    def create_entry(self, **argv):
        """Creates a new data entry in the data repository"""
        pass

    @abstractmethod
    def upload_data(self, **argv):
        """Uploads files to the data repository"""
