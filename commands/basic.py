from datetime import datetime
from random import random
import discord
from discord.ext import commands
from discord.utils import get

import sys
sys.path.insert(1, '/path/to/application/app/folder')
from methods import tavazio, getid, embed_msg

@commands.command()
async def membros(ctx: commands.Context):
    """Exibe uma listagem dos membros deste servidor."""

    string_member = ""
    bot = ctx.bot
    for guild in bot.guilds:
        title_header = guild.name
        icon_header = guild.icon
        title_content = "Membros deste servidor: "
        for member in guild.members:
            string_member +=f'\n{member}'
    
    desc_content = string_member
    footer = f"Perguntado por {ctx.author}"

    await ctx.send (embed = embed_msg(ctx, icon_header=icon_header, title_header=title_header, title_content=title_content, desc_content=desc_content, footer=footer))

@commands.command()
async def info(ctx: commands.Context, username: str = None):
    """Exibe informações sobre você ou sobre um usuário especificado"""
    
    if(username==None):
        user = ctx.author
    else:
        user = getid(username)
        if(user==None):
            await ctx.send(f':no_entry_sign: Usuário não encontrado!')
            return
        bot = ctx.bot
        user = get(bot.get_all_members(), id=user.id)

    title_header = "Usuário Encontrado!"
    username = user.name
    avatar = user.display_avatar.url
    joined_at = user.joined_at.replace(tzinfo=None)
    diff = datetime.now() - joined_at
    desc = f"Entrou no servidor há {diff.days} dias!"
    footer = f"Perguntado por {ctx.author}"
    await ctx.send(embed=embed_msg(ctx, title_header=title_header, title_content=username, desc_content=desc, img_content=avatar, footer=footer))

@commands.command()
async def repetir(ctx, times: int , content='repeating...'):
    """Repete uma mensagem várias vezes. repetir <nro vezes> <mensagem>"""
    for i in range(times):
        await ctx.send(content)

@commands.command()
async def decida(ctx, *choices: str):
    """Pede ao cão para decidir entre um ou outro. decida <arg> ou <arg> ou <arg> ..."""

    if(tavazio(choices)):
        await ctx.send("Temq colocar algo ne")
        return

    choices_list = []
    frase = ""
    for c in choices:
        if c != 'ou':
            print(c)
            frase += f"{c} "
        else:
            choices_list.append(frase)
            print(frase)
            frase = ""

    choices_list.append(frase)
    
    result = "Eu escolho acho que\n"
    result = f"{result}**{random.choice(choices_list)}** "
    await ctx.send(result)

@commands.command()
async def dado(ctx, * ,dice : str = None):
    """Joga um dado dX, x vezes. dado xdX"""
    try:
        if(tavazio(dice)):raise Exception("sim")
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Formato tem que ser INTdINT!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

async def setup(bot):
    # Every extension should have this function
    
    bot.add_command(membros)
    bot.add_command(info)
    bot.add_command(repetir)
    bot.add_command(decida)
    bot.add_command(dado)
    print("chamou setup")