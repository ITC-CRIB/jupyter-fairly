
from requests import Request, Session
from requests.utils import requote_uri

class Connection(object):
    '''
    A class for creating HTTP connections to data repositories using TOKEN-based authentification
    '''

    def __init__(self, root_url: str, token: str ) -> None:
        """
        Creates and test a connection (Session) to a data repository endpoint.
        Connections use digested credentials, and supports multiple simultaneous connections (requests).

        Params:
            base_url: data repository  base endpoint
            token: authorization token
        """

        self.root_url = root_url
        self.token = token
        self.session = Session()
        self.status = "Use test_connection() before checking the connection status"
        self.session.headers.update({'Authorization': self.token})

    def test_connection(self) -> bool:
        '''
        Tests connection and update the "status" attribute upon success.
        
        returns:
            True on sucessful connection
        '''
        
        try:
            test_request= Request('GET', self.root_url)
            prepare = self.session.prepare_request(test_request)
            response = self.session.send(prepare)
        except ConnectionError:
            print("Connection failed. Check if the roor_url is set correctly and if the remote server is responsive")
        else:
            self.status = response.status_code
            print("Test completed! Status code:", self.status)
            return True

    def close_connection(self) -> None:
        '''
        Ends the connection and closes the connection session.
        '''

        self.session.close()
        print(f"Session for {self.session} was closed by user")
        return None

    def get(self, request:str, stream:bool=False, timeout:int=None, headers:dict={}) -> object:
        '''
        Implements the HTTP-GET method

        Args:
            request: a valid URL
            stream: set data streaming. Default is FALSE
            hearders: HTTP headers
        
        Returns: requests object
        '''
        encode_request = requote_uri(request)
        get_request= Request('GET', encode_request, headers=headers)
        prepare = self.session.prepare_request(get_request)
        response = self.session.send(prepare, verify=True, stream=stream, timeout=timeout) # timeout=None, wait forever for a response
        response.raise_for_status
        return response

    def post(self, request:str, stream:bool=False, timeout:int=None, headers:dict={}) -> object:
        '''
        Implements the HTTP-POST method

        Args:
            request: a valid URL
            stream: set data streaming. Default is FALSE
            hearders: HTTP headers
        
        Returns: requests object
        '''
        encode_request = requote_uri(request)
        get_request= Request('GET', encode_request, headers=headers)
        prepare = self.session.prepare_request(get_request)
        response = self.session.send(prepare, verify=True, stream=stream, timeout=timeout) # timeout=None, wait forever for a response
        response.raise_for_status

        return response
