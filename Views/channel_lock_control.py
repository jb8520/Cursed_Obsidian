from .fleet_base import BaseFleetControlView
from discord import Interaction, ButtonStyle, VoiceChannel, PermissionOverwrite
from discord.ui import Button, button

from Utils.embed_functions import create_embed, set_embed_attr

from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class ChannelLockControlButtons(BaseFleetControlView):
    def __init__(self, bot: 'MyBot'):
        super().__init__(bot)
        self.bot = bot
        for i, emoji in enumerate(self.Circles):
            row = 1 + i // 2

            self.generate_toggle_button(
                index = i,
                emoji = emoji,
                row = row)
    


    @button(label = 'Unlock All', style = ButtonStyle.green, emoji = '🔓', custom_id = 'unlock_all', row = 0)
    async def unlock_all(self, interaction: Interaction, button: Button):
        channels = self.get_fleet_channels(interaction)
        
        for channel in channels:
            overwrites = channel.overwrites_for(interaction.guild.default_role)

            overwrites.connect = True
            overwrites.view_channel = True

            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites)

        await self.update_status(interaction, channels, '🔓 Unlocked all Fleet channels')


    @button(label = 'Lock All', style = ButtonStyle.red, emoji = '🔒', custom_id = 'lock_all', row = 0)
    async def lock_all(self, interaction: Interaction, button: Button):
        channels = self.get_fleet_channels(interaction)
        
        for channel in channels:
            overwrites = channel.overwrites_for(interaction.guild.default_role)

            overwrites.connect = False
            overwrites.view_channel = False

            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites)

        await self.update_status(interaction, channels, '🔒 Locked all Fleet channels')


    @button(label = 'Refresh', style = ButtonStyle.blurple, emoji = '🔁', custom_id = 'unlock_lock_refresh', row = 0)
    async def refresh(self, interaction:Interaction, button: Button):
        channels = self.get_fleet_channels(interaction)
        
        await self.update_status(interaction, channels, '🔁 Refreshed')
    


    def _overwrites_fetcher(self, interaction: Interaction, channel: VoiceChannel) -> PermissionOverwrite:
        return channel.overwrites_for(interaction.guild.default_role)
    

    async def update_status(self, interaction: Interaction, channels: List[VoiceChannel], footer: str):
        message = ''

        for index, channel in enumerate(channels):
            overwrites = self._overwrites_fetcher(interaction, channel)
            
            status = '🔓' if overwrites.connect else '🔒'

            message += f'{index + 1}. {channel.mention} | {status}\n'
        
        embed = create_embed(
            title = 'Fleet Voice Channel Unlock & Lock Configuration Panel',
            description = f'**Current Channel Status:**\n{message}',
            color = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': f'Latest Action: {footer}'
            }
        )

        await interaction.response.edit_message(embed = embed)
    


    def generate_toggle_button(self, index: int, emoji: str, row: int):
        async def handler(interaction: Interaction):
            await self.toggle_single(interaction, index)
        
        button = Button(
            label = 'Unlock/Lock VC',
            style = ButtonStyle.blurple,
            emoji = emoji,
            row = row,
            custom_id = f'unlock_lock_toggle_{index}'
        )
        
        button.callback = handler
        self.add_item(button)
    

    async def toggle_single(self, interaction: Interaction, index: int):
        channels = self.get_fleet_channels(interaction)
        channel = channels[index]

        circle = self.Circles[index]
        overwrites = self._overwrites_fetcher(interaction, channel)
        
        permission_state = overwrites.connect
        overwrites.connect = not permission_state
        overwrites.view_channel = not permission_state
        
        await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites)
        await self.update_status(interaction, channels, f'{circle} VC toggled')