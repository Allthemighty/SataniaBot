import discord
from discord.ext import commands
from dbconn import *


class Reactions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def dbping(self, ctx):
        """|Ping database."""
        await ctx.send("Conn = {}".format(conn.status))

    @commands.command()
    @commands.is_owner()
    async def reactlist(self, ctx):
        """|List all reactions."""
        sql = "SELECT * FROM reactions"
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        response = ""
        for row in rows:
            response += "ID: {} | URL: {} | KEYWORD: {}\n".format(row[0], row[1], row[2])
        await ctx.send(response)


def setup(bot):
    bot.add_cog(Reactions(bot))
