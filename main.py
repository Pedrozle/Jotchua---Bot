import discord, os, random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# id_do_servidor = os.getenv('ID_SERVIDOR')
# intents = discord.Intents.default()

# bot = commands.Bot(command_prefix='jotchua', intents=intents)
# class client(discord.Client):
#     def __init__(self):
#         super().__init__(intents=discord.Intents.default())
#         self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

#     async def on_ready(self):
#         await self.wait_until_ready()
#         if not self.synced: #Checar se os comandos slash foram sincronizados 
#             await tree.sync(guild = discord.Object(id=id_do_servidor)) # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
#             self.synced = True
#         print(f"Entramos como {self.user}.")

# aclient = client()
# tree = app_commands.CommandTree(aclient)

# @tree.command(guild = discord.Object(id=id_do_servidor), name = 'late', description='Pede pro cão latir') #Comando específico para seu servidor
# async def slash2(interaction: discord.Interaction):
#     await interaction.response.send_message(f"AUAUAU caralho", ephemeral = False)


# @tree.command(guild = discord.Object(id=id_do_servidor), name = 'dado', description='Pede pro cão rolar um dado') #Comando específico para seu servidor
# async def dado(interaction: discord.Interaction):
#     numero = random.randint(1, 6)
#     await interaction.response.send_message(f"o cão conseguiu tirar um {numero}", ephemeral = False) 

# aclient.run(os.getenv('BOT_TOKEN'))

# This example requires the 'members' and 'message_content' privileged intents to function.

# import discord
# from discord.ext import commands
# import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='jotchua ', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command(description="Pede ao cão para decidir entre um ou outro")
async def decide(ctx, left: str, right: str):
    result = "Eu escolho acho que "
    if random.randint(0, 1) == 1:
        result = f'{result} {left}'
    else:
        result = f'{result} {right}'
    await ctx.send(result)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run(os.getenv('BOT_TOKEN'))