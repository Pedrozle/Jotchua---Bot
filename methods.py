import json
import random
import discord
import db.mongo as mongo
from discord.ui import View, Button

from classes.user import User

user_list = {}

def atualizar_lista_usuarios(nome_colecao: str):
    dados = mongo.buscar_varios_na_colecao(nome_colecao)
    print("Dados\n")
    for dado in dados:
        usuario = User(dado)
        user_list.update({usuario.getId(): usuario})



def getUser_list():
    return user_list


def verificaUsuario(user, nome_colecao:str):
    user_id = user.id
    username = user.name
    apelido = user.display_name
    if (user_id not in user_list):
        dict = {
            "id" : user_id,
            "name": username,
            "balance": 0,
            "apelido": apelido,
            "bank": 0
        }
        usuario = User(dict)
        user_list.update({user_id: usuario})
        mongo.inserir_na_colecao(nome_colecao, usuario.__dict__)


def tavazio(content):
    if (not content):
        return True
    else:
        return False


async def transacao2(ctx, tipo: str, valor: str | int = None):
    user_id = ctx.author.id
    saldo = 0
    user = user_list[user_id]
    if (tipo == "Deposito"):
        saldo = user_list[user_id].getsaldo()
    else:
        saldo = user_list[user_id].getpoup()

    if (valor == None):
        await ctx.send(f':no_entry_sign: Necessario Especificar valor 1')
        return
    else:
        if (valor.isdigit() == False and valor not in ['all', 'tudo']):
            await ctx.send(f':no_entry_sign: Necessario Especificar valor 2')
            return

    quantidade = saldo if valor in ['all', 'tudo'] else int(valor)
    if (saldo <= 0 or quantidade > saldo):
        await ctx.send(f':no_entry_sign: Você não possui **{valor}** :dollar: Para {tipo}')
        return
    view = BankView(tipo, quantidade, user_id)
    await ctx.send(f'Comfirme que deseja {tipo} {quantidade}:dollar: ', view=view)


async def transacao(ctx, tipo: str, valor: str | int = None):
    colecao = str(ctx.guild.id)
    user_id = ctx.author.id
    saldo = 0
    user = user_list[user_id]
    if (tipo == "Deposito"):
        saldo = user_list[user_id].getsaldo()
    else:
        saldo = user_list[user_id].getpoup()

    if (valor == None):
        await ctx.send(f':no_entry_sign: Necessario Especificar valor 1')
        return
    else:
        if (valor.isdigit() == False and valor not in ['all', 'tudo']):
            await ctx.send(f':no_entry_sign: Necessario Especificar valor 2')
            return

    quantidade = saldo if valor in ['all', 'tudo'] else int(valor)
    if (saldo <= 0 or quantidade > saldo):
        await ctx.send(f':no_entry_sign: Você não possui **{valor}** :dollar: Para {tipo}')
        return

    button1 = Button(label="Sim", style=discord.ButtonStyle.green, emoji='💰')
    button2 = Button(label="No", style=discord.ButtonStyle.red, emoji="🙅‍♂️")

    async def button1_action(interaction):
        if (interaction.user.id == user_id):
            if (tipo == "Deposito"):
                user_list[user_id].deposito(colecao, quantidade)
            else:
                user_list[user_id].saque(colecao, quantidade)
            await interaction.response.send_message(content=f"{tipo} Com sucesso")

    async def button2_action(interaction):
        if (interaction.user.id == user_id):
            await interaction.response.send_message(content=f"{tipo} Cancelado")

    button1.callback = button1_action
    button2.callback = button2_action

    view = View()
    view.add_item(button1)
    view.add_item(button2)

    await ctx.send(f'Comfirme que deseja {tipo} {quantidade}:dollar: ', view=view)


def getid(name):
    user = None
    for _user in user_list.values():
        if (_user.name.lower() == name.lower()):
            user = user_list[_user.id]
        else:
            if (_user.apelido.lower() == name.lower()):
                user = user_list[_user.id]
    return user


def embed_msg(ctx, icon_header: str = None, title_header: str = None, title_content: str = None, desc_content: str = None, img_content: str = None, footer: str = None):
    # color = 0x4fff4d #cor da barra lateral
    color = pick_color()
    embed_box = discord.Embed(
        title=title_content, description=desc_content, color=color)

    embed_box.set_author(name=title_header, icon_url=icon_header)
    embed_box.set_footer(text=footer)
    embed_box.set_image(url=img_content)

    return embed_box


def pick_color():
    colors = [0x4fff4d, 0x07a6eb, 0x843af2, 0xab163e,
              0xf05716, 0xf5ff33, 0x520808, 0xff00ee]
    return random.choice(colors)
