from asyncio import TimeoutError

import discord
import validators
from discord.ext import commands

from src.modules.misc.misc_util import simple_check
from src.modules.reaction.reaction_model import Reaction
from src.modules.reaction.reaction_util import add_reaction, delete_reaction, get_reactions_paginated
from src.modules.server.server_util import set_message_chance, set_gif_chance


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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setchance(self, ctx):
        """|Change the chance for a reaction to appear"""
        try:
            server_id = ctx.message.guild.id
            new_check = simple_check(ctx.author, ctx.channel)
            await ctx.send('Do you want to edit the chance percentage for messages or images?\n'
                           'Type **0**: to change the message percentage\n'
                           'Type **1**: to change the image percentage')
            type_prompt = await self.bot.wait_for('message', timeout=30, check=new_check)
            type_prompt = type_prompt.content
            if type_prompt not in ['0', '1']:
                await ctx.send(f'{type_prompt} is not a valid type.')

            else:
                await ctx.send('Please type the new chance percentage.')
                percentage = await self.bot.wait_for('message', timeout=30, check=new_check)
                percentage = percentage.content
                try:
                    percentage = int(percentage)
                except ValueError:
                    await ctx.send(f'{percentage} is not a valid percentage.')
                if not 0 <= percentage <= 100:
                    await ctx.send(f'{percentage} is not a valid percentage.')

                if type_prompt == '0':
                    set_message_chance(server_id, percentage)
                    await ctx.send(f'New message chance successfully set to {percentage}%')
                elif type_prompt == '1':
                    set_gif_chance(server_id, percentage)
                    await ctx.send(f'New image chance successfully set to {percentage}%')
        except TimeoutError:
            await ctx.send('No response received, aborting command.')


def setup(bot):
    bot.add_cog(Reactions(bot))
