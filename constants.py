import logging
import os
import sys

from discord.colour import Color
from sqlalchemy.ext.declarative import declarative_base

# SECRETS
TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# MAIN
VERSION = '4.1.5'
BOT_PREFIX = '.'
DESCRIPTION = 'Witty reactions, and gimmicky functions, Satania has it all!'
BOT_MENTION_URL = '@386627978618077184'
MESSAGE_CHANCE = 25
GIF_CHANCE = 10

# GAME
EMBED_COLOR_GAME = Color.from_rgb(253, 4, 91)
DELETE_TIME = 15

# Reactions
EMBED_COLOR_REACTIONS = Color.from_rgb(255, 255, 0)
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
