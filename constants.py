import os

from sqlalchemy.ext.declarative import declarative_base

# SECRETS
TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# MAIN
VERSION = '3.00'
TWITCH_URL = 'https://www.twitch.tv/ninjatuna6'
STATUS_PLAYING = 'So much power! Muahuahuahua'
BOT_PREFIX = '.'
DESCRIPTION = 'A silly bot for people with a low IQ.'
BOT_MENTION_URL = '@386627978618077184'
MESSAGE_CHANCE = 25
GIF_CHANCE = 10

# GAME
DELETE_TIME = 15
FLIP_IMAGE_HEADS = 'https://cdn.discordapp.com/attachments/386624118495248385/484690453594374156/sataniahead.png'
FLIP_IMAGE_TAILS = 'https://cdn.discordapp.com/attachments/386624118495248385/484690459944550410/sataniatail.png'

# SQLAlchemy
BASE = declarative_base()

