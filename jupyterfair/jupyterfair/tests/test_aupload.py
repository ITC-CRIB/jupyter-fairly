#!/usr/bin/env python
""" This module is called test_bench.py because I am using it as a main entry point
to explore and document the functionalities I am testing. It is not following at the moment
a specific architecture, or testing best practices, mostly used to do TDD,
"""
from codecs import raw_unicode_escape_decode
from http.client import BAD_REQUEST
import os
import json
import random
import time
import string
from zipapp import create_archive

import requests
from requests.exceptions import HTTPError

import asyncio
import aiohttp
import aiofiles

import pytest

# Import developed modules 
import jupyterfair.config as config
from jupyterfair.core.four_tu import *

AUTH = {'Authorization' : 'token ' + config.FOURTU_TOKEN}

BASE_URL = 'https://api.figshare.com/v2/{endpoint}'
TOKEN = config.FOURTU_TOKEN
CHUNK_SIZE = 1048576

FIXTURES = './tests/fixtures/' # FIXTUREStures path
DUMMY_PROJECT= f'./jupyterfair/jupyterfair/tests/fixtures/dummy_project/'
SMALL_FILE = 'file_1MB.txt'
MEDIUM_FILE = 'file1.txt'

def create_file(n, d, path, file_name):
    f = open(f'{path}/{file_name}', 'w')
    for i in range(n):
        nums = [str(round(random.uniform(0, 1000 * 1000), 3)) for j in range(d)]
        f.write(' '.join(nums))
        f.write('\n')
    f.close()

def check_file(chunksize, file_path):
    """md5 checksum and file size for a file"""
    with open(file_path, 'rb') as fin:
        md5 = hashlib.md5()
        size = 0
        data = fin.read(chunksize)
        while data:
            size += len(data)
            md5.update(data)
            data = fin.read(chunksize)
        return md5.hexdigest(), size 

async def raw_issue_request(session, method, url, data=None, binary=False ):
    """Issue a request to the given endpoint"""
    async with session.request(method, url, 
                            headers=AUTH) as response:
            try:
                return await response.json(content_type=None)
            except aiohttp.ContentTypeError as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise 

async def issue_request(session, method, endpoint, **kwargs):
    """Issue a request to the given endpoint"""
    return await raw_issue_request(session, method, BASE_URL.format(endpoint=endpoint), **kwargs) 

async def create_archive(session, title):
    """Creates a new article with the given title
    Returns json like this:
    {'entity_id': 20158211, 
    'location': 'https://api.figshare.com/v2/account/articles/20158211', 
    'warnings': []}
    """
    payload = { 'title': title }
    async with session.post(f'{BASE_URL.format(endpoint="")}/account/articles', 
                            headers=AUTH, json=payload) as response:
        article = await response.json()
        print ('Created article:', article['location'], '\n')
        return article

async def get_archive(session: object, id: str):
    """Returns the article with the given id"""
    async with session.get(f'{BASE_URL.format(endpoint="")}/account/articles/{id}', 
                            headers=AUTH) as response:
        if response.status == 200:
            return await response.json()
        else:
            print('Wrong id input')
            raise aiohttp.ClientError(response.status)

async def del_archive(session: object, article_id: str):
    if article_id is int: article_id = str(article_id) 
    return await issue_request(session,'DELETE', f'account/articles/{article_id}?page=&page_size=10')


async def list_my_archives(session: object):
    """Returns a list of articles in the account
    if no articles, then it returns a message that there are no articles
    """
    async with session.get(f'{BASE_URL}/account/articles', 
                            headers=AUTH) as response:
        archives_list = await response.json()
        # Transform data to standard output
        print(archives_list)

async def initiate_upload(session : object, 
                        file_path: str, archive_id: str, chunksize:int):
    """ Catches if: article already exists,
    if the file is empty, if the file is not a file
    Returns message of initiating upload of articles id and title
    """
    endpoint = f'account/articles/{archive_id}/files'
    md5, size = check_file(chunksize, file_path)

    assert size > 0, "Cannot upload empty file"
    assert os.path.isfile(file_path), "File does not exist"

    payload = {'name': os.path.basename(file_path),
            'md5': md5,
            'size': size}

    async with session.post(BASE_URL.format(endpoint=endpoint), 
                            headers=AUTH, 
                            data=json.dumps(payload)) as response:
        print(await response.json(content_type=None))
        return await response.json(content_type=None)

async def upload_part(session, upload_url, chunk, part, **kwargs):
    '''Uploads a part of the file to the given article'''
    payload = { "upload_url" : upload_url }
    payload.update(part)

    part_upload_url = '{upload_url}/{partNo}'.format(**payload)
    print(f'Part Upload Url at : {part_upload_url}')
    
    # stream.seek(part['startOffset'])
    # data = stream.read(part['endOffset'] - part['startOffset'] + 1)
    
    headers = {'Transder-Encoding' : 'chunked' }
    # print(data)
    await session.put(part_upload_url, data=chunk, headers=headers)
    # async with await session.put(part_upload_url, data=data) as response:
    #     print(response.status)
    # return await raw_issue_request(session, 'PUT', part_upload_url, 
    #                             data=data, binary=True)
async def main():
    '''Here we append the tasks to the workers queue'''
    
    tasks = []
    # sync_create_archive('My new article')
    
    async with aiohttp.ClientSession() as session:

        article = await create_archive(session, 'My new article')
        file = await initiate_upload(session, 
                                f'{DUMMY_PROJECT}/{MEDIUM_FILE}', 
                                article['entity_id'], CHUNK_SIZE)
        # Get file upload url
        file_upload_url = file['location']
        file_upload_url = await raw_issue_request(session,'GET', file_upload_url )
        file_upload_url = file_upload_url['upload_url']
        print(f'File upload url: {file_upload_url}')

        upload_parts_endpoints = await raw_issue_request(session, 'GET', file_upload_url)
        print("Uploading parts:")
        print(upload_parts_endpoints)

        async with aiofiles.open(f'{DUMMY_PROJECT}/{SMALL_FILE}', 'rb') as stream:
            for part in upload_parts_endpoints['parts']:
                chunk = await stream.read(CHUNK_SIZE)
                print(part)
                
                # Make asyncronous call for each part
                tasks.append(asyncio.ensure_future(upload_part(session, 
                                                    file_upload_url, chunk, part)))
        # Gather tasks
        await asyncio.gather(*tasks)
        await del_archive(session, article['entity_id'])

@pytest.mark.asyncio
async def test_get_archive():
    """Test if the article is correctly returned"""

    async with aiohttp.ClientSession() as session:
        new_article = await create_archive(session, 'My new article')
        article = await get_archive(session, new_article['entity_id'])
        assert article['id'] == new_article['entity_id']
        
        # Raises wrong input
        with pytest.raises(aiohttp.ClientError):
            await get_archive(session, 'aaaaa')

        # Test issue_request alternative method
        article_2 = await issue_request(session, 'GET', f'account/articles/{article["id"]}')
        assert article_2['id'] == new_article['entity_id']

        # Delete test archive after test
        await del_archive(session, article['id'])

@pytest.mark.asyncio
async def test_upload():
    """Test if the file is correctly uploaded"""
    async with aiohttp.ClientSession() as session:
        new_article = await create_archive(session, 'My new article')
        upload_location = await initiate_upload(session, 
                                f'{DUMMY_PROJECT}file_1MB.txt', 
                                new_article['entity_id'], 1048576)
        # Here we try to upload the file

        await del_archive(session, new_article['entity_id'])
        pass

# run main
if __name__ == '__main__':
    article = asyncio.run(main())