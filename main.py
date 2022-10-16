from logging import raiseExceptions
import discord, os, random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='jot!', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


def tavazio(content):
    if(not content):
        return True
    else:
        return False

@bot.command()
async def dado(ctx, * ,dice : str = None):
    """Rolls a dice in NdN format."""
    try:
        if(tavazio(dice)):raise Exception("sim")
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Formato tem que ser INTdINT!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='Pede ao cão para decidir entre um ou outro')
async def decida(ctx, *choices: str):
    
    if(tavazio(choices)):
        await ctx.send("Temq colocar algo ne")
        return
    
    choices_list = list(choices)
    for choice in choices_list:
        if choice == "ou":choices_list.remove(choice)

    """Chooses between multiple choices."""
    result = "Eu escolho acho que"
    result = f"{result} {random.choice(choices_list)}"
    await ctx.send(result)


@bot.command()
async def repeat(ctx, times: int , content='repeating...'):
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


    
@bot.command()
async def userinfo(ctx: commands.Context, user: discord.User):
    # In the command signature above, you can see that the `user`
    # parameter is typehinted to `discord.User`. This means that
    # during command invocation we will attempt to convert
    # the value passed as `user` to a `discord.User` instance.
    # The documentation notes what can be converted, in the case of `discord.User`
    # you pass an ID, mention or username (discrim optional)
    # E.g. 80088516616269824, @Danny or Danny#0007

    # NOTE: typehinting acts as a converter within the `commands` framework only.
    # In standard Python, it is use for documentation and IDE assistance purposes.

    # If the conversion is successful, we will have a `discord.User` instance
    # and can do the following:
    user_id = user.id
    username = user.name
    avatar = user.display_avatar.url
    await ctx.send(f'User found: {user_id} -- {username}\n{avatar}')


bot.run(os.getenv('BOT_TOKEN'))