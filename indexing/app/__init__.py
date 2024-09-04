from app.base import BaseTask, BaseMultiTask, RAW_DIR, CLENSING_DIR, STRUCTURED_DATA_DIR, TRANSFORMED_DATA_DIR, INDEXED_DATA_DIR, MENU_FILE, SITEMAP_FILE
from collections import namedtuple
from typing import List

import os
from dotenv import load_dotenv
load_dotenv()

DATA_SAVE_DIR = os.getenv('DATA_SAVE_DIR')
DATA_GITBOOK_SITE = os.getenv('DATA_GITBOOK_SITE')
DATA_SEED_URI = os.getenv('DATA_SEED_URI')
DATA_TASK = os.getenv('DATA_TASK')
DATA_TASK_MODEL = os.getenv('DATA_TASK_MODEL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODE = os.getenv('EMBEDDING_MODE')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')

Menu = namedtuple('Menu', ['title', 'url', 'include_media'])
SiteMap = namedtuple('SiteMap', ['filename', 'url', 'menu'])
StructuredSiteMap = namedtuple('StructuredSiteMap', ['filename', 'url', 'menu'])



