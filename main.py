from datetime import datetime
from logging import raiseExceptions
import discord, os, random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from discord.utils import get

from discord.ui import Button , View

user_list = {}


load_dotenv()
description = '''Jotchua - Bot é o seu mais novo bot que você vai amar ter em seu servidor, auauau caralho'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=['jot!','j!'], description=description, intents=intents)


def updateData(ctx):
    if(ctx.id != bot.user.id):
        if(user_list[ctx.id].name.lower() != ctx.name.lower()):
            user_list[ctx.id] = ctx.name.lower()
        if(user_list[ctx.id].apelido.lower() != ctx.display_name.lower()):
            user_list[ctx.id].apelido = ctx.display_name.lower()
    

@bot.event
async def on_message(message):
    #print(message.author)
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


def tavazio(content):
    if(not content):
        return True
    else:
        return False

@bot.command()
async def butao(ctx):
    button1 = Button(label="Sim",style=discord.ButtonStyle.green , emoji="💰")
    button2 = Button(label="No",style=discord.ButtonStyle.red, emoji="🙅‍♂️")
    
    async def button_action(interaction):
        await interaction.response.send_message(content="aaaa",allowed_mentions=None)
    
    button1.callback = button_action
    
    view =  View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.send("content",view=view)

@bot.command()
async def dado(ctx, * ,dice : str = None):
    """Joga um dado x vezes."""
    try:
        if(tavazio(dice)):raise Exception("sim")
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Formato tem que ser INTdINT!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def decida(ctx, *choices: str):
    """Pede ao cão para decidir entre um ou outro."""

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


@bot.command()
async def repeat(ctx, times: int , content='repeating...'):
    """Repete uma mensagem várias vezes."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Diz quando um usuário entrou no servidor"""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


class User():
    def __init__(self,userid,name,apelido):
        self.id = userid
        self.name = name
        self.balance = 0
        self.apelido = apelido
        self.bank = 0
        
    def work(self,value):
        self.balance += value
            
    def saldo(self):
        string_formatada =(
        f'{self.name}\n'
        f':money_with_wings: : {self.balance}\n'
        f':bank: : {self.bank}'
        )
        return string_formatada 
    
    def deposito(self,value):
        self.bank += value
    
    def saque(self,value):
        self.balance+=value
        self.bank-=value

    def getsaldo(self):
        return self.balance

@bot.command()
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
    
    user_list[user_id].work(value)
    await ctx.send (resp)
                    

def verificaUsuario(user):
    user_id = user.id
    username = user.name 
    apelido = user.display_name
    if(user_id not in user_list):
        user_list.update({user_id:User(user_id,username,apelido)})

@bot.command()
async def saldo(ctx):
    """Exibe o seu saldo atual! Quanto você tem na mão e no banco."""
    
    user_id = ctx.message.author.id
    user = user_list[user_id]   
    await ctx.send (embed=embed_msg(ctx,None,None,None,user.saldo()))


@bot.command()
async def placar(ctx):
    """Exibe a lista de usuários no servidor e exibe o saldo total deles, ranqueados pelo saldo."""

    a = ':first_place:' 
    emojis = [':first_place:' , ':second_place:' , ':third_place:' ]
    emojiNum = [':one:',':two:',':three:' ,':four:' ,':five:' ,':six:', ':seven:' ,':eight:', ':nine:', ':keycap_ten:' ]
    top10emojis = 'emojiNum[index] if index <= int(len(emojiNum))-1 else index+1'
    users=''
    sorted_list = list(user_list.values())
    sorted_list.sort(key=lambda x: x.balance, reverse=True)
    users +="\n" . join(f'**{index+1}.** {user.name} - :dollar: {user.balance}' for index,user in enumerate(sorted_list))
    await ctx.send (embed=embed_msg( 
                                    ctx, 
                                    ctx.guild.icon.url , 
                                    ctx.guild.name,
                                    "Placar dor Milionários", 
                                    users 
                                    ))

@bot.command()
async def membros(ctx):
    """Exibe uma listagem dos membros deste servidor."""

    string_member = ""
    for guild in bot.guilds:
        title_header = guild.name
        icon_header = guild.icon
        title_content = "Membros deste servidor: "
        for member in guild.members:
            string_member +=f'\n{member}'
    
    desc_content = string_member
    footer = f"Perguntado por {ctx.author}"

    await ctx.send (embed = embed_msg(ctx, icon_header=icon_header, title_header=title_header, title_content=title_content, desc_content=desc_content, footer=footer))

def getid(name):
    user = None
    for _user in user_list.values():
        if(_user.name.lower() == name.lower()):
            user = user_list[_user.id]
        else:
            if(_user.apelido.lower() == name.lower()):
                user = user_list[_user.id]
    return user

@bot.command()
async def roubar(ctx: commands.Context, Username:str):
    """Você rouba um valor aleatório de algum membro, boa sorte!"""

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
        
    user_list[user.id].work(value*-1)
    user_list[ladrao.id].work(value)
    
    await ctx.channel.send(resp)
    
def embed_msg(ctx, icon_header: str = None, title_header: str = None, title_content: str = None , desc_content: str = None, img_content: str = None, footer: str = None): 
    #color = 0x4fff4d #cor da barra lateral
    color = pick_color()
    embed_box = discord.Embed(title=title_content, description=desc_content, color=color)

    embed_box.set_author(name=title_header, icon_url=icon_header)
    embed_box.set_footer(text=footer)
    embed_box.set_image(url = img_content)
    
    return embed_box

def pick_color():
    colors = [0x4fff4d, 0x07a6eb, 0x843af2, 0xab163e, 0xf05716, 0xf5ff33, 0x520808, 0xff00ee]
    return random.choice(colors)
    
@bot.command()
async def embed(ctx):
    title ="Custom Message Window Opened!"
    desc = 'Hey Bhavyadeep! I have opened the custom message window now. You can see it is visible to you now.'     
    color = 0x4fff4d #cor da barra lateral
    author_img = ctx.message.author.display_avatar.url
    
    embed_box = discord.Embed(title=title, description=desc, color=color,url =author_img)
    embed_box.set_footer(text=ctx.author)
    embed_box.set_author(name=ctx.author.name,icon_url =author_img)
    embed_box.set_image(url = ctx.message.author.display_avatar.url)
    await ctx.channel.send(embed=embed_box)
    
@bot.command()
async def info(ctx: commands.Context, username: str = None):
    """Exibe informações sobre você ou sobre um usuário especificado"""
    
    if(username==None):
        user = ctx.author
    else:
        user = getid(username)
        if(user==None):
            await ctx.send(f':no_entry_sign: Usuário não encontrado!')
            return
        user = get(bot.get_all_members(), id=user.id)

    title_header = "Usuário Encontrado!"
    username = user.name
    avatar = user.display_avatar.url
    joined_at = user.joined_at.replace(tzinfo=None)
    diff = datetime.now() - joined_at
    desc = f"Entrou no servidor há {diff.days} dias!"
    footer = f"Perguntado por {ctx.author}"
    await ctx.send(embed=embed_msg(ctx, title_header=title_header, title_content=username, desc_content=desc, img_content=avatar, footer=footer))

bot.run(os.getenv('BOT_TOKEN'))