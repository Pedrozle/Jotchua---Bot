import discord
from discord.ext import commands
import random

class economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bot.command()
    async def trabalhar(ctx):
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

    @bot.command()
    async def saldo(ctx):
        #print(type(ctx.message.author.name))
        user_id = ctx.message.author.id
        user = user_list[user_id]   
        await ctx.send (embed=embed_msg(ctx ,icon_header = ctx.author.display_avatar ,title_header=ctx.author,title_content="Saldo", desc_content = user.saldo()))
        
        @commands.command()
        async def transacao(ctx,tipo : str, valor):
            user_id = ctx.author.id
            print(user_list.items())
            saldo = 0 
            user = user_list[user_id]
            if(tipo == "Deposito"):
                saldo = user_list[user_id].getsaldo()
            else:
                saldo = user_list[user_id].getpoup()
            if(valor == None):
                await ctx.send(f':no_entry_sign: Necessario Especificar valor')
                return
            if(saldo <= 0 or valor > saldo ):
                await ctx.send(f':no_entry_sign: Necessario Especificar valor valido ')
                return
            
            button1 = Button(label="Sim",style=discord.ButtonStyle.green , emoji='💰')
            button2 = Button(label="No",style=discord.ButtonStyle.red, emoji="🙅‍♂️")
            
            async def button1_action(interaction):
                if(valor=='all' or int(valor) > 0):
                    if(tipo == "Deposito"):
                        user_list[user_id].depositar(int(valor))
                    else:
                        user_list[user_id].saque(int(valor))
                await interaction.response.send_message(content="{tipo} Com sucesso",allowed_mentions=None)
            async def button2_action(interaction):
                await interaction.response.send_message(content="{tipo} Cancelado",allowed_mentions=None)
            
            button1.callback = button1_action
            button2.callback = button2_action
            
            view =  View()
            view.add_item(button1)
            view.add_item(button2)
            
            await ctx.send(view=view)
    

def setup(bot):
    bot.add_cog(rpbase(bot))    