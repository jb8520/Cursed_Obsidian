from discord.ext.commands import Cog
from discord.app_commands import command
from discord import Interaction

from Utils.embed_functions import create_embed, set_embed_attr
from Utils.command_decorators import app_command_requires_role_of_perm_tiers

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class Commands(Cog):
    def __init__(self, bot: 'MyBot'):
        self.bot = bot
        self.state = bot.state
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State
    
    @command(name = 'goldrush', description = 'A command that shows when the next Goldrush hour will be')
    @app_command_requires_role_of_perm_tiers()
    async def goldrush(self, interaction: Interaction):
        embed = create_embed(
            title = 'Goldrush Hours',
            description = 'Hours for Goldrush (shown for your timezone)\n\n**<t:2563290000:t>-<t:2563293600:t>** and **<t:2563318800:t>-<t:2563322400:t>**',
            colour = 0xffd700
        )
        embed = set_embed_attr(
            embed = embed,
            image_url = 'https://media1.giphy.com/media/2LnaiD9MmlVeCkDPYz/giphy.gif?cid=ecf05e470v7xhzbtv0zjdodc29mrc91naz8ff8bi5yxg4ncf&rid=giphy.gif&ct=g'
        )

        await interaction.response.send_message(embed = embed)
    
    
    @command(name = 'spike',description = 'Sends a message about when the next fleet/spike will be')
    @app_command_requires_role_of_perm_tiers()
    async def spike(self, interaction: Interaction):
        embed = create_embed(
            description = 'A staff member will ping when they are able to spike and host a server. If you want to be notified of server spikes, grab the `@Spiking` or `@Alliance Ping` role from <#984437310756118528>. Also, please read the <#974661594015481896> If you haven\'t already done so. Thanks.',
            colour = 0x00F3FF
        )

        await interaction.response.send_message(embed = embed, ephemeral = True)
    
    
    
async def setup(bot: 'MyBot'):
    await bot.add_cog(Commands(bot))