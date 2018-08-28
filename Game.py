import discord
from discord.ext import commands

from dbconn import *


class GameUtils:

    def user_exists(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE did = %s ", (self,))
        row = cur.fetchone()
        cur.close()
        if row:
            return True
        else:
            return False

    def user_get(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE did = %s ", (self,))
        row = cur.fetchone()
        cur.close()
        return row

    def user_create(self, discord_name, score=0, reactions_triggered=0):
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (self, discord_name, score, reactions_triggered))
        print("Posted user to DB | {}: {}".format(self, discord_name))
        cur.close()

    def increment_score(self, score):
        cur = conn.cursor()
        cur.execute("UPDATE users SET score = score + %s WHERE did = %s", (score, self))
        print("Incremented score by {}| {}".format(score, self))
        cur.close()


class Game:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx):
        """|Check how high your IQ is"""
        did = ctx.message.author.id
        user = GameUtils.user_get(did)
        embed = discord.Embed(title="Profile for {}".format(user[1]),
                              description="Look at your stats for Satania\'s IQGame", color=0xd309ea)
        embed.add_field(name="Score", value=user[2], inline=True)
        embed.add_field(name="Reactions triggered", value=user[3], inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Game(bot))
