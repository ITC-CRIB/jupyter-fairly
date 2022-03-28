import os
from dotenv import load_dotenv

load_dotenv('../.env')

TOKEN = os.getenv('TOKEN')

BASE_URL = 'https://api.figshare.com/v2/{endpoint}'

# ARTICLE_ID = 
CHUNK_SIZE = 1048576
