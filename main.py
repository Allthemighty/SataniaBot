import random

import discord
import requests
from discord.ext import commands

import Util
from game import GameUtils as Gu
from reactions import ReactUtils as Ru
from dbconn import *

BOT = commands.Bot(command_prefix=cons.BOT_PREFIX, description=cons.DESCRIPTION)


@BOT.event
async def on_ready():
    BOT.load_extension('simple_commands')
    BOT.load_extension('reactions')
    BOT.load_extension('game')
    print("I am the Great Archdemon Satanichia, Queen of all Hell!\n")
    print("SATANIA Version: {}".format(cons.VERSION))
    print("Bot id: {} | Bot name {} | Bot tag: #{}".format(BOT.user.id, BOT.user.name, BOT.user.discriminator))
    print("Bot status: '{}' | Stream url: {}".format(cons.STATUS_PLAYING, cons.TWITCH_URL))
    if conn.status:
        print("Database connection: True\n")
    else:
        print("Database connection: False, check ASAP.\n")
    await BOT.change_presence(activity=discord.Streaming(name=cons.STATUS_PLAYING, url=cons.TWITCH_URL))


@BOT.event
async def on_message(message):
    msg = message.content
    did = message.author.id
    random_number = int(random.uniform(1, 100))
    message_chance = 25
    gif_chance = 10

    if not message.author.bot:
        if random_number <= message_chance:
            if not Gu.user_exists(did):
                Gu.user_create(did, message.author.name)
            reactions = Ru.get_reacts(msg)
            if reactions:
                if random_number <= gif_chance:
                    Gu.increment_score(did, 1)
                    Util.url_remove(reactions)
                else:
                    Util.url_remove(reactions, False)
                if reactions:
                    r = random.choice(reactions)
                    await message.channel.send(r[1])
                    Gu.increment_reaction_counter(did, 1)
                    Gu.increment_score(did, 1)
        # if bot is mentioned in a message
        elif "@386627978618077184" in msg:
            response = requests.get(url='http://api.adviceslip.com/advice')
            advice = response.json()['slip']['advice']
            await message.channel.send("Somebody asked for my assistance? Fine then, "
                                       "i'll bless you with my glorious knowledge: *{}*".format(advice))
    await BOT.process_commands(message)

BOT.run(cons.TOKEN)
