import discord
from discord.ext import commands

@commands.command()
async def baz(ctx):
    await ctx.send("Whatever")


async def setup(bot):
    # Every extension should have this function
    print("chamou setup")
    bot.add_command(baz)