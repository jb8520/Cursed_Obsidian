from .fleet_base import BaseFleetControlView
from discord import Interaction, ButtonStyle, VoiceChannel
from discord.ui import Button, button

from Utils.embed_functions import create_embed, set_embed_attr

from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class ChannelCloseControlButtons(BaseFleetControlView):
    def __init__(self, bot: 'MyBot'):
        super().__init__(bot)
        self.bot = bot
        for i, emoji in enumerate(self.Circles):
            row = 1 + i // 2

            self.generate_toggle_button(
                index = i,
                emoji = emoji,
                row = row)
            


    @button(label = 'Open All', style = ButtonStyle.green, emoji = '🔓', custom_id = 'open_all', row = 0)
    async def open_all(self, interaction: Interaction, button: Button):
        channels = self.get_fleet_channels(interaction)
        
        for index, channel in enumerate(channels):
            await channel.edit(name = f'{self.Circles[index]}  [RB-B] /rename')
        
        await self.update_status(interaction, channels, '🔓 Opened all Fleet channels')


    @button(label = 'Close All', style = ButtonStyle.red, emoji = '🔒', custom_id = 'close_all', row = 0)
    async def close_all(self, interaction: Interaction, button: Button):
        channels = self.get_fleet_channels(interaction)
        
        for index, channel in enumerate(channels):
            await channel.edit(name = f'{self.Circles[index]}[CLOSED]')

        await self.update_status(interaction, channels, '🔒 Closed all Fleet channels')
    

    @button(label = 'Refresh', style = ButtonStyle.blurple, emoji = '🔁', custom_id = 'open_close_refresh', row = 0)
    async def refresh(self, interaction:Interaction, button: Button):
        channels = self.get_fleet_channels(interaction)
        
        await self.update_status(interaction, channels, '🔁 Refreshed')
    

    
    async def update_status(self, interaction: Interaction, channels: List[VoiceChannel], footer: str):
        message = ''

        for index, channel in enumerate(channels):
            status = 'Closed' if '[CLOSED]' in channel.name else 'Open'

            message += f'{index + 1}. {channel.mention} | {status}\n'
        
        embed = create_embed(
            title = 'Fleet Voice Channel Open & Close Configuration Panel',
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
            label = 'Open/Close VC',
            style = ButtonStyle.blurple,
            emoji = emoji,
            row = row,
            custom_id = f'open_close_toggle_{index}'
        )
        
        button.callback = handler
        self.add_item(button)
        

    async def toggle_single(self, interaction: Interaction, index: int):
        channels = self.get_fleet_channels(interaction)
        channel = channels[index]

        circle = self.Circles[index]

        if '[CLOSED]' in channel.name:
            new_name = f'{circle} [RB-B] /rename'
        
        else:
            new_name = f'{self.Circles[index]}[CLOSED]'
        
        await channel.edit(name = new_name)
        await self.update_status(interaction, channels, f'{circle} VC toggled')