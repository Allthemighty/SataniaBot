import asyncio

import discord
from discord.ext import commands
from sqlalchemy import func

from modules.user.user_util import *


class User:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def profile(self, ctx):
        """|Check how high your IQ is"""
        user = user_get(ctx.message.author.id)
        embed = discord.Embed(title=f"Profile for {user.dname}",
                              description="Your stats for Satania's wonderful shenanigans",
                              color=const.EMBED_COLOR)
        embed.add_field(name="Reactions triggered", value=user.reactions_triggered, inline=True)
        await ctx.send(embed=embed)
        await asyncio.sleep(const.DELETE_TIME)
        await ctx.message.delete()

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, page_count=1):
        """|Shows the leaderboard for Satania statistics"""
        page_constant = 12
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count
        order = (User.reactions_triggered.desc(), User.dname)

        row_number = func.row_number().over(order_by=order)
        query = session.query(User)
        query = query.add_column(row_number)
        query = query.from_self().filter(row_number.between(low_bound, high_bound))

        users = query.all()
        embed = discord.Embed(title="Leaderboard", color=const.EMBED_COLOR)
        for row in users:
            user = row[0]
            ranking = row[1]
            value_field = f"Reactions triggered: {user.reactions_triggered}"
            embed.add_field(name=f"#{ranking} {user.dname[:20]}", value=value_field, inline=True)
        embed.set_footer(text=f"Page {page_count}")
        await ctx.send(embed=embed)
        await asyncio.sleep(const.DELETE_TIME)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(User(bot))
