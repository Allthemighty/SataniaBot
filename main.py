import random

import discord
from discord.ext import commands

from util.util import url_remove, get_advice
from util.game_util import *
from util.react_util import get_reacts

BOT = commands.Bot(command_prefix=const.BOT_PREFIX, description=const.DESCRIPTION)


@BOT.event
async def on_ready():
    BOT.load_extension('modules.simple_commands')
    BOT.load_extension('modules.reactions')
    BOT.load_extension('modules.game')
    print("I am the Great Archdemon Satanichia, Queen of all Hell!\n")
    print("SATANIA Version: {}".format(const.VERSION))
    print("Bot id: {} | Bot name {} | Bot tag: #{}".format
          (BOT.user.id, BOT.user.name, BOT.user.discriminator))
    print("Bot status: '{}' | Stream url: {}".format(const.STATUS_PLAYING, const.TWITCH_URL))
    await BOT.change_presence(activity=discord.Streaming(name=const.STATUS_PLAYING,
                                                         url=const.TWITCH_URL))


@BOT.event
async def on_message(message):
    msg = message.content
    did = message.author.id
    random_number = int(random.uniform(1, 100))
    message_chance = const.MESSAGE_CHANCE
    gif_chance = const.GIF_CHANCE

    if not message.author.bot:
        if random_number <= message_chance:
            if not user_exists(did):
                user_create(did, message.author.name)
            reaction_list = get_reacts(msg)
            if reaction_list:
                if random_number <= gif_chance:
                    increment_score(1)
                    url_remove(reaction_list)
                else:
                    url_remove(reaction_list, False)
                reaction = random.choice(reaction_list)
                await message.channel.send(reaction)
                increment_reaction_counter(did, 1)
                increment_score(1)
        elif const.BOT_MENTION_URL in msg:
            await message.channel.send("Somebody asked for my assistance? Fine then, "
                                       "I'll help you: *{}*".format(get_advice()))
    await BOT.process_commands(message)


BOT.run(const.TOKEN)
