from discord import Game, Embed
from discord.ext import commands

import constants as const
from util.util import connected_to_db, change_status, get_discord_colors, get_advice


class Simple:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """|Used to test if bot is responsive and online"""
        await ctx.send("pong")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dbping(self, ctx):
        """|Ping database."""
        if connected_to_db():
            await ctx.send('Connection is responsive.')
        else:
            await ctx.send('Unknown error appeared when pinging database.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def status(self, ctx, *, activity):
        change_status(activity)
        await self.bot.change_presence(activity=Game(activity))

    @commands.command()
    async def advice(self, ctx):
        await ctx.send(
            f"You asked for my assistance? Fine then, I'll help you: *{get_advice()}*")

    @commands.command()
    async def toc(self, ctx, temperature):
        """|Converts a temperature in Fahrenheit to Celsius. Use <prefix>tof for reverse"""
        try:
            temp = float(temperature)
            fahrenheit = round(temp, 1)
            celsius = round(((fahrenheit - 32) * 5.0) / 9.0, 1)
            await ctx.send(f'{fahrenheit}° Fahrenheit is {celsius}° Celsius')
        except ValueError:
            await ctx.send(f'"{temperature}" is not a valid digit.')

    @commands.command()
    async def tof(self, ctx, temperature):
        """|Converts a temperature in Celsius to Fahrenheit. Use <prefix>toc for reverse"""
        try:
            temp = float(temperature)
            celsius = round(temp, 1)
            fahrenheit = round(((9.0 / 5.0) * celsius) + 32, 1)
            await ctx.send(f'{celsius}° Celsius is {fahrenheit}° Fahrenheit')
        except ValueError:
            await ctx.send(f'"{temperature}" is not a valid digit.')

    @commands.command()
    async def embed(self, ctx, title, description, color=None, url=None):
        """|Send a simple embed. For colors use the 'colors' command"""
        discord_colors = get_discord_colors()
        if not title or not description:
            raise commands.errors.MissingRequiredArgument
        embed = Embed(title=title, description=description)
        if color in discord_colors:
            embed.colour = discord_colors[color]
        else:
            raise commands.errors.BadArgument
        if url:
            embed.url = url
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def colors(self, ctx):
        """|List all colors that you can use in the embed command"""
        embed = Embed(title='Colors', description='Colors you can use in the embed command')
        for color in get_discord_colors():
            embed.add_field(name=color, value=const.INVISIBLE_CHAR)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        embed = Embed(color=const.EMBED_COLOR)
        embed.add_field(name='About',
                        value="Satania is a robust bot which adds custom reactions to your server. "
                              "Unlike other bots however, Satania doesn't instantly respond "
                              "whenever a keyword is mentioned, instead, this is all based on "
                              "chance. This makes sure you don't get tired of a reaction easily, "
                              "and makes it more fun by turning it into a game.")
        embed.add_field(name='Author', value='This bot is developed by All#9999')
        embed.add_field(name='Repository', value='https://bit.ly/2RjOYJk')
        embed.set_footer(text=f'Satania is running on version {const.VERSION}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Simple(bot))