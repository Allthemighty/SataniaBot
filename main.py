import random

import discord
from discord.ext import commands

from util.util import url_remove, get_advice
from util.game_util import *
from util.react_util import get_reacts

BOT = commands.Bot(command_prefix=const.BOT_PREFIX, description=const.DESCRIPTION)


@BOT.event
async def on_ready():
    """To be executed on startup"""
    BOT.load_extension('modules.simple_commands')
    BOT.load_extension('modules.reactions')
    BOT.load_extension('modules.game')
    print("I am the Great Archdemon Satanichia, Queen of all Hell!\n")
    print(f"SATANIA Version: {const.VERSION}")
    print(f"Bot id: {BOT.user.id} | Bot name {BOT.user.name} | Bot tag: #{BOT.user.discriminator}")
    print(f"Bot status: '{const.STATUS_PLAYING}' | Stream url: {const.TWITCH_URL}")
    await BOT.change_presence(activity=discord.Streaming(name=const.STATUS_PLAYING,
                                                         url=const.TWITCH_URL))


@BOT.event
async def on_message(message):
    """This is what the bot does whenever a new message is posted"""
    author = message.author.id
    random_number = random.randint(1, 100)

    if not message.author.bot:
        if random_number <= const.MESSAGE_CHANCE:
            if not user_exists(author):
                user_create(author, message.author.name)
            reaction_list = get_reacts(message.content)
            if reaction_list:
                if random_number <= const.GIF_CHANCE:
                    increment_score(author, 1)
                    url_remove(reaction_list)
                else:
                    url_remove(reaction_list, False)
                reaction = random.choice(reaction_list)
                await message.channel.send(reaction)
                increment_reaction_counter(author, 1)
                increment_score(author, 1)
        elif const.BOT_MENTION_URL in message.content:
            await message.channel.send(f"Somebody asked for my assistance? Fine then,"
                                       f" I'll help you: *{get_advice()}*")
    await BOT.process_commands(message)


BOT.run(const.TOKEN)
