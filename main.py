import random
import traceback

from discord import Game, Embed
from discord.ext import commands

import constants as const
from util.react_util import get_reacts
from util.user_util import user_exists, user_create, increment_reaction_counter
from util.util import get_status, get_servers, add_server

BOT = commands.Bot(command_prefix=const.BOT_PREFIX, description=const.DESCRIPTION)
logger = const.logger


@BOT.event
async def on_ready():
    """To be executed on startup"""

    # Initialize servers #
    connected_servers = BOT.guilds
    db_servers = get_servers()
    for server in connected_servers:
        if server.id not in [server.server_id for server in db_servers]:
            add_server(server.id, server.name)
    logger.info(f'Servers initialized')

    # Load extensions #
    BOT.load_extension('modules.simple')
    BOT.load_extension('modules.reaction')
    BOT.load_extension('modules.user')
    logger.info(f'Extensions loaded')

    # Bot information #
    logger.info(f'Bot id: {BOT.user.id} | '
                f'Bot name: {BOT.user.name}#{BOT.user.discriminator} | '
                f'Bot version: {const.VERSION} | '
                f'Bot status: {get_status()}')
    await BOT.change_presence(activity=Game(get_status()))


@BOT.event
async def on_message(message):
    """This is what the bot does whenever a new message is posted"""
    author = message.author.id
    random_number = random.randint(1, 100)
    content = message.content
    server_id = message.guild.id

    if not message.author.bot:
        if const.BOT_MENTION_URL in content:
            await message.channel.send(
                f"To use Satania, type **{const.BOT_PREFIX}help** for a list of commands")
        elif random_number <= const.MESSAGE_CHANCE:
            if not user_exists(author):
                user_create(author, message.author.name)
            if random_number <= const.GIF_CHANCE:
                reaction_list = get_reacts(content, server_id, 'gif')
            else:
                reaction_list = get_reacts(content, server_id, 'message')
            if reaction_list:
                reaction = random.choice(reaction_list)
                await message.channel.send(reaction)
                increment_reaction_counter(author, 1)
    await BOT.process_commands(message)


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument) or \
            isinstance(error, commands.errors.BadArgument):
        name = ctx.author.display_name
        embed = Embed(title='Command error')
        embed.add_field(name=f'{name}, this is not the right way to use this command',
                        value=f'**Command usage:** {ctx.prefix}{ctx.command.signature}')
        await ctx.send(embed=embed)


@BOT.event
async def on_error(event, *args):
    message = args[0]
    logger.error(f'Error in message: {message.content}\nEvent: {event}\n{traceback.format_exc()}')


BOT.run(const.TOKEN)
