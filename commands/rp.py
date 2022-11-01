import discord, random
from discord.ext import commands

import sys
sys.path.insert(1, '/path/to/application/app/folder')
from methods import transacao, getid, embed_msg, user_list

@commands.command()
async def placar(ctx):
    """Exibe a lista de usuários no servidor e exibe o saldo total deles, ranqueados pelo saldo."""
    
    users=''
    sorted_list = list(user_list.values())
    sorted_list.sort(key=lambda x: x.balance, reverse=True)
    users +="\n" . join(f'**{index+1}.** {user.name} - :dollar: {user.balance + user.bank}' for index,user in enumerate(sorted_list))
    await ctx.send (embed=embed_msg( 
                                    ctx, 
                                    ctx.guild.icon.url , 
                                    ctx.guild.name,
                                    "Placar dor Milionários", 
                                    users 
                                    ))

@commands.command()
async def saldo(ctx):
    """Exibe o seu saldo atual! Quanto você tem na mão e no banco."""

    user_id = ctx.message.author.id
    user = user_list[user_id]   
    await ctx.send (embed=embed_msg(ctx ,icon_header = ctx.author.display_avatar ,title_header=ctx.author,title_content="Saldo", desc_content = user.saldo()))

@commands.command()
async def trabalhar(ctx):
    """Você sai a trabalho e recebe um salário!."""

    user_id = ctx.message.author.id
    username = ctx.message.author.name 
    work_list = {'A':random.randint(20,60) * -1,
                 'B':random.randint(20,60),
                 'C':random.randint(30,90),
                 'D':random.randint(20,30)}
    work_weight = ['C'] * 15 + ['A'] * 25 + ['B'] * 80 + ['D'] * 30 #atribui pessos as variaveis
   
    #string = f'{random.choice(worl_weight)}'
    choice = random.choice(work_weight)
    value = work_list[choice]
    emoji = ":money_with_wings:"
    resp = ""
    
    response_text = {
        'A':f"<@{user_id}> Jogou pastel no cliente e foi multado em {emoji}**{value}**",
        'B':f"<@{user_id}> Em mais um dia de trabalho arduo e ganhou {emoji}**{value}**",
        'C':f" <@{user_id}> No fim do expediente um cliente te deu gorjeta com isso ganhou {emoji}**{value}**",
        'D':f" <@{user_id}> Esqueceu de bater o ponto e recebeu apenas{emoji}**{value}**"
    }
    
    resp = response_text[choice]
    colecao = str(ctx.guild.id)
    user_list[user_id].work(colecao, value)
    await ctx.send (resp)

@commands.command()
async def saque(ctx, valor : str = None):
    """Saca o valor especificado

    uso: saque <valor | tudo>

    Argumentos:
        - valor: Um valor inteiro de dinheiro a ser sacado
        - tudo: Todo o dinheiro guardado
    """
    
    view =  await transacao(ctx,"Saque",valor)

@commands.command()
async def depositar(ctx, valor : str = None):
    """Deposita o valor especificado

    uso: depositar <valor | tudo>

    Argumentos:
        - valor: Um valor inteiro de dinheiro a ser depositado
        - tudo: Guardar todo o dinheiro
    """

    view = await transacao(ctx,"Deposito",valor)

@commands.command()
async def roubar(ctx: commands.Context, Username:str):
    
    """Você rouba um valor aleatório de algum membro, boa sorte!

    uso: roubar <apelido | nome>

    Argumentos:
        - apelido: O apelido daquele membro neste servidor
        - nome: O nome daquele usuário
    """

    ladrao = ctx.message.author
    user = getid(Username)
    if(user == None):
        await ctx.send(f':no_entry_sign:  Não da pra roubar fantasma , digite j!roubar <Usuario>')
        return

    saldo_da_vitima = user_list[user.id].getsaldo()
    if(saldo_da_vitima <= 0):
        await ctx.send (f"{user.name} Não tem 1 centavo na mao" )
        return
    
    robb_weight = [1] * 80 + [2] * 20
    robb_odds = {1:random.randint(int(saldo_da_vitima*.2),int(saldo_da_vitima*.5)),
                 2:random.randint(int(saldo_da_vitima*.2),int(saldo_da_vitima))
                }
    resp="?"
    choice = random.choice(robb_weight)
    value = robb_odds[choice]
    emoji = ":money_with_wings:"
    
    if user_list[user.id].getsaldo() > 1:
        if value > saldo_da_vitima*.80:
            resp = f"> {ladrao.name} Deu uma Rasteira em <@{user.id}> e roubou quase tudo ({emoji}{value})"
        else:
            if value < saldo_da_vitima*.80:
                resp = f"> <@{user.id}>  deixou cair ({emoji}{value}) da carteira e {ladrao.name} não deu mole "
            else:
                resp = f"> {ladrao.name} Roubou a pequena quantia de ({emoji}{value}) do <@{user.id}>"
    else:
        resp = f"> {user.name} Não tem 1 centavo na mao"
    
    colecao = str(ctx.guild.id)
    user_list[user.id].work(colecao ,value*-1)
    user_list[ladrao.id].work(colecao, value)
    
    await ctx.channel.send(resp)
    
async def setup(bot):
    # Every extension should have this function
    bot.add_command(placar)
    bot.add_command(saldo)
    bot.add_command(trabalhar)
    bot.add_command(roubar)
    bot.add_command(saque)
    bot.add_command(depositar)
    print("chamou setup")