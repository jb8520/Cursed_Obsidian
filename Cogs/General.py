import os
from datetime import datetime

from discord.ext.commands import Cog
from discord.app_commands import command
from discord import Interaction

from Utils.embed_functions import create_embed

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class General(Cog):
    def __init__(self, bot: 'MyBot'):
        self.bot = bot
        self.state = bot.state
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State
        
    

    @command(name = 'ping', description = 'Sends the latency of the bot')
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f'Latency: {round(self.bot.latency * 1000)}ms', ephemeral = True)    
    
    @command(name = 'bot-info', description = 'Shows info about the bot')
    async def botinfo(self, interaction: Interaction):
        uptime_start = self.bot.state.time
        uptime_timestamp = f'<t:{int(datetime.timestamp(uptime_start))}:R>'


        ping = f'{round(self.bot.latency * 1000)}ms'
        

        total_lines = 0
        current_dir = os.getcwd()
        skip_dirs = ['.venv', '__pycache__', '.git']

        for root, dirs, files in os.walk(current_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
        
        embed = create_embed(
            title = 'Bot Status',
            description = f'Bot Uptime: {uptime_timestamp}\nLines of code: {total_lines}\nPing: {ping}',
            colour = 0x00F3FF
        )

        await interaction.response.send_message(embed = embed, ephemeral = True)
    
    

async def setup(bot: 'MyBot'):
    await bot.add_cog(General(bot))