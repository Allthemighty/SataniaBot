# coding=utf-8
import logging
import sys

from discord.colour import Color
from sqlalchemy.ext.declarative import declarative_base

# MAIN
VERSION = '5.1.21'
BOT_PREFIX = ',,'
DESCRIPTION = 'The only custom reaction bot you\'ll ever need'
BOT_MENTION_URL = '@386627978618077184'
EMBED_COLOR = Color.from_rgb(253, 4, 91)

# GAME
DELETE_TIME = 15

# Reactions
INVISIBLE_CHAR = ' ̷̧̟̭̺͕̜̦̔̏̊̍ͧ͊́̚̕͞'

# SQLAlchemy
BASE = declarative_base()

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
