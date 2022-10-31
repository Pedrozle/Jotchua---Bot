from methods import user_list
import discord
from discord.ui import View

import sys
sys.path.insert(1, '/path/to/application/app/folder')


class BankView(View):
    def __init__(self, tipo, valor, user_id):
        super().__init__(timeout=3)
        self.tipo = tipo
        self.valor = valor
        self.user_id = user_id

    @discord.ui.button(label="Sim", style=discord.ButtonStyle.green, emoji='💰', custom_id="deposit_sim")
    async def button_callback(self, button, interaction):
        for x in self.children:
            x.disabled = True

        if (interaction.user.id == self.user_id):
            if (self.tipo == "Deposito"):
                user_list[self.user_id].deposito(self.valor)
        else:
            user_list[self.user_id].saque(self.valor)

        await interaction.response.send_message(content=f"{tipo} Com sucesso")
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Nao", style=discord.ButtonStyle.red, emoji='🙅‍♂️', custom_id="deposit_no")
    async def button_callback(self, button, interaction):
        for x in self.children:
            x.disabled = True
        await interaction.response.send_message(content=f"Operacao Cancelada")
        await interaction.response.edit_message(view=self)

    async def on_timeout(self):
        self.ctx.send(f"Operacao Cancelada")
        return
