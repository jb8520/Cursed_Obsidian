from discord import ButtonStyle, Interaction, Role
from discord.ui import View, Button, button

from Utils.embed_functions import create_embed, set_embed_attr

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class DutySwitchButtons(View):
    def __init__(self, bot: 'MyBot'):
        super().__init__(timeout = None)
        self.bot = bot
        self.config = bot.config
    
    
    def _on_duty_embed_message(self, on_duty_role: Role) -> str:
        index = 0
        message = ''

        for member in on_duty_role.members:
            index += 1
            message += f'{index}. {member.mention}\n'
        
        if index == 0:
            message = 'None'
        
        return message
    
    
    
    @button(label = 'Apply for On-Duty', style = ButtonStyle.green, custom_id = 'apply_duty')
    async def apply_duty(self, interaction: Interaction, button: Button):
        on_duty_role = interaction.guild.get_role(self.config.roles.on_duty)
        if on_duty_role in interaction.user.roles:
            await interaction.response.send_message(f'❌ You already have {on_duty_role.mention} role', ephemeral = True)
            return
        
        await interaction.user.add_roles(on_duty_role)

        message = self._on_duty_embed_message(on_duty_role)

        embed = create_embed(
            description = f'Get or Drop {on_duty_role.mention} role by using the buttons below.\n\n__**Current On-Duty Members:**__\n{message}',
            color = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': f'Latest Action: ✅ {interaction.user.name} joined the On Duty team'
            }
        )

        await interaction.response.edit_message(embed = embed)


        log_channel = interaction.guild.get_channel(self.config.channels.logs.bot)

        embed = create_embed(
            description = f'{interaction.user.mention} applied for `on-duty`.'
        )

        await log_channel.send(embed = embed)
    
    
    @button(label = 'Resign from On-Duty', style = ButtonStyle.red, custom_id = 'resign_duty')
    async def resign_duty(self, interaction: Interaction, button: Button):
        on_duty_role = interaction.guild.get_role(self.config.roles.on_duty)
        if on_duty_role not in interaction.user.roles:
            await interaction.response.send_message(f'❌ You don\'t have {on_duty_role.mention} role', ephemeral = True)
            return
        
        await interaction.user.remove_roles(on_duty_role)

        message = self._on_duty_embed_message(on_duty_role)

        embed = create_embed(
            description = f'Get or Drop {on_duty_role.mention} role by using the buttons below.\n\n__**Current On-Duty Members:**__\n{message}',
            color = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': f'Latest Action: ⛔ {interaction.user.name} resigned from the On Duty team'
            }
        )

        await interaction.response.edit_message(embed = embed)


        log_channel = interaction.guild.get_channel(self.config.channels.logs.bot)

        embed = create_embed(
            description = f'{interaction.user.mention} resigned for `on-duty`.'
        )

        await log_channel.send(embed = embed)
    
    
    @button(label = 'Refresh', style = ButtonStyle.blurple, emoji = '🔁', custom_id = 'refresh_duty')
    async def refresh_duty(self, interaction: Interaction, button: Button):
        on_duty_role = interaction.guild.get_role(self.config.roles.on_duty)
        
        message = self._on_duty_embed_message(on_duty_role)

        embed = create_embed(
            description = f'Get or Drop {on_duty_role.mention} role by using the buttons below.\n\n__**Current On-Duty Members:**__\n{message}',
            color = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': 'Latest Action: 🔄 Refreshed'
            }
        )

        await interaction.response.edit_message(embed = embed)