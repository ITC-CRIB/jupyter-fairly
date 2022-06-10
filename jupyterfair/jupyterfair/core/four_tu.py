from jupyterfair.core.client import *

class FourTuData(Client):
    '''
    '''
    TOKEN = config.FOURTU_TOKEN
    BASE_URL = 'https://api.figshare.com/v2/{endpoint}'
    CHUNK_SIZE = 1048576

    # BASE_URL = 'https://api.figsh.com/v2/{endpoint}'

    def create_archive(self, article_title):
        '''
        
        '''
        data = {
            'title': article_title  # You may add any other information about the article here as you wish.
        }
        response = self.issue_request('POST', 'account/articles', data=data)
        data = json.loads(response.content)
        print ('Created article:', data['location'], '\n')
        return response

    def get_archive(self, article_id):
        '''article_id: str or int'''
        assert type(article_id) is str, "Article id is not a string"
        if article_id is int: article_id = str(article_id) 
        return self.issue_request('GET', f'account/articles/{article_id}').content
    
    def del_archive(self, article_id):
        '''article_id: str or int'''
        assert type(article_id) is str, "Article id is not a string"
        if article_id is int: article_id = str(article_id) 
        return self.issue_request('DELETE', f'account/articles/{article_id}?page=&page_size=10').content

    def list_my_archives(self):
        return self.issue_request('GET', 'account/articles')

    def upload_data_to_archive(self, archive_id, file_path):
        '''
        archive_id: str containing the id where the archive is located
        returns 
        '''
        def initiate_new_upload(self, archive_id, file_path):
            """ 
            Returns a response for initiated upload
            figshare api needs to initiate an upload before publishing an article
            and uploading files to it

            - response.content: A dict like::
            {
                b'{"location": "https://api.figshare.com/v2/account/articles/20047799/files/35857895"}'
            }
            """
            endpoint = f'account/articles/{archive_id}/files'
            md5, size = self.get_file_check_data(file_path, self.CHUNK_SIZE)
            
            assert size > 0, "Cannot upload empty file"

            data = {'name': os.path.basename(file_path),
                    'md5': md5,
                    'size': size}
            response = self.issue_request('POST', endpoint, data=data)
            data = json.loads(response.content)
            print ('Initiated file upload:', data['location'], '\n')
            return response

        def upload_part(self, upload_url, stream, part):
            """ Uploads one part of a file
            file_info: dict contains url location of the file to be uploaded
            {"location" : <url_file_path> }
            stream: file stream to be uploaded
            part: dict part of the file to be uploaded
            """
            udata = { "upload_url" : upload_url }
            udata.update(part)
            # Create the url from upload_url and part number data
            url = '{upload_url}/{partNo}'.format(**udata)
            print(url)    

            stream.seek(part['startOffset'])
            data = stream.read(part['endOffset'] - part['startOffset'] + 1)

            self.raw_issue_request('PUT', url, data=data, binary=True)
            print (f'Uploaded part{part["partNo"]} from {part["startOffset"]} to {part["endOffset"]}')

        def upload_parts(self, file_info, file_path):
            """
            - file_info: dict contains url location of the file to be uploaded
            {"location" : <url_file_path> }
            
            - file_path: str
            
            - Returns 201 status code object
            """

            # Here we get the an upload object from the upload service endpoints
            # Locate the file url
            upload_url = self.raw_issue_request('GET', file_info['location'])
            upload_url = json.loads(upload_url.content)
            # Gets the upload url from file location
            upload_url = upload_url['upload_url']

            upload = self.raw_issue_request('GET', upload_url)
            upload = json.loads(upload.content)
            print ('Uploading parts:')
            with open(file_path, 'rb') as fin:
                for part in upload['parts']:
                    upload_part(self, upload_url, fin, part)
            print("File upload finished")

        def complete_upload(self, article_id: str, file_id : str):
            """Confirms that the upload has been finished
            """
            self.issue_request('POST', 'account/articles/{}/files/{}'.format(article_id, file_id))

        
        file_info = json.loads(initiate_new_upload(self, archive_id, file_path).content)
        file_id = file_info['location'].split("/")[-1]
        # Until here we used the figshare API; following lines use the figshare upload service API.
        upload_parts(self, file_info, file_path)
        # We return to the figshare API to complete the file upload process.
        complete_upload(self, archive_id, file_id)
