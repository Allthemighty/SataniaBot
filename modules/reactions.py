from discord.ext import commands
from sqlalchemy import func

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
        page_constant = 20
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count

        row_number = func.row_number().over(order_by=Reaction.iid).label('row_number')
        query = session.query(Reaction.iid, Reaction.url, Reaction.keyword)
        query = query.add_column(row_number)
        query = query.from_self().filter(row_number.between(low_bound, high_bound))

        rows = query.all()
        response = "".join(["ID: {} | URL: {} | KEYWORD: {}\n".format(row[0], row[1][:20], row[2]) for row in rows])
        await ctx.send("```{}\n\n\tPage {}```".format(response, page_count))

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
