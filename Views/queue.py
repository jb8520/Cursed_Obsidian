import discord, datetime
from discord import Interaction, ButtonStyle, TextStyle
from discord.ui import View, Modal, Button, button, TextInput

from discord.utils import utcnow


from Utils.embed_functions import create_embed, set_embed_attr

from Configuration.value_types import ConfigTypes

from Utils import (
    send_log_message,
    update_queue_embed,
    update_user_in_queue_role,
    queue_check_requires_role_of_perm_tiers,
    check_queue_open,
    check_member_in_queue
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints





class ActivityModal(Modal):
    def __init__(self, bot: 'MyBot'):
        super().__init__(title = 'Join Fleet Queue')
        self.bot = bot
        self.state = bot.state
        self.config = bot.config
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State
        


    activity_from_modal = TextInput(
        label = 'TYPE YOUR DESIRED ACTIVITY',
        style = TextStyle.short,
        placeholder = 'You can change this at any time later using the button without losing your place in the queue',
        required = True
    )
    

    async def on_submit(self, interaction: Interaction):
        activity = self.activity_from_modal.value

        self.bot.state_loader.user_join_queue(
            user_id = interaction.user.id,
            activity = activity
        )


        await update_user_in_queue_role(
            interaction = interaction,
            config = self.config,
            member = interaction.user,
            queue_role_add = True
        )
        await update_queue_embed(
            interaction = interaction,
            config = self.config,
            queue_state = self.queue_state
        )

        await interaction.response.send_message('✅ Success!', ephemeral = True)

        

        log_description = f'{interaction.user.mention} queued for {activity}.'

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = log_description
        )

        
class OpenQueueButtons(View):
    def __init__(self, bot: 'MyBot'):
        super().__init__(timeout = None)
        self.bot = bot
        self.state = bot.state
        self.config = bot.config
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State


    @button(label = 'Join Queue/Update Queue', style = ButtonStyle.green, custom_id = 'join_queue', row = 1)
    async def join_queue(self, interaction: Interaction, button: Button):
        if not await queue_check_requires_role_of_perm_tiers(
            interaction = interaction,
            tiers = ['tier_0', 'tier_1']
        ):
            return
 

        await interaction.response.send_modal(ActivityModal(self.bot))
    
    
    @button(label = 'Leave Queue', style = ButtonStyle.red, custom_id = 'leave_queue', row = 1)
    async def leave_queue(self, interaction: Interaction, button: Button):
        if not await check_member_in_queue(
            queue_state = self.queue_state,
            interaction = interaction,
            member = interaction.user
        ):
            return
        if not await queue_check_requires_role_of_perm_tiers(
            interaction = interaction,
            tiers = ['tier_0', 'tier_1']
        ):
            return
        

        self.bot.state_loader.user_leave_queue(
            user_id = interaction.user.id
        )


        await update_user_in_queue_role(
            interaction = interaction,
            config = self.config,
            member = interaction.user,
            queue_role_add = False
        )
        await update_queue_embed(
            interaction = interaction,
            config = self.config,
            queue_state = self.queue_state
        )

        await interaction.response.send_message('✅ Success!', ephemeral = True)



        log_description = f'{interaction.user.mention} left the queue.'

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = log_description
        )


    @button(label = 'Leave Ship', style = ButtonStyle.blurple, custom_id = 'leave_ship', row = 2)
    async def leave_ship(self, interaction: Interaction, button: Button):
        if not await queue_check_requires_role_of_perm_tiers(
            interaction = interaction,
            tiers = ['tier_0', 'tier_1']
        ):
            return
        

        ship = None
        for fleet_num in self.fleet_state.category:
            fleet_role_id = self.fleet_state.role[fleet_num]
            fleet_role = interaction.guild.get_role(fleet_role_id)

            if fleet_role in interaction.user.roles:
                vc_ids = self.state.Fleet_State.vcs[fleet_num]
                vcs = [interaction.guild.get_channel(vc_ids[i]) for i in range(6)]

                for vc in vcs:
                    if interaction.user in vc.members:
                        ship = vc.mention
                        break
                
                if not ship:
                    await interaction.response.send_message(f'**{interaction.user.name}**, you aren\'t on a ship!', ephemeral = True)
                    return
                
                queue_channel = interaction.guild.get_channel(self.config.channels.fleet_queue.queue)
                on_duty_role = interaction.guild.get_role(self.config.roles.on_duty)

                await queue_channel.send(
                    f'{on_duty_role.mention} {interaction.user.mention} has to leave {ship} in <t:{int(datetime.datetime.timestamp(utcnow() + datetime.timedelta(minutes = 10)))}:R>',
                    delete_after = 600
                )

                
                await interaction.response.send_message('✅ Submitted leave request', ephemeral = True)
                
                
                log_description = f'{interaction.user.mention} used `/leave` - {ship}.'

                await send_log_message(
                    interaction = interaction,
                    config = self.config,
                    description = log_description
                )

                return
        await interaction.response.send_message(f'**{interaction.user.name}**, you aren\'t on a ship!', ephemeral = True)

            

    @button(label = 'Disconnected', style = ButtonStyle.grey, custom_id = 'disconnect', row = 2)
    async def disconnect(self, interaction: Interaction, button: Button):
        if not await queue_check_requires_role_of_perm_tiers(
            interaction = interaction,
            tiers = ['tier_0', 'tier_1']
        ):
            return
       
        
        on_duty_chat = interaction.guild.get_channel(self.config.channels.fleet_staff.on_duty_chat)
        on_duty_role = interaction.guild.get_role(self.config.roles.on_duty)
        
        
        await on_duty_chat.send(f'{on_duty_role.mention} {interaction.user.mention} has been disconnected from their ship.')

        await interaction.response.send_message('✅ Please join the waiting room & wait to be moved.', ephemeral = True)


        log_description = f'{interaction.user.mention} used `/disconnect`.'

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = log_description
        )


class ClosedQueueButton(View):
    def __init__(self, bot: 'MyBot' ):
        super().__init__(timeout = None)
        self.bot = bot
        self.state = bot.state
        self.config = bot.config
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State


    @button(label = 'Open Queue', style = ButtonStyle.green, emoji = '🔓', custom_id = 'open_queue')
    async def open_queue(self, interaction: Interaction, button: Button):
        if not await queue_check_requires_role_of_perm_tiers(
            interaction = interaction,
            tiers = ['tier_3', 'tier_4']
        ):
            return
        

        self.bot.state_loader.queue_open()


        queue_channel = interaction.guild.get_channel(self.config.channels.fleet_queue.queue)
        queue_embed = await queue_channel.fetch_message(self.config.embeds.queue_panel)

        embed = create_embed(
            title = self.config.preset_messages.queue_title,
            description = self.config.preset_messages.queue_description,
            colour = 0x00F3FF
        )

        await queue_embed.edit(
            embed = embed,
            view = OpenQueueButtons(self.bot)
        )
        

        embed = create_embed(
            title = 'Staff Queue Buttons',
            description = 'Use the Buttons below to control the queue',
            colour = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': f'Latest Action: ✅ Queue opened by {interaction.user.name}'
            }
        )

        await interaction.response.edit_message(
            embed = embed,
            view = StaffQueueButtons(self.bot)
        )
        
        
        log_description = f'{interaction.user.mention} `opened` the queue.'

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = log_description
        )



class StaffQueueButtons(View):
    def __init__(self, bot: 'MyBot'):
        super().__init__(timeout = None)
        self.bot = bot
        self.state = bot.state
        self.config = bot.config
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State



    @button(label = 'Refresh', style = ButtonStyle.blurple, emoji = '🔄', custom_id = 'refresh_queue')
    async def refresh_queue(self, interaction: Interaction, button: Button):
        await update_queue_embed(
            interaction = interaction,
            config = self.config,
            queue_state = self.queue_state
        )


        embed = create_embed(
            title = 'Staff Queue Buttons',
            description = 'Use the Buttons below to control the queue',
            colour = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': f'Latest Action: 🔁 refreshed the queue'
            }
        )

        await interaction.response.edit_message(embed = embed)
        

        log_description = f'{interaction.user.mention} `refreshed` the queue.'

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = log_description
        )
    
    
    @button(label = 'Close Queue', style = ButtonStyle.red, emoji = '🔒', custom_id = 'close_queue')
    async def close_queue(self, interaction: Interaction, button: Button):
        if not await queue_check_requires_role_of_perm_tiers(
            interaction = interaction,
            tiers = ['tier_3', 'tier_4']
        ):
            return
        

        self.bot.state_loader.queue_close()

        queue_channel = interaction.guild.get_channel(self.config.channels.fleet_queue.queue)
        queue_embed = await queue_channel.fetch_message(self.config.embeds.queue_panel)

        embed = create_embed(
            title = '__**Cursed Obsidian Queue**__',
            description = 'The queue is currently closed',
            colour = 0xFF0000
        )

        await queue_embed.edit(
            embed = embed,
            view = None
        )
        

        embed = create_embed(
            title = 'Staff Queue Buttons',
            description = 'Use the Buttons below to control the queue',
            colour = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': f'Latest Action: ❌ Queue closed by {interaction.user.name}'
            }
        )

        await interaction.response.edit_message(
            embed = embed,
            view = ClosedQueueButton(self.bot)
        )


        in_queue_role = interaction.guild.get_role(self.config.roles.in_queue)

        for member in in_queue_role.members:
            await member.remove_roles(in_queue_role)


        log_description = f'{interaction.user.mention} `closed` the queue.'

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = log_description
        )
    
    
    @button(label = 'Clear Queue', style = ButtonStyle.grey, emoji = '🧹', custom_id = 'clear_queue')
    async def clear_queue(self, interaction: Interaction, button: Button):
        if not await queue_check_requires_role_of_perm_tiers(
            interaction = interaction,
            tiers = ['tier_3', 'tier_4']
        ):
            return
        
        if not await check_queue_open(
            queue_state = self.queue_state,
            interaction = interaction
        ):
            return
        

        self.bot.state_loader.queue_clear()

        queue_channel = interaction.guild.get_channel(self.config.channels.fleet_queue.queue)
        queue_embed = await queue_channel.fetch_message(self.config.embeds.queue_panel)

        embed = create_embed(
            title = self.config.preset_messages.queue_title,
            description = self.config.preset_messages.queue_description,
            colour = 0x00F3FF
        )

        await queue_embed.edit(embed = embed)
        

        embed = create_embed(
            title = 'Staff Queue Buttons',
            description = 'Use the Buttons below to control the queue',
            colour = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': f'Latest Action: 🧹 Queue cleared by {interaction.user.name}'
            }
        )

        await interaction.response.edit_message(embed = embed)


        in_queue_role = interaction.guild.get_role(self.config.roles.in_queue)

        for member in in_queue_role.members:
            await member.remove_roles(in_queue_role)


        log_description = f'{interaction.user.mention} `cleared` the queue.'

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = log_description
        )
