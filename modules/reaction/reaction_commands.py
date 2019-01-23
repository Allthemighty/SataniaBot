from asyncio import TimeoutError

import discord
import validators
from discord.ext import commands

from db_connection import *
from modules.misc.misc_util import simple_check
from modules.reaction.reaction_model import Reaction
from modules.reaction.reaction_util import add_reaction, delete_reaction, get_reactions_paginated


class Reactions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listr(self, ctx, page_count=1):
        """|List all reactions."""
        server_id = ctx.message.guild.id
        page_constant = 15
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count

        reactions = get_reactions_paginated(low_bound, high_bound, server_id)
        if reactions:
            embed = discord.Embed(title="Reaction list", color=const.EMBED_COLOR)
            for reaction in reactions:
                url = reaction.url if len(reaction.url) <= 20 else reaction.url[:17] + "..."
                keyword = reaction.keyword
                embed.add_field(name=f'#{reaction.reaction_id} Keyword: {keyword}',
                                value=f'{url}',
                                inline=True)
            embed.set_footer(text=f'Page {page_count}')
            await ctx.send(embed=embed)
        else:
            await ctx.send('No reactions found in this server.')

    @commands.command()
    async def showr(self, ctx, reaction_id):
        """|Show a specific reaction"""
        server_id = ctx.message.guild.id
        reaction = session.query(Reaction).filter_by(reaction_id=reaction_id,
                                                     from_server=server_id).first()
        if reaction:
            embed = discord.Embed(title='Reaction preview', color=const.EMBED_COLOR,
                                  description=f'Showing reaction with ID {reaction.reaction_id}')
            embed.add_field(name=f"{reaction.keyword}", value=f'{reaction.url}', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Can't find a reaction with that ID")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addr(self, ctx):
        """|Add a reaction."""
        try:
            new_check = simple_check(ctx.author, ctx.channel)
            server_id = ctx.message.guild.id

            await ctx.send('Please type the message/url you want to add')
            url = await self.bot.wait_for('message', timeout=30.0, check=new_check)
            react_type = 'gif' if validators.url(url.content) else 'message'

            await ctx.send('Please type the keyword on which this reaction should trigger')
            keyword = await self.bot.wait_for('message', timeout=30.0, check=new_check)

            add_reaction(url=url.content,
                         keyword=keyword.content,
                         react_type=react_type,
                         server_id=server_id)
            await ctx.send(f'Reaction to "{keyword.content}" added')
        except TimeoutError:
            await ctx.send('No response received, aborting command.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deleter(self, ctx, reaction_id):
        """|Delete a reaction."""
        delete_reaction(reaction_id)
        await ctx.send(f'Reaction #{reaction_id} deleted')


def setup(bot):
    bot.add_cog(Reactions(bot))
