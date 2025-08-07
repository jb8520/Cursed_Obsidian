import discord
from discord import app_commands
from discord.app_commands import AppCommandError
from discord.ext import tasks
from discord.ext.commands import Cog

from Utils.command_decorators import app_command_requires_role_of_perm_tiers

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints


class Background_Tasks(Cog):
    def __init__(self, bot: 'MyBot'):
        self.bot= bot
        self.config = bot.config
        self.active_auto_message_fleet_nums = []
    
    
    
    @tasks.loop(hours = 1)
    async def auto_message(self):
        for fleet_num in self.active_auto_message_fleet_nums:
            fleet_chat = self.bot.get_channel(self.bot.state.Fleet_State.chat[fleet_num])

            embed_1 = discord.Embed(
                title = '<a:teal_siren:1058114293184331876> __**FLEET COMMANDS:**__ <a:teal_siren:1058114293184331876>',
                description = '```fix\n/leave = Use this if you would like to leave your ship. You must use this 10 minutes before wanting to leave.\n``````fix\n/disconnect = Use this if you were removed from your ship voice chat by accident\n``````ini\nOr you can click the [leave ship] or [disconnect] button in the Join-Queue channel```',
                color = 0x00F3FF
            )
            embed_2 = discord.Embed(
                title = '<a:white_siren:1058120536942723123> **ATTENTION** <a:white_siren:1058120536942723123>',
                description = '```diff\n- DO NOT INTERACT WITH THE HOURGLASS\n\n- \'Voting to pledge allegiance\' will cause us to lose a ship on our server. Crewmates should NEVER vote on the hourglass. NO EXCEPTIONS.\n\n- Failure to follow this rule will result in punishment for all 3 members of the crew that lost the ship```\n\n```ansi\n[2;31m• Do not accept DM\'s from other players asking for an invite to your ship.\n• Staff will never ask for an invite via DM.\n• ONLY invite players who are in your voice channel.\n• ONLY send invites to the players[0m [2;32mlinked xbox account[0m[2;31m.[0m\n```',
                color = 0xFF0000
            )

            await fleet_chat.send(embed = embed_1)
            await fleet_chat.send(embed = embed_2)
    
    
    @app_commands.command(name = 'start-loop', description = 'Staff Only | Starts Fleet Auto Message Reminders.')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def start(self, interaction: discord.Interaction, fleet_number: int):
        if fleet_number not in self.bot.state.Fleet_State.category.keys():
            await interaction.response.send_message(f'❌ Please select any active fleet', ephemeral = True)
            return
        if fleet_number in self.active_auto_message_fleet_nums:
            await interaction.response.send_message(f'❌ The auto-message for fleet {fleet_number} is already active.', ephemeral = True)
            return
        
        self.active_auto_message_fleet_nums.append(fleet_number)

        if not self.auto_message.is_running():
            self.auto_message.start()
        
        await interaction.response.send_message('✅ Successfully Started Loop!', ephemeral = True)

        log_channel = interaction.guild.get_channel(self.config.channels.logs.bot) 
        embed = discord.Embed(
            description = f'{interaction.user.mention} has `started` the fleet {fleet_number} auto-message.'
        )

        await log_channel.send(embed = embed)
                
    
    @app_commands.command(name = 'stop-loop', description = 'Staff Only | Stops Fleet Auto Message Reminders.')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def cancel(self, interaction: discord.Interaction, fleet_number: int):
        if fleet_number not in self.bot.state.Fleet_State.category.keys():
            await interaction.response.send_message(f'❌ Please select any active fleet', ephemeral = True)
            return
        
        if fleet_number not in self.active_auto_message_fleet_nums:
            await interaction.response.send_message(f'❌ The auto-message for fleet {fleet_number} is not currently active.', ephemeral = True)
            return
        
        self.active_auto_message_fleet_nums.remove(fleet_number)
        
        if not self.active_auto_message_fleet_nums:
            self.auto_message.stop()
        
        await interaction.response.send_message('✅ Successfully Stopped Loop!', ephemeral = True)

        log_channel = interaction.guild.get_channel(self.config.channels.logs.bot)
        embed = discord.Embed(
            description = f'{interaction.user.mention} has `stopped` the fleet {fleet_number} auto-message.'
        )

        await log_channel.send(embed = embed)            
    
    
    
    @app_commands.command(name = 'stacking', description = 'Sends a reminder about loot stacking')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def stacking(self, interaction: discord.Interaction, fleet_number: int):
        if fleet_number not in self.bot.state.Fleet_State.category.keys():
            await interaction.response.send_message(f'❌ Please select any active fleet', ephemeral = True)
            return
        
        fleet_chat = interaction.guild.get_channel(self.bot.state.Fleet_State.chat[fleet_number])
        fleet_role = interaction.guild.get_role(self.bot.state.Fleet_State.role[fleet_number])

        embed = discord.Embed(
            title = '<a:siren_green:1037535598648512553> REMINDER <a:siren_green:1037535598648512553>',
            description = 'Please remember the to follow the loot stacking rules in <#933896846030536756>. Stacking rules are enforced so that everyone benefits from selling, and also to minimize server lag.\n\n**3 stacks max - Applies to every event/voyage**',
            color = 0x00F3FF
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/987840022076080229/1037541030955851866/gold_pile.png')

        await fleet_chat.send(content = fleet_role.mention, embed = embed)

        await interaction.response.send_message('✅ Success!', ephemeral = True)
    
    
    @app_commands.command(name = 'ritual-skulls',description='Sends a reminder not to sell ritual skulls')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def ritual(self,interaction:discord.Interaction,fleet_number:int):
        if fleet_number not in self.bot.state.Fleet_State.category.keys():
            await interaction.response.send_message(f'❌ Please select any active fleet', ephemeral = True)
            return
        
        fleet_chat = interaction.guild.get_channel(self.bot.state.Fleet_State.chat[fleet_number])
        fleet_role = interaction.guild.get_role(self.bot.state.Fleet_State.role[fleet_number])

        embed = discord.Embed(
            title = '<a:siren_green:1037535598648512553> REMINDER <a:siren_green:1037535598648512553>',
            description = 'PLEASE DO NOT SELL RITUAL SKULLS. ALL RITUAL SKULLS ARE TO GO TO THE FOTD CREW.',
            color = 0x00F3FF
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/987840022076080229/1037539022668578826/unknown.png')

        await fleet_chat.send(content = fleet_role.mention, embed = embed)

        await interaction.response.send_message('✅ Success!', ephemeral = True)

    
    @app_commands.command(name='rogue',description='Sends a ping to notify players of a rogue ship')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def rogue(self,interaction:discord.Interaction,fleet_number:int):
        if fleet_number not in self.bot.state.Fleet_State.category.keys():
            await interaction.response.send_message(f'❌ Please select any active fleet', ephemeral = True)
            return
        
        fleet_chat = interaction.guild.get_channel(self.bot.state.Fleet_State.chat[fleet_number])
        fleet_role = interaction.guild.get_role(self.bot.state.Fleet_State.role[fleet_number])

        embed = discord.Embed(
            title = '<a:siren_green:1037535598648512553> REMINDER <a:siren_green:1037535598648512553>',
            description = '**There is a rogue ship on the server**\n\n**SELL WHAT YOU HAVE AND THEN LEAVE THE GAME\nDO NOT ATTEMPT TO ATTACK/COMMUNICATE WITH THE ROGUE SHIP**',
            color = 0x00F3FF
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/944057671160561694/1033861074912546856/skull_glow.gif')
        embed.set_image(url = 'https://cdn.discordapp.com/attachments/987840022076080229/1037533607075528714/Rogue.png')

        await fleet_chat.send(content = fleet_role.mention, embed = embed)

        await interaction.response.send_message('✅ Success!', ephemeral = True)

        log_channel = interaction.guild.get_channel(self.config.channels.logs.bot)
        embed = discord.Embed(
            description = f'{interaction.user.mention} used the `/rogue` command.'
        )

        await log_channel.send(embed = embed)

    
    
    async def cog_app_command_error(self, interaction: discord.Interaction, error: AppCommandError):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message('❌ Only Staff can invoke that command!', ephemeral = True)
        
        else:
            print(error)
            await interaction.response.send_message('❌ An error occurred, please try again later.')


async def setup(bot: 'MyBot'):
    await bot.add_cog(Background_Tasks(bot))