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
    async def listr(self, ctx, page_count=1):
        """|List all reactions."""
        page_constant = 20
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count
        sql = "SELECT  iid, url, keyword" \
              " FROM (SELECT  iid , url, keyword , " \
              "ROW_NUMBER() OVER (ORDER BY iid) AS rn" \
              " FROM reactions) q WHERE rn BETWEEN %s and %s"
        cur = conn.cursor()
        cur.execute(sql, (low_bound, high_bound))
        rows = cur.fetchall()
        cur.close()
        response = ""
        for row in rows:
            response += "ID: {} | URL: {} | KEYWORD: {}\n".format(row[0], row[1][:20], row[2])
        await ctx.send("```{}\n\n   Page {}```".format(response, page_count))

    @commands.command()
    @commands.is_owner()
    async def addr(self, ctx, url, keyword):
        """|Add a reaction."""
        sql = "INSERT INTO reactions (url, keyword) VALUES (%s, %s)"
        cur = conn.cursor()
        cur.execute(sql, (url, keyword))
        cur.close()
        await ctx.send("Reaction added")

    @commands.command()
    @commands.is_owner()
    async def deleter(self, ctx, reaction_id):
        """|Delete a reaction."""
        sql = "DELETE FROM reactions WHERE iid = %s"
        cur = conn.cursor()
        cur.execute(sql, (reaction_id,))
        cur.close()
        await ctx.send("Reaction deleted")


def setup(bot):
    bot.add_cog(Reactions(bot))
