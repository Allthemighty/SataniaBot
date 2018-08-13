from discord.ext import commands

from dbconn import *


class ReactUtils:

    def get_reacts(self):
        msg = self.lower()
        cur = conn.cursor()
        cur.execute("select * from reactions where %s like '%%' || keyword || '%%'", (msg,))
        rows = cur.fetchall()
        cur.close()
        if rows:
            return rows


class Reactions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dbping(self, ctx):
        """|Ping database."""
        await ctx.send("Conn = {}".format(conn.status))

    @commands.command()
    @commands.is_owner()
    @commands.has_permissions(administrator=True)
    async def listr(self, ctx):
        """|List all reactions."""
        sql = "SELECT * FROM reactions"
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        response = ""
        for row in rows:
            response += "ID: {} | URL: {} | KEYWORD: {}\n".format(row[0], row[1], row[2])
        await ctx.send("```{}```".format(response))

    @commands.command()
    @commands.is_owner()
    async def addr(self, ctx, url, keyword):
        """|Add a reaction."""
        sql = "INSERT INTO reactions (url, keyword) VALUES (%s, %s)"
        cur = conn.cursor()
        cur.execute(sql, (url, keyword))
        cur.close()
        await ctx.send("Reaction added")


def setup(bot):
    bot.add_cog(Reactions(bot))
