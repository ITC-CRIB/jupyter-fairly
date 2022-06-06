import os
from dotenv import load_dotenv

load_dotenv('./.env')

# TODO: Fix this later 
load_dotenv('./.env.dev')


FOURTU_TOKEN = os.environ['FOURTU_TOKEN']
ZENODO_TOKEN = os.environ['ZENODO_TOKEN']
# BASE_URL = os.environ['BASE_URL']

# Dev environment variables
# ARTICLE_ID = os.environ['ARTICLE_ID']
CHUNK_SIZE = 1048576
