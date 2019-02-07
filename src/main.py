import random

from discord import Game, Embed
from discord.ext import commands

import src.constants as const
from src.modules.misc.misc_util import get_status
from src.modules.reaction.reaction_util import get_matching_reactions
from src.modules.server.server_util import get_server, refresh_servers, add_server, remove_server
from src.modules.user.user_util import user_exists, create_user, increment_reaction_counter
from src.secrets import TOKEN

BOT = commands.Bot(command_prefix=const.BOT_PREFIX, description=const.DESCRIPTION)
logger = const.logger


@BOT.event
async def on_ready():
    """To be executed on startup"""
    try:
        # Initialize servers #
        connected_servers = BOT.guilds
        refresh_servers(connected_servers)
        logger.info(f'Servers initialized')

        # Load extensions #
        BOT.load_extension('modules.simple.simple_commands')
        BOT.load_extension('modules.reaction.reaction_commands')
        BOT.load_extension('modules.user.user_commands')
        logger.info(f'Extensions loaded')

        # Bot information #
        logger.info(f'Bot id: {BOT.user.id} | '
                    f'Bot name: {BOT.user.name}#{BOT.user.discriminator} | '
                    f'Bot version: {const.VERSION} | '
                    f'Bot status: {get_status()}')
        await BOT.change_presence(activity=Game(get_status()))
    except:
        logger.exception('Unable to complete starting sequence', exc_info=True)


@BOT.event
async def on_guild_join(guild):
    """Add server to database on server join"""
    add_server(guild.id, guild.name)


@BOT.event
async def on_guild_remove(guild):
    """Remove server from database on server leave"""
    remove_server(guild.id)


@BOT.event
async def on_message(message):
    """Main reaction management logic"""
    author = message.author.id
    random_number = random.randint(1, 100)
    content = message.content
    server_id = message.guild.id

    if not message.author.bot:
        server = get_server(server_id)
        if const.BOT_MENTION_URL in content:
            await message.channel.send(
                f"To use McDowell, type **{const.BOT_PREFIX}help** for a list of commands")
        elif random_number <= server.message_chance:
            if not user_exists(author):
                create_user(author, message.author.name)
            if random_number <= server.gif_chance:
                reaction_list = get_matching_reactions(content, server_id, 'gif')
            else:
                reaction_list = get_matching_reactions(content, server_id, 'message')
            if reaction_list:
                reaction = random.choice(reaction_list)
                await message.channel.send(reaction)
                increment_reaction_counter(author, 1)
    await BOT.process_commands(message)


@BOT.event
async def on_command_error(ctx, error):
    """Correct user when a command is not activated the right way"""
    if isinstance(error, commands.errors.MissingRequiredArgument) or \
            isinstance(error, commands.errors.BadArgument):
        name = ctx.author.display_name
        embed = Embed(title='Command error')
        embed.add_field(name=f'{name}, this is not the right way to use this command',
                        value=f'**Command usage:** {ctx.prefix}{ctx.command.signature}')
        await ctx.send(embed=embed)


@BOT.event
async def on_error(event, *args):
    """Log specific message plus stracktrace that produces an error"""
    message = args[0]
    logger.error(f'Error in message: {message.content}\nEvent: {event}', exc_info=True)


BOT.run(TOKEN)
