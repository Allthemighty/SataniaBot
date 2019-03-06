import asyncio

import discord
from discord.ext import commands

from src.modules.user.user_util import *


class User:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def profile(self, ctx):
        """|Show how much reactions you triggered"""
        user = get_user(ctx.message.author.id)
        embed = discord.Embed(title=f"Profile for {user.username}",
                              description="Your stats for McDowell",
                              color=const.EMBED_COLOR)
        embed.add_field(name="Reactions triggered", value=user.reaction_count, inline=True)
        await ctx.send(embed=embed)
        await asyncio.sleep(const.DELETE_TIME)
        await ctx.message.delete()

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, page_count=1):
        """|Shows the leaderboard for McDowell statistics"""
        page_constant = 12
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count
        users = get_users_paginated(low_bound, high_bound)

        embed = discord.Embed(title="Leaderboard", color=const.EMBED_COLOR)
        for row in users:
            user, ranking = row[0], row[1]
            if user.reaction_count > 0:
                embed.add_field(name=f"#{ranking} {user.username[:20]}",
                                value=f'Reactions triggered: {user.reaction_count}',
                                inline=True)
        embed.set_footer(text=f"Page {page_count}")
        await ctx.send(embed=embed)
        await asyncio.sleep(const.DELETE_TIME)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(User(bot))
