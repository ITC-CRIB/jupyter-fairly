#!/usr/bin/env python
""" This module is called test_bench.py because I am using it as a main entry point
to explore and document the functionalities I am testing. It is not following at the moment
a specific architecture, or testing best practices, mostly used to do TDD,
"""
import json
import pytest
import random
import requests
from requests.exceptions import HTTPError

from config import *

# Import developed modules 
from src.figshare import *



FIX = './tests/fixtures/' # Fixtures path

def create_file(n,d, file_name):
    f = open(f'./tests/fixtures/{file_name}', 'w')
    for i in range(n):
        nums = [str(round(random.uniform(0, 1000 * 1000), 3)) for j in range(d)]
        f.write(' '.join(nums))
        f.write('\n')
    f.close()

def test_article():
    """ Here we test the entire article creation process, including the following:
    1. Create, update and delete article
    2. Publish article
    2. Upload files to article
    """
    response = create_article('New Article') 
    response = json.loads(response.content)    
    article_id = response['entity_id']
      
    location_key_exists = 'location' in response

    # assert basic request works
    assert list_articles().status_code == 200
    # Check that location is within the response dict keys
    assert location_key_exists

    # Check that upload is initiated
    res = initiate_new_upload(article_id, f"{FIX}text.txt") 
    assert res.status_code == 201
    # Stops upload init if file is empty
    with pytest.raises(AssertionError):
        initiate_new_upload(article_id, f"{FIX}empty.txt")

    # Upload file to article
    create_file(1000,100,"small_file")
    
    # Assert that part one was uploaded
    # Assert that the entire file was uploaded

    assert os.path.exists(f"{FIX}big_file")
    os.remove(f"{FIX}big_file")
    
    # assert upload_file(article_id, f"{FIX}text.txt").status_code == 201

    # Delete created article
    delete_article(article_id)

    # assert that file is empty and not uploaded
    # Assert that file has been uploaded

def test_author_search():
    ''' We will look for an author's orcid using orcid API and use is to search
    for the author to add it to the metadata of the article is being created
    '''
    pass

def test_article_validation():
    ''' We use a technology like json schema to make sure the data is valid before creating
    the article, to make the data more FAIR from the start
    '''
    pass

    # result = raw_issue_request('GET', result['location'])
    # return result

def fairy():
    """
    Here we can test domain logic, 
    
    for example rejecting upload of empty metadata ,finding author, or generating metadata objects
    domain logic doesnt have any dependency on implementations
    """
    pass




