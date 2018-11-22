import os

from discord.colour import Color
from sqlalchemy.ext.declarative import declarative_base

# SECRETS
TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# MAIN
VERSION = '3.1.7'
BOT_PREFIX = '.'
DESCRIPTION = 'Witty reactions, and gimmicky functions, Satania has it all!'
BOT_MENTION_URL = '@386627978618077184'
MESSAGE_CHANCE = 25
GIF_CHANCE = 10

# GAME
EMBED_COLOR_GAME = Color.from_rgb(253, 4, 91)
DELETE_TIME = 15
FLIP_IMAGE_HEADS = 'https://cdn.discordapp.com/attachments/386624118495248385/484690453594374156/sataniahead.png'
FLIP_IMAGE_TAILS = 'https://cdn.discordapp.com/attachments/386624118495248385/484690459944550410/sataniatail.png'

# Reactions
EMBED_COLOR_REACTIONS = Color.from_rgb(255, 255, 0)

# SQLAlchemy
BASE = declarative_base()

