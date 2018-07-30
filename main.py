import discord
import random
import requests
from discord.ext import commands
from dbconn import *
import os

version = '2.3'
bot = commands.Bot(command_prefix=".", description="A silly bot for people with a low IQ.")
twitch_url = "https://www.twitch.tv/ninjatuna6"
status_playing = "Playing with myself"


@bot.event
async def on_ready():
    bot.load_extension('SimpleCommands')
    print("Back in action baby! SATANIA VERSION {}".format(version))
    print("Logged in as: {}||{}#{}".format(bot.user.id, bot.user.name, bot.user.discriminator))
    print("Status loaded as: |{}| and streaming this url {}".format(status_playing, twitch_url))
    print(conn.status)
    await bot.change_presence(activity=discord.Streaming(name=status_playing, url=twitch_url))


@bot.event
async def on_message(message):
    msg = message.content
    random_number = int(random.uniform(1, 100))
    nou = ['no u', 'No u', 'NO U', 'no U']
    uwu = ['uwu', 'UWU', 'uwU', 'Uwu', 'UwU']
    owo = ['owo', 'OWO', 'owO', 'Owo', 'OwO']
    if msg in nou:
        if random_number < 30:
            await message.channel.send('**no u**')
        if random_number > 89:
            await message.channel.send(file=discord.File('nou.gif', filename='nou.gif'))
    if msg in owo:
        if random_number < 30:
            await message.channel.send(file=discord.File('owo.gif', filename='owo.gif'))
    if msg in uwu:
        if random_number < 40:
            await message.channel.send(file=discord.File('uwu.gif', filename='uwu.gif'))
        if "@386627978618077184" in msg:
            if random_number < 60:
                url = '	http://api.adviceslip.com/advice'
                response = requests.get(url=url)
                data = response.json()
                advice = data['slip']['advice']
                await message.channel.send("Somebody asked for my assistance? Fine then, "
                                           "i'll bless you with my glorious knowledge: *{}*".format(advice))

    await bot.process_commands(message)


bot.run(os.getenv('TOKEN'))
