from discord import Interaction, ButtonStyle
from discord.ui import View, Button, button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class ConfirmView(View):
    def __init__(self, bot: 'MyBot', confirm_message: str = 'Action Confirmed', cancel_message: str = 'Action Cancelled'):
        super().__init__(timeout = None)
        self.bot = bot
        self.confirm_message = confirm_message
        self.cancel_message = cancel_message

    @button(label = 'Confirm', style = ButtonStyle.green, custom_id = 'confirm_button')
    async def confirm(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(
            content = self.confirm_message, 
            view = None
        )

        self.confirmed = True
        self.stop()
    
    @button(label = 'Cancel', style = ButtonStyle.red, custom_id = 'cancel_button')
    async def cancel(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(
            content = self.cancel_message,
            view = None
        )

        self.confirmed = False
        self.stop()



class VerifyView(View):
    def __init__(self, bot: 'MyBot'):
        super().__init__(timeout = None)
        self.bot = bot

    @button(label = 'Verify', style = ButtonStyle.green, custom_id = 'verify_button')
    async def verify(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(
            content = 'Verification Granted', 
            view = None
        )

        self.verified = True
        self.stop()
    
    @button(label = 'Reject', style = ButtonStyle.red, custom_id = 'reject_button')
    async def reject(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(
            content = 'Verification Denied',
            view = None
        )

        self.verified = False
        self.stop()