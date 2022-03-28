#!/usr/bin/env python
import json
import requests
from requests.exceptions import HTTPError
import hashlib


# import environment variables object
from config import *

TOKEN = '4d68fd2d181057850b12bdbd4b1c5e8e027878572fd9b845d800fe9aad4b82dfb760ddafab7d063ba27b8f9178eb14337219aaf67c0d1c4a6e29cccbf844c872'
def raw_issue_request(method, url, data=None, binary=False):
    headers = {'Authorization': 'token ' + TOKEN}
    if data is not None and not binary:
        data = json.dumps(data)
    response = requests.request(method, url, headers=headers, data=data)
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


def issue_request(method, endpoint, *args, **kwargs):
    # Avoid this impure function using BASE_URL
    return raw_issue_request(method, BASE_URL.format(endpoint=endpoint), *args, **kwargs)


def list_articles():
    return issue_request('GET', 'account/articles')


def create_article(article_title):
    data = {
        'title': article_title  # You may add any other information about the article here as you wish.
    }
    response = issue_request('POST', 'account/articles', data=data)
    data = json.loads(response.content)
    print ('Created article:', data['location'], '\n')
    return response

def delete_article(article_id):
    '''article_id: str or int'''
    if article_id is int: article_id = str(article_id) 
    return issue_request('DELETE', f'account/articles/{article_id}')

def get_article_by_id(article_id):
    '''article_id: str or int'''
    if article_id is int: article_id = str(article_id) 
    return issue_request('GET', f'account/articles/{article_id}').content

def get_file_check_data(file_name):
    """md5 checksum and file size for a file"""
    with open(file_name, 'rb') as fin:
        md5 = hashlib.md5()
        size = 0
        data = fin.read(CHUNK_SIZE)
        while data:
            size += len(data)
            md5.update(data)
            data = fin.read(CHUNK_SIZE)
        return md5.hexdigest(), size   

def initiate_new_upload(article_id, file_name):
    """ figshare api needs to initiate an upload before publishing an article
    and uploading files to it
    """
    endpoint = f'account/articles/{article_id}/files'
    md5, size = get_file_check_data(file_name)
    
    assert size > 0, "Cannot upload empty file"

    data = {'name': os.path.basename(file_name),
            'md5': md5,
            'size': size}
    response = issue_request('POST', endpoint, data=data)
    data = json.loads(response.content)
    print ('Initiated file upload:', data['location'], '\n')
    return response

def upload_part(upload_url, stream, part):
    """
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

    raw_issue_request('PUT', url, data=data, binary=True)
    print (f'Uploaded part{part["partNo"]} from {part["startOffset"]} to {part["endOffset"]}')

def upload_parts(file_info, file_path):
    """
    file_info: dict contains url location of the file to be uploaded
    {"location" : <url_file_path> }
    file_path: str
    returns response with 201 status code
    """

    # Here we get the an upload object from the upload service endpoints
    # Locate the file url
    upload_url = raw_issue_request('GET', file_info['location'])
    upload_url = json.loads(upload_url.content)
    # Gets the upload url from file location
    upload_url = upload_url['upload_url']

    upload = raw_issue_request('GET', upload_url)
    upload = json.loads(upload.content)
    print ('Uploading parts:')
    with open(file_path, 'rb') as fin:
        for part in upload['parts']:
            upload_part(upload_url, fin, part)
    
    # TODO: return a response of success 201

# def complete_upload(article_id, file_id):
#     issue_request('POST', 'account/articles/{}/files/{}'.format(article_id, file_id))

# def upload_part(file_info, stream, part):
#     udata = file_info.copy()
#     udata.update(part)
#     url = '{upload_url}/{partNo}'.format(**udata)

#     stream.seek(part['startOffset'])
#     data = stream.read(part['endOffset'] - part['startOffset'] + 1)

#     raw_issue_request('PUT', url, data=data, binary=True)
#     print '  Uploaded part {partNo} from {startOffset} to {endOffset}'.format(**part)


# def upload_parts(file_info):
#     url = '{upload_url}'.format(**file_info)
#     result = raw_issue_request('GET', url)

#     print 'Uploading parts:'
#     with open(FILE_PATH, 'rb') as fin:
#         for part in result['parts']:
#             upload_part(file_info, fin, part)
#     print


# def main():
#     # We first create the article
#     list_articles()
#     article_id = create_article(TITLE)
#     list_articles()
#     list_files_of_article(article_id)

#     # Then we upload the file.
#     file_info = initiate_new_upload(article_id, FILE_PATH)
#     # Until here we used the figshare API; following lines use the figshare upload service API.
#     upload_parts(file_info)
#     # We return to the figshare API to complete the file upload process.
#     complete_upload(article_id, file_info['id'])
#     list_files_of_article(article_id)


# if __name__ == '__main__':
#     main()