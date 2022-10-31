import discord
import os
from discord.ext import commands

from dotenv import load_dotenv

from methods import getUser_list, verificaUsuario

load_dotenv()
description = '''Jotchua - Bot é o seu mais novo bot que você vai amar ter em seu servidor, auauau caralho'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=['jot!', 'j!'],
                   description=description, intents=intents)

cogs = ["commands.rp", "commands.basic"]


def updateData(ctx):
    name = ctx.name
    display_name = ctx.display_name
    if (ctx.id != bot.user.id):
        if (getUser_list()[ctx.id].apelido.lower() != display_name.lower()):
            getUser_list()[ctx.id].apelido = display_name.lower()


@bot.event
async def on_message(message):
    # print(message.author)
    updateData(message.author)
    message.content = message.content.lower()
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    for guild in bot.guilds:
        print(guild)
        for member in guild.members:
            verificaUsuario(member)
            print(member)
    print('------')
    for cog in cogs:
        await bot.load_extension(cog)

bot.run(os.getenv('BOT_TOKEN_DEV'))
