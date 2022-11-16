#!/usr/bin/env python
""" This module is called test_bench.py because I am using it as a main entry point
to explore and document the functionalities I am testing. It is not following at the moment
a specific architecture, or testing best practices, mostly used to do TDD,
"""
import os
import json
import random
import time
import string

import requests
from requests.exceptions import HTTPError

import pytest

# Import developed modules 
import jupyterfair.config as config
from jupyterfair.core.four_tu import *


BASE_URL = 'https://api.figshare.com/v2/{endpoint}'
TOKEN = config.FOURTU_TOKEN
CHUNK_SIZE = 1048576

FIXTURES = './tests/fixtures/' # FIXTUREStures path
DUMMY_PROJECT= f'./jupyterfair/tests/fixtures/dummy_project/'

def create_file(n, d, path, file_name):
    f = open(f'{path}/{file_name}', 'w')
    for i in range(n):
        nums = [str(round(random.uniform(0, 1000 * 1000), 3)) for j in range(d)]
        f.write(' '.join(nums))
        f.write('\n')
    f.close()

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

def list_files_of_article(article_id):
    result = issue_request('GET', 'account/articles/{}/files'.format(article_id))
    print('Listing files for article {}:'.format(article_id))
    if result:
        for item in result:
            print('  {id} - {name}'.format(**item))
    else:
        print('  No files.')

    print

def delete_article(article_id):
    '''article_id: str or int'''
    if article_id is int: article_id = str(article_id) 
    return issue_request('DELETE', f'account/articles/{article_id}')

def get_article_by_id(article_id):
    '''article_id: str or int'''
    if article_id is int: article_id = str(article_id) 
    return issue_request('GET', f'account/articles/{article_id}').content

def get_file_check_data(file_name, chunk_size):
    """md5 checksum and file size for a file"""
    with open(file_name, 'rb') as fin:
        md5 = hashlib.md5()
        size = 0
        data = fin.read(chunk_size)
        while data:
            size += len(data)
            md5.update(data)
            data = fin.read(chunk_size)
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
    print("File upload finished")
    # Here we should get the file

def complete_upload(article_id, file_id):
    issue_request('POST', 'account/articles/{}/files/{}'.format(article_id, file_id))

def upload_file(title, file_path):
    # We first create the article
    list_articles()
    article_id = json.loads(create_article(title).content)['entity_id']
    list_articles()
    # list_files_of_article(article_id)

    # Then we upload the file.
    file_info = json.loads(initiate_new_upload(article_id, file_path).content)
    file_id = file_info['location'].split("/")[-1]
    # Until here we used the figshare API; following lines use the figshare upload service API.
    upload_parts(file_info, file_path)
    # We return to the figshare API to complete the file upload process.
    complete_upload(article_id, file_id)
    # list_files_of_article(article_id)
def del_all_test_archives():
    ''' Here I pass a list of all archives I have created in 4TU 
    and delete them programmatically
    '''
    archive = FourTuData()

    def get_archives_list():
        resp = archive.list_my_archives()
        return json.loads(resp.content)
    
    def del_archives(archives_list):
        ''' This recursive function deletes articles in archive_list, considering that
        archives_list is a partial list. We create 20 articles to demostrate how the
        recursive deletion works
        '''
        if archives_list:    
            for item in archives_list:
                item_id = str(item['id'])
                archive.del_archive(item_id)
                del_archives(get_archives_list())
            return True
        else: 
            print("You have no archives under this account")
            return False
    
    if not get_archives_list():
        for num in range(20):
            archive.create_archive(f'My article numberv {num}')
    try: del_archives(get_archives_list())
    except HTTPError: pass
    archive.session.close()

def test_compression():
    # FIXTURESME: This should be tested for all in one test script
    archive = FourTuData()
    archive.zip_data_dir('./')
    # archive.session.close()

def test_requests():
    archive = FourTuData()
    # Check that wrong request throws HTTPError
    with pytest.raises(HTTPError):
        archive.raw_issue_request('GET','https://api.figshare.com/v2/account/articles/20021168?' )
    
    archive.session.close

def test_upload():
    archive = FourTuData()
    # Upload small file
    r = archive.create_archive('My article numberv 0')
    article_id = json.loads(r.content)['entity_id']
    r = archive.upload_file_to_archive(article_id,  f'{DUMMY_PROJECT}file_1MB.txt')
    # assert that response was succesful
    assert r.status_code == 202 
    






