from discord import Interaction, ButtonStyle, VoiceChannel
from discord.ui import View, Button, button

from Utils.embed_functions import create_embed, set_embed_attr


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class SpikingControlButton(View):
    def __init__(self, bot: 'MyBot'):
        super().__init__(timeout = None)
        self.bot = bot
        self.state = bot.state
        self.config = bot.config
    

    @button(label = 'Lock/Unlock VC', style = ButtonStyle.blurple, custom_id = 'Spiking_Vc_Control')
    async def spiking(self, interaction: Interaction, button: Button):
        spiking_vc = interaction.guild.get_channel(self.config.channels.fleet_queue.spiking_vc)
        member_role = interaction.guild.get_role(self.config.roles.member)

        member_permissions = spiking_vc.overwrites_for(member_role)

        if member_permissions.view_channel:
            member_permissions.view_channel = False
            status = 'Locked'
            emoji = '🔒'
        
        else:
            member_permissions.view_channel = True
            status = 'Unlocked'
            emoji = '🔓'
        
        footer = f'{emoji} {interaction.user.name} {status} the Spiking VC'

        await spiking_vc.set_permissions(member_role, overwrite = member_permissions)

        embed = create_embed(
            title = 'Spiking Vc',
            description = f'The Spiking Vc is currently: {emoji}',
            colour = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': footer
            }
        )

        await interaction.response.edit_message(embed = embed)
        

        log_channel = interaction.guild.get_channel(self.config.channels.logs.bot)
        
        embed = create_embed(
            description = f'{interaction.user.mention} `{status}` the Spiking VC'
        )

        await log_channel.send(embed = embed)