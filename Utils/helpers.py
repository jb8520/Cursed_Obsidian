from discord import Interaction
from discord.utils import utcnow

from .embed_functions import create_embed

from Configuration.value_types import ConfigTypes

async def send_log_message(interaction: Interaction, config: ConfigTypes, description: str):
    log_channel = interaction.guild.get_channel(config.channels.logs.bot)
    
    embed = create_embed(
        description = description,
        timestamp = utcnow()
    )

    await log_channel.send(embed = embed)