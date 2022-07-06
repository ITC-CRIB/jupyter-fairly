#!/usr/bin/env python
""" This module is called test_bench.py because I am using it as a main entry point
to explore and document the functionalities I am testing. It is not following at the moment
a specific architecture, or testing best practices, mostly used to do TDD,
"""
from codecs import raw_unicode_escape_decode
from http.client import BAD_REQUEST
from lzma import CHECK_UNKNOWN
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
import asynctest
import collections

# Import developed modules
import jupyterfair.config as config
from jupyterfair.core.four_tu import *

AUTH = {'Authorization': 'token ' + config.FOURTU_TOKEN}

BASE_URL = 'https://api.figshare.com/v2/{endpoint}'
TOKEN = config.FOURTU_TOKEN
CHUNK_SIZE = 1024

FIXTURES = './tests/fixtures/'  # FIXTUREStures path
DUMMY_PROJECT = f'./jupyterfair/jupyterfair/tests/fixtures/dummy_project/'
SMALL_FILE = 'file_1MB.txt'
MEDIUM_FILE = 'file1.txt'


def create_file(n, d, path, file_name):
    f = open(f'{path}/{file_name}', 'w')
    for i in range(n):
        nums = [str(round(random.uniform(0, 1000 * 1000), 3))
                for j in range(d)]
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


async def raw_issue_request(session, method, url, data=None, binary=False):
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
    payload = {'title': title}
    async with session.post(f'{BASE_URL.format(endpoint="")}/account/articles',
                            headers=AUTH, json=payload) as response:
        article = await response.json()
        print('Created article:', article['location'], '\n')
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
    if article_id is int:
        article_id = str(article_id)
    return await issue_request(session,
                               'DELETE', f'account/articles/{article_id}?page=&page_size=10')


async def list_my_archives(session: object):
    """Returns a list of articles in the account
    if no articles, then it returns a message that there are no articles
    """
    async with session.get(f'{BASE_URL}/account/articles',
                           headers=AUTH) as response:
        archives_list = await response.json()
        # Transform data to standard output
        print(archives_list)
        return archives_list


async def initiate_upload(session: object,
                          file_path: str, archive_id: str, chunksize: int):
    """Initiates the upload of a file to the given article
    Checks if the file is empty or is not a file
    Returns dict with information about the file upload
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

        file_upload_url = await response.json(content_type=None)
        file_info = await raw_issue_request(session, 'GET', file_upload_url['location'])
        return file_info

async def get_upload_info(session: object,
                         archive_id: str):
    endpoint = f'account/articles/{archive_id}/files'
    return await session.get(BASE_URL.format(endpoint=endpoint))


async def upload_part(session: object, upload_url: str, stream: int, part: str, **kwargs):
    '''Uploads a part of the file to the given article'''
    partNo = part['partNo']
    part_upload_url = f'{upload_url}/{partNo}'
    
    # Point to the chunk part to be uploaded
    stream.seek(part['startOffset'])
    data = await stream.read(part['endOffset'] - part['startOffset'] + 1)
    print(f"Data to upload is of type:   {type(data)}")
    print(f'Uploading part at: {part_upload_url}')

    res = await session.put(part_upload_url, data=data)
    
    if res.status == 200:
        print(f'Part {part["partNo"]} uploaded')
        return res
    else:
        print(f'Error uploading part {part}')
        raise aiohttp.ClientError(res.status)

async def upload_parts(session, file_upload_url, file_path):
    """Uploads all parts of a file to the given archive/article"""
    tasks = set()

    print(f'Upload info: {file_upload_url}' )

    # Get endpoint where we want to upload the file using figshare API upload service
    # This is a different service (different API url, endpoints, etc)
    upload_url = file_upload_url
    print(f'File upload url: {upload_url}')
    upload_parts_endpoints = await raw_issue_request(session, 'GET', upload_url)
    print("Uploading parts:")

    async with aiofiles.open(file_path, 'rb') as stream:
        for part in upload_parts_endpoints['parts']:
            # Build asyncronous coroutine for each part to be uploaded
            task = asyncio.create_task(upload_part(session,
                                                    upload_url, stream, part))
            tasks.add(task)
            # Remove references to finished tasks
            task.add_done_callback(tasks.discard)
        
        # Gather tasks
        await asyncio.gather(*tasks)

async def complete_upload(session: object, article_id: str, file_id: str):
    """Requests to finish the upload process to the server once all parts are 
    uploaded"""
    endpoint = f'account/articles/{article_id}/files/{file_id}'
    url = BASE_URL.format(endpoint=endpoint)
    res = await session.post(url)
    print(f'File upload url: {url}')
    if res.status == 200:
        print(f'Completed file upload')
    else: 
        print(f'Complete upload response failing with status: {res.status}')


async def main():
    # initiate upload
    timeout = aiohttp.ClientTimeout(total=15*60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # create article
        article = await create_archive(session, 'Test Article')
        article_id = article['entity_id']
        print(f'Article id: {article_id}')

        file_info = await initiate_upload(session,f'{DUMMY_PROJECT}{MEDIUM_FILE}',
                          article_id, CHUNK_SIZE)
        
        print(f"Print file info when initiated {file_info}")

        # print(f"File upload url: {file_upload_url}")
        await upload_parts(session, file_info['upload_url'], f'{DUMMY_PROJECT}{MEDIUM_FILE}')
        
        endpoint = f'account/articles/{article_id}/files'
        res =  await issue_request(session, 'GET', endpoint=endpoint)

        # Lets check if the parts upload is pending or completed
        res =  await raw_issue_request(session, 'GET', file_info['upload_url'] )
        
        await complete_upload(session, article_id, file_info['id'])   
        return res     


@pytest.mark.asyncio
async def test_async():
    pass


# These tests can be done for integration testing, not for unit testing
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

        # raise exception if archive doesnt exist
        with pytest.raises(aiohttp.ClientError):
            await upload_parts(session, f'{DUMMY_PROJECT}{SMALL_FILE}', '122323', chunksize=1024)

        await upload_parts(session, f'{DUMMY_PROJECT}/{SMALL_FILE}',
                          new_article['entity_id'], chunksize=1024)
        await del_archive(session, new_article['entity_id'])

        # if one of the parts is missing, the upload will fail
        # if one of the parts is missing rettry to upload that part, or task
        # if one of the upload tasks doesnt succeed then try again

    # Make a muck for upload file where upload part is mocked
    # We dont need to actually do this request but instead mock it


# run main
if __name__ == '__main__':
    article = asyncio.run(main())
