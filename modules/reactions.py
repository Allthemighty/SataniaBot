from discord.ext import commands
from sqlalchemy import func
import discord

from db_connection import *
from models.reactions import Reaction


class Reactions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dbping(self, ctx):
        """|Ping database."""
        try:
            session.query(Reaction).all()
            await ctx.send('Connection is responsive.')
        except:
            await ctx.send('Unknown error appeared when pinging database.')

    @commands.command()
    async def listr(self, ctx, page_count=1):
        """|List all reactions."""
        page_constant = 15
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count

        row_number = func.row_number().over(order_by=Reaction.iid)
        query = session.query(Reaction.iid, Reaction.url, Reaction.keyword)
        query = query.add_column(row_number)
        query = query.from_self().filter(row_number.between(low_bound, high_bound))

        reactions = query.all()
        embed = discord.Embed(title="Reaction list", color=const.EMBED_COLOR_REACTIONS)
        for react in reactions:
            reaction_id = react.iid
            url = react.url if len(react.url) <= 20 else react.url[:17] + "..."
            keyword = react.keyword
            embed.add_field(name=f"#{reaction_id} KW: {keyword}",
                            value=f"{url}", inline=True)
        embed.set_footer(text=f"Page {page_count}")
        await ctx.send(embed=embed)

    @commands.command()
    async def showr(self, ctx, reaction_id):
        """|Show a specific reaction"""
        reaction = session.query(Reaction).filter_by(iid=reaction_id).first()
        if reaction:
            embed = discord.Embed(title="Reaction preview", color=const.EMBED_COLOR_REACTIONS,
                                  description=f"Showing reaction with ID {reaction.iid}")
            embed.add_field(name=f"{reaction.keyword}", value=f"{reaction.url}", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Can't find a reaction with that ID")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def addr(self, ctx, url, keyword):
        """|Add a reaction."""
        reaction = Reaction(url=url, keyword=keyword)
        session.add(reaction)
        session.commit()
        await ctx.send("Reaction added")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleter(self, ctx, reaction_id):
        """|Delete a reaction."""
        session.query(Reaction).filter_by(iid=reaction_id).delete()
        session.commit()
        await ctx.send("Reaction deleted")


def setup(bot):
    bot.add_cog(Reactions(bot))
