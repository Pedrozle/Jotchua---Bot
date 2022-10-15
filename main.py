import discord, os, random
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

id_do_servidor = os.getenv('ID_SERVIDOR')

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #Checar se os comandos slash foram sincronizados 
            await tree.sync(guild = discord.Object(id=id_do_servidor)) # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True
        print(f"Entramos como {self.user}.")

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'late', description='Pede pro cão latir') #Comando específico para seu servidor
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"AUAUAU caralho", ephemeral = False)


@tree.command(guild = discord.Object(id=id_do_servidor), name = 'dado', description='Pede pro cão rolar um dado') #Comando específico para seu servidor
async def dado(interaction: discord.Interaction):
    numero = random.randint(1, 6)
    await interaction.response.send_message(f"o cão conseguiu tirar um {numero}", ephemeral = False) 

aclient.run(os.getenv('BOT_TOKEN'))