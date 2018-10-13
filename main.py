import random

import discord
import requests
from discord.ext import commands

from util import util
import constants as const
from db_connection import *
from modules.game import GameUtil as Gu
from util.react_util import ReactUtil as Ru

BOT = commands.Bot(command_prefix=const.BOT_PREFIX, description=const.DESCRIPTION)


@BOT.event
async def on_ready():
    BOT.load_extension('modules.simple_commands')
    BOT.load_extension('modules.reactions')
    BOT.load_extension('modules.game')
    print("I am the Great Archdemon Satanichia, Queen of all Hell!\n")
    print("SATANIA Version: {}".format(const.VERSION))
    print("Bot id: {} | Bot name {} | Bot tag: #{}".format(BOT.user.id, BOT.user.name, BOT.user.discriminator))
    print("Bot status: '{}' | Stream url: {}".format(const.STATUS_PLAYING, const.TWITCH_URL))
    if conn.status:
        print("Database connection: True\n")
    else:
        print("Database connection: False, check ASAP.\n")
    await BOT.change_presence(activity=discord.Streaming(name=const.STATUS_PLAYING, url=const.TWITCH_URL))


@BOT.event
async def on_message(message):
    msg = message.content
    did = message.author.id
    random_number = int(random.uniform(1, 100))
    message_chance = const.MESSAGE_CHANCE
    gif_chance = const.GIF_CHANCE

    if not message.author.bot:
        if random_number <= message_chance:
            if not Gu.user_exists(did):
                Gu.user_create(did, message.author.name)
            reactions = Ru.get_reacts(msg)
            if reactions:
                if random_number <= gif_chance:
                    Gu.increment_score(did, 1)
                    util.url_remove(reactions)
                else:
                    util.url_remove(reactions, False)
                if reactions:
                    r = random.choice(reactions)
                    await message.channel.send(r[1])
                    Gu.increment_reaction_counter(did, 1)
                    Gu.increment_score(did, 1)
        # if bot is mentioned in a message
        elif const.BOT_MENTION_URL in msg:
            response = requests.get(url='http://api.adviceslip.com/advice')
            advice = response.json()['slip']['advice']
            await message.channel.send("Somebody asked for my assistance? Fine then, "
                                       "i'll bless you with my glorious knowledge: *{}*".format(advice))
    await BOT.process_commands(message)


BOT.run(const.TOKEN)
