import asyncio
import random

import discord
from discord.ext import commands

from db_connection import *
import constants as const
from util.game_util import GameUtil


class Game:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g'], hidden=True)
    @commands.is_owner()
    async def grant(self, ctx, score):
        """|Gives an user points"""
        user = ctx.message.mentions[0]
        if not user.bot:
            GameUtil.increment_score(user.id, score)
            await ctx.send("User {} has been given **{}** points.".format(user, score))
            asyncio.sleep(const.DELETE_TIME)
            await ctx.message.delete()

    @commands.command(aliases=['p'])
    async def profile(self, ctx):
        """|Check how high your IQ is"""
        user = GameUtil.user_get(ctx.message.author.id)
        embed = discord.Embed(title="Profile for {}".format(user[1]),
                              description="Look at your stats for Satania\'s IQ games", color=0xe41b71)
        embed.add_field(name="IQ", value=user[2], inline=True)
        embed.add_field(name="Reactions triggered", value=user[3], inline=True)
        await ctx.send(embed=embed)
        asyncio.sleep(const.DELETE_TIME)
        await ctx.message.delete()

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, page_count=1):
        """|Shows the leaderboard for the IQ games"""
        page_constant = 15
        low_bound = (page_count - 1) * page_constant + 1
        high_bound = page_constant * page_count
        sql = "SELECT * FROM (SELECT  *, ROW_NUMBER() OVER " \
              "(ORDER BY score DESC, dname ASC ) AS rn FROM users) q " \
              "WHERE rn BETWEEN %s and %s"
        cur = conn.cursor()
        cur.execute(sql, (low_bound, high_bound))
        rows = cur.fetchall()
        cur.close()
        response = "".join(
            [("#{}  IQ: {} | Reactions: {} | {}\n".format(row[4], row[2], row[3], row[1][:30])) if row[4] < 10
             else ("#{} IQ: {} | Reactions: {} | {}\n".format(row[4], row[2], row[3], row[1][:30])) for row in rows])
        await ctx.send("```{}\n\n\tPage {}```".format(response, page_count))
        asyncio.sleep(const.DELETE_TIME)
        await ctx.message.delete()

    @commands.command()
    async def flip(self, ctx, bet, guess):
        """|Flip a coin"""
        bet = int(bet)
        flip_arguments = ['h', 't']
        result = random.choice(flip_arguments)
        flip_full = ''
        flip_image = ''
        author = ctx.message.author.id
        balance = GameUtil.user_get(author)[2]

        if balance < bet:
            await ctx.send("You don't have enough points for that.")
        else:
            if result is 'h':
                flip_full = 'heads'
                flip_image = 'https://cdn.discordapp.com/attachments/386624118495248385/484690453594374156/sataniahead.png'
            elif result is 't':
                flip_full = 'tails'
                flip_image = 'https://cdn.discordapp.com/attachments/386624118495248385/484690459944550410/sataniatail.png'
            if guess in flip_arguments:
                if bet >= 10:
                    embed = discord.Embed(title="{} flipped {}".format(ctx.message.author.name, flip_full),
                                          color=0xe41b71)
                    embed.set_image(url=flip_image)
                    if guess is result:
                        won_points = round((bet * 1.5) - bet)
                        embed.description = "You gain {} IQ points!".format(won_points)
                        GameUtil.increment_score(author, won_points)
                    elif guess is not result:
                        embed.description = "You lost."
                        GameUtil.reduce_score(author, bet)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('Please enter a bet of at least 10.')
            else:
                await ctx.send('Please send a valid command')

    @commands.command()
    async def roll(self, ctx, bet):
        """|Roll the dice"""
        bet = int(bet)
        author = ctx.message.author.id
        balance = GameUtil.user_get(author)[2]
        r_number = int(random.uniform(1, 101))
        won_points = 0
        multipliers = [0, 0.8, 1.2, 1.5, 1.7]

        if balance < bet:
            await ctx.send("You don't have enough points for that.")
        else:
            if bet >= 10:
                embed = discord.Embed(title="You rolled a {}".format(r_number), color=0xe41b71)
                if r_number <= 20:
                    won_points = round((bet * multipliers[0]))
                elif r_number <= 50:
                    won_points = round((bet * multipliers[1]))
                elif r_number <= 70:
                    won_points = round((bet * multipliers[2]) - bet)
                elif r_number <= 90:
                    won_points = round((bet * multipliers[3]) - bet)
                elif r_number <= 100:
                    won_points = round((bet * multipliers[4]) - bet)

                if won_points < bet:
                    embed.description = "You lost {} points.".format(won_points)
                    GameUtil.reduce_score(author, won_points)
                else:
                    embed.description = "You won {} points!".format(won_points)
                    GameUtil.increment_score(author, won_points)
                await ctx.send(embed=embed)
            else:
                await ctx.send('Please enter a bet of at least 10')


def setup(bot):
    bot.add_cog(Game(bot))
