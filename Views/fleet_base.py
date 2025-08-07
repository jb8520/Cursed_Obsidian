from discord.ui import View
from discord import Interaction
from discord import VoiceChannel

from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class BaseFleetControlView(View):
    def __init__(self, bot: 'MyBot'):
        super().__init__(timeout = None)
        self.bot = bot
        self.state = bot.state
        self.Circles = ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣']

    def get_fleet_num(self, interaction: Interaction) -> int:
        control_channel = interaction.channel
                
        return next((key for key, value in self.state.Fleet_State.control.items() if value == control_channel.id), None)



    def get_fleet_channels(self, interaction: Interaction) -> List[VoiceChannel]:
        fleet_num = self.get_fleet_num(interaction)
        
        vc_ids = self.state.Fleet_State.vcs[fleet_num]
        return [
            interaction.guild.get_channel(vc_ids[i]) for i in range(6)
        ]