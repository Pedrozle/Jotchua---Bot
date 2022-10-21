from logging import raiseExceptions
import discord, os, random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

user_list = {}


load_dotenv()
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=['jot!','j!'], description=description, intents=intents)

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
async def test(ctx):
      await ctx.send (ctx.message.author)

class User():
    def __init__(self,userid,name):
        self.userid = userid
        self.name = name
        self.balance = 50
        
    def work(self,value):
        self.balance += value
            
    def saldo(self):
        string_formatada =(
        f'{self.name}\n'
        f':money_with_wings: : {self.balance}\n'
        f':bank: : {self.balance}'
        )
        return string_formatada   

    def getsaldo(self):
        return self.balance

@bot.command()
async def trabalhar(ctx):
    verificaUsuario(ctx.message.author) 
    user_id = ctx.message.author.id
    username = ctx.message.author.name 
    work_list = {'A':random.randint(20,60) * -1,
                 'B':random.randint(20,60),
                 'C':random.randint(30,90)}
    work_weight = ['C'] * 5 + ['A'] * 15 + ['B'] * 80 #atribui pessos as variaveis
   
    #string = f'{random.choice(worl_weight)}'
    choice = random.choice(work_weight)
    value = work_list[choice]
    emoji = ":money_with_wings:"
    resp = ""
    
    if choice == 'A':
        resp+=f"<@{user_id}> Jogou pastel no cliente e foi multado em {emoji}{value}"
    if choice == 'B':
        resp+=f"<@{user_id}> Em mais um dia de trabalho arduo e ganhou {emoji}{value}"
    if choice == 'C':
        resp+=f" <@{user_id}> No fim do expediente um cliente te deu gorjeta com isso ganhou {emoji}{value}"
        
    user_list[user_id].work(value)
    await ctx.send (resp)
                    

def verificaUsuario(user) :
    user_id = user.id
    username = user.name 
    if(user_id not in user_list):
        user_list.update({user_id:User(user_id,username)})

@bot.command()
async def saldo(ctx):
    #print(type(ctx.message.author.name))
    user_id = ctx.message.author.id
    verificaUsuario(ctx.message.author) 
    user = user_list[user_id]   
    await ctx.send (embed=embed_msg(ctx,None,user.saldo()))

@bot.command()
async def placar(ctx):
    users='>>> '
    if(len(user_list) == 0):
        ctx.send (f'Tem niguem :(')
        return
    users +="\n" . join(f'{index}. ' + str(user.name) for index,user in enumerate(user_list.values()))
    await ctx.send (users)

@bot.command()
async def roubar(ctx: commands.Context, user: discord.User = None):
    ladrao = ctx.message.author
    
    
    if(user == None):
        await ctx.send(f':no_entry_sign:  Não da pra roubar fantasma digite j!roubar <Usuario>')
    verificaUsuario(ladrao)
    verificaUsuario(user)
    
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
    
    print(f'{choice}----{value}')
    
    if user_list[user.id].getsaldo() > 1:
        print("1")
        if value > 80:
            resp = f"> {ladrao.name} Deu uma Rasteira em <@{user.id}> e roubou quase tudo ({emoji}{value})"
        else:
            if value < 15:
                resp = f"> <@{user.id}>  deixou cair ({emoji}{value}) da carteira e {ladrao.name} não deu mole "
            else:
                resp = f"> {ladrao.name} Roubou a pequena quantia de ({emoji}{value}) do <@{user.id}>"
    else:
        resp = f"> {user.name} Não tem 1 centavo na mao"
        
    user_list[user.id].work(value*-1)
    user_list[ladrao.id].work(value)
    
    await ctx.channel.send(resp)
    
def embed_msg(ctx,title,desc,color = 0x4fff4d): 
    #color = 0x4fff4d #cor da barra lateral
    author_img = ctx.message.author.display_avatar.url
    embed_box = discord.Embed(title=title, description=desc, color=color,url =author_img)
    embed_box.set_footer(text=ctx.author)
    embed_box.set_author(name=ctx.author.name,icon_url = author_img)
    return embed_box
    
@bot.command()
async def embed(ctx):
    title ="Custom Message Window Opened!"
    desc = 'Hey Bhavyadeep! I have opened the custom message window now. You can see it is visible to you now.'     
    color = 0x4fff4d #cor da barra lateral
    author_img = ctx.message.author.display_avatar.url
    
    embed_box = discord.Embed(title=title, description=desc, color=color,url =author_img)
    embed_box.set_footer(text=ctx.author)
    embed_box.set_author(name=ctx.author.name,icon_url =author_img)
    #embed_box.set_image(url = ctx.message.author.display_avatar.url)
    await ctx.channel.send(embed=embed_box)
    
@bot.command()
async def userinfo(ctx: commands.Context, user: discord.User = None):
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
    
    if(user==None):
        user = ctx.author
    
    user_id = user.id
    username = user.name
    avatar = user.display_avatar.url
    await ctx.send(f'User found: {user_id} -- {username}\n{avatar}')


bot.run(os.getenv('BOT_TOKEN'))