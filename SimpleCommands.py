import discord
from discord.ext import commands
import requests


class SimpleCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """|Used to test if bot is responsive and online"""
        await ctx.send("pong")

    @commands.command()
    async def toc(self, ctx, temperature):
        """|Converts a temperature in Fahrenheit to Celsius. Use <prefix>tof for reverse"""
        fahrenheit = round(float(temperature), 1)
        celsius = round(((fahrenheit - 32) * 5.0) / 9.0, 1)
        await ctx.send('{}° Fahrenheit is {}° Celsius'.format(fahrenheit, celsius))

    @commands.command()
    async def tof(self, ctx, temperature):
        """|Converts a temperature in Celsius to Fahrenheit. Use <prefix>toc for reverse"""
        celsius = round(float(temperature), 1)
        fahrenheit = round(((9.0 / 5.0) * celsius) + 32, 1)
        await ctx.send('{}° Celsius is {}° Fahrenheit'.format(celsius, fahrenheit))

    @commands.command()
    async def summarize(self, ctx, link, length=7):
        """|Summarizes a text from an url for you, first provide the url, then
         optionally provide the amount of sentences (max is 15)"""
        host = 'https://api.smmry.com'
        path = '/&SM_API_KEY=72A5528F9D&SM_URL='
        if int(length) > 15:
            length = 15
        sum_length = '&SM_LENGTH=' + '{}'.format(length)
        merged_link = host + path + link + sum_length
        resp = requests.get(url=merged_link)
        data = resp.json()
        print(data)
        if 'sm_api_error' in data:
            error_code = data['sm_api_error']
            if error_code is 0:
                await ctx.send("Oops! Something went wrong when summarizing. Error: "
                               "Internal server problem, aka, this is not All's fault.")
            if error_code is 1:
                await ctx.send("Oops! Something went wrong when summarizing.Error: Incorrect submission variables, "
                               "did you use the command correctly?.")
            if error_code is 2:
                await ctx.send("Oops! Something went wrong when summarizing. Try again. Error: Intentional restriction."
                               " Either all the daily request are used up,  or All"
                               " needs to check his SMMRY account asap.")
            if error_code is 3:
                await ctx.send("Oops! Something went wrong when summarizing. "
                               "Error: Summarization error. {}".format(data['sm_api_message']))
        else:
            em = discord.Embed(title="Summary of  {}".format(link), description="{}"
                               .format(data['sm_api_content'].lower()), colour=discord.Colour.dark_gold())
            em.set_footer(text="Content reduced by {}".format(data['sm_api_content_reduced']))
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
