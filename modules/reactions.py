from discord.ext import commands
from sqlalchemy import func
import discord
import validators
from asyncio import TimeoutError

from db_connection import *
from models.reactions import Reaction


class Reactions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listr(self, ctx, page_count=1):
        """|List all reactions."""
        page_constant = 15
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count

        row_number = func.row_number().over(order_by=Reaction.reaction_id)
        query = session.query(Reaction.reaction_id, Reaction.url, Reaction.keyword)
        query = query.add_column(row_number)
        query = query.from_self().filter(row_number.between(low_bound, high_bound))

        reactions = query.all()
        embed = discord.Embed(title="Reaction list", color=const.EMBED_COLOR)
        for reaction in reactions:
            url = reaction.url if len(reaction.url) <= 20 else reaction.url[:17] + "..."
            keyword = reaction.keyword
            embed.add_field(name=f'#{reaction.iid} Keyword: {keyword}', value=f'{url}', inline=True)
        embed.set_footer(text=f'Page {page_count}')
        await ctx.send(embed=embed)

    @commands.command()
    async def showr(self, ctx, reaction_id):
        """|Show a specific reaction"""
        reaction = session.query(Reaction).filter_by(iid=reaction_id).first()
        if reaction:
            embed = discord.Embed(title='Reaction preview', color=const.EMBED_COLOR,
                                  description=f'Showing reaction with ID {reaction.iid}')
            embed.add_field(name=f"{reaction.keyword}", value=f'{reaction.url}', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Can't find a reaction with that ID")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def addr(self, ctx):
        """|Add a reaction."""
        try:
            await ctx.send('Please type the message/url you want to add')
            url = await self.bot.wait_for('message', timeout=30.0,
                                          check=lambda message: (message.author == ctx.author
                                                                 and message.channel == ctx.channel))
            react_type = 'gif' if validators.url(url.content) else 'message'
            await ctx.send('Please type the keyword on which this reaction should trigger')
            keyword = await self.bot.wait_for('message', timeout=30.0,
                                              check=lambda message: (message.author == ctx.author
                                                                     and message.channel == ctx.channel))
            reaction = Reaction(url=url.content, keyword=keyword.content, react_type=react_type)
            session.add(reaction)
            session.commit()
            await ctx.send(f'Reaction to "{keyword.content}" added')
        except TimeoutError:
            await ctx.send('No response received, aborting command.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleter(self, ctx, reaction_id):
        """|Delete a reaction."""
        session.query(Reaction).filter_by(iid=reaction_id).delete()
        session.commit()
        await ctx.send(f'Reaction #{reaction_id} deleted')


def setup(bot):
    bot.add_cog(Reactions(bot))
