from discord.ext import commands


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
        await ctx.send(f"{fahrenheit}° Fahrenheit is {celsius}° Celsius")

    @commands.command()
    async def tof(self, ctx, temperature):
        """|Converts a temperature in Celsius to Fahrenheit. Use <prefix>toc for reverse"""
        celsius = round(float(temperature), 1)
        fahrenheit = round(((9.0 / 5.0) * celsius) + 32, 1)
        await ctx.send(f"{celsius}° Celsius is {fahrenheit}° Fahrenheit")


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
