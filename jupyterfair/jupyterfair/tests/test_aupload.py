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

import aiohttp
import asyncio

import pytest

# Import developed modules 
import jupyterfair.config as config
from jupyterfair.core.four_tu import *

AUTH = {'Authorization' : 'token ' + config.FOURTU_TOKEN}

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

async def raw_issue_request(session, method, url):
    """Issue a request to the given endpoint"""
    async with session.request(method, url, 
                            headers=AUTH) as response:
            return await response.json(content_type=None)
            

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
    data = { 'title': title }
    async with session.post(f'{BASE_URL.format(endpoint="")}/account/articles', 
                            headers=AUTH, json=data) as response:
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

async def del_archive(session, article_id):
    if article_id is int: article_id = str(article_id) 
    return await issue_request(session,'DELETE', f'account/articles/{article_id}?page=&page_size=10')


async def list_my_archives(session):
    """Returns a list of articles in the account
    if no articles, then it returns a message that there are no articles
    """
    async with session.get(f'{BASE_URL}/account/articles', 
                            headers=AUTH) as response:
        archives_list = await response.json()
        # Transform data to standard output
        print(archives_list)

async def initiate_upload(session : object, file_path: str, archive_id: str):
    """ Catches if: article already exists,
    if the file is empty, if the file is not a file
    Returns message of initiating upload of articles id and title
    """
    endpoint = f'account/articles/{archive_id}/files'
    md5, size = check_file(file_path)

    try:
        assert size > 0, "Cannot upload empty file"
        assert os.path.isfile(file_path), "File does not exist"
    except HTTPError as e:
        print(e)
        return None

    data = {'name': os.path.basename(file_path),
            'md5': md5,
            'size': size}

    async with session.post(f'{BASE_URL}{endpoint}', 
                            headers=AUTH, 
                            data=json.dumps(data)) as response:
        print(await response.json())
        return await response.json()

async def main():
    '''Here we append the tasks to the workers queue'''
    
    tasks = []
    # sync_create_archive('My new article')
    
    async with aiohttp.ClientSession() as session:
        # Get article
        # value = await get_archive(session, '20158211')
        # value = await get_archive(session, 'aaa')

        # Test generic issue request functionality
        value = await issue_request(session, 'GET', 'account/articles/20158211')
        #         
        # tasks.append(asyncio.create_task(list_my_archives(session)))
        # tasks.append(asyncio.create_task(create_archive(session, 'My new article')))
        # await asyncio.gather(*tasks) 
        await del_archive(session, '20158211')
        return value

@pytest.mark.asyncio
async def test_get_archive():
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

        await del_archive(session, article['id'])

        


# run main
if __name__ == '__main__':
    article = asyncio.run(main())



