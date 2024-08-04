import discord,Configuration,Functions
from discord import app_commands
from discord.ext import commands,tasks
class Background_Tasks(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.Active_Auto_Message=[[],[]]
        self.Active_Fleets=bot.Active_Fleets
        self.Fleet_Roles=bot.Fleet_Roles
        self.Fleet_Chats=bot.Fleet_Chats
    @tasks.loop(hours=1)
    async def Auto_Message(self):
        for Server in range(len(self.Active_Auto_Message)):
            for Fleet in self.Active_Auto_Message[Server]:
                Position=self.Active_Fleets[Server].index(Fleet)
                Fleet_Chat=self.bot.get_channel(self.Fleet_Chats[Server][Position])
                await Fleet_Chat.send(embed=discord.Embed(title="<a:teal_siren:1058114293184331876> __**FLEET COMMANDS:**__ <a:teal_siren:1058114293184331876>",description="```fix\n/leave = Use this if you would like to leave your ship. You must use this 10 minutes before wanting to leave.\n``````fix\n/disconnect = Use this if you were removed from your ship voice chat by accident\n``````ini\nOr you can click the [leave ship] or [disconnect] button in the Join-Queue channel```",color=0x00F3FF))
                await Fleet_Chat.send(embed=discord.Embed(title="<a:white_siren:1058120536942723123> **ATTENTION** <a:white_siren:1058120536942723123>",description="```diff\n- DO NOT INTERACT WITH THE HOURGLASS\n\n- 'Voting to pledge allegiance' will cause us to lose a ship on our server. Crewmates should NEVER vote on the hourglass. NO EXCEPTIONS.\n\n- Failure to follow this rule will result in punishment for all 3 members of the crew that lost the ship```\n\n```ansi\n[2;31m• Do not accept DM's from other players asking for an invite to your ship.\n• Staff will never ask for an invite via DM.\n• ONLY invite players who are in your voice channel.\n• ONLY send invites to the players[0m [2;32mlinked xbox account[0m[2;31m.[0m\n```",color=0xFF0000))
    @app_commands.command(name="start-loop",description="Staff Only | Starts Fleet Auto Message Reminders.")
    @app_commands.checks.has_any_role("Staff")
    async def start(self,interaction:discord.Interaction,fleet:int):
        if fleet in self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            if fleet in self.Active_Auto_Message[Functions.Configuration_Position(interaction.guild.id)]:
                await interaction.response.send_message(f"❌ The auto-message for fleet {fleet} is already active.",ephemeral=True)
                return
            self.Active_Auto_Message[Functions.Configuration_Position(interaction.guild.id)].append(fleet)
            if self.Auto_Message.is_running()==False:
                self.Auto_Message.start()
            await interaction.response.send_message("✅ Successfully Started Loop!",ephemeral=True)
            Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)]) 
            await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} has `started` the fleet {fleet} auto-message."))
        else:
            await interaction.response.send_message(f"❌ Please select any active fleet",ephemeral=True)
    @app_commands.command(name="stop-loop",description="Staff Only | Stops Fleet Auto Message Reminders.")
    @app_commands.checks.has_any_role("Staff")
    async def cancel(self, interaction:discord.Interaction,fleet:int):
        if fleet in self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            if fleet not in self.Active_Auto_Message[Functions.Configuration_Position(interaction.guild.id)]:
                await interaction.response.send_message(f"❌ The auto-message for fleet {fleet} is not currently active.",ephemeral=True)
                return
            self.Active_Auto_Message[Functions.Configuration_Position(interaction.guild.id)].remove(fleet)
            if self.Active_Auto_Message[Functions.Configuration_Position(interaction.guild.id)]==[]:
                self.Auto_Message.stop()
            await interaction.response.send_message("✅ Successfully Stopped Loop!",ephemeral=True)
            Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)]) 
            await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} has `stopped` the fleet {fleet} auto-message."))
        else:
            await interaction.response.send_message(f"❌ Please select any active fleet",ephemeral=True)
    @app_commands.command(name="stacking",description="Sends a reminder about loot stacking")
    @app_commands.checks.has_any_role("Staff")
    async def stacking(self,interaction:discord.Interaction,fleet:int):
        if fleet in self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            Position=self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(fleet)
            Fleet_Chat=interaction.guild.get_channel(self.Fleet_Chats[Functions.Configuration_Position(interaction.guild.id)][Position])
            Fleet_Role=interaction.guild.get_role(self.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)][Position])
            await Fleet_Chat.send(content=Fleet_Role.mention,embed=discord.Embed(title="<a:siren_green:1037535598648512553> REMINDER <a:siren_green:1037535598648512553>",description="Please remember the to follow the loot stacking rules in <#933896846030536756>. Stacking rules are enforced so that everyone benefits from selling, and also to minimize server lag.\n\n**3 stacks max - Applies to every event/voyage**",color=0x00F3FF).set_thumbnail(url='https://cdn.discordapp.com/attachments/987840022076080229/1037541030955851866/gold_pile.png'))
            await interaction.response.send_message("✅ Success!",ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Please select any active fleet",ephemeral=True)
    @app_commands.command(name="ritual-skulls",description="Sends a reminder not to sell ritual skulls")
    @app_commands.checks.has_any_role("Staff")
    async def ritual(self,interaction:discord.Interaction,fleet:int):
        if fleet in self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            Position=self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(fleet)
            Fleet_Chat=interaction.guild.get_channel(self.Fleet_Chats[Functions.Configuration_Position(interaction.guild.id)][Position])
            Fleet_Role=interaction.guild.get_role(self.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)][Position])
            await Fleet_Chat.send(content=Fleet_Role.mention,embed=discord.Embed(title="<a:siren_green:1037535598648512553> REMINDER <a:siren_green:1037535598648512553>",description="PLEASE DO NOT SELL RITUAL SKULLS. ALL RITUAL SKULLS ARE TO GO TO THE FOTD CREW.",color=0x00F3FF).set_thumbnail(url='https://cdn.discordapp.com/attachments/987840022076080229/1037539022668578826/unknown.png'))
            await interaction.response.send_message("✅ Success!",ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Please select any active fleet",ephemeral=True)
    @app_commands.command(name="rogue",description="Sends a ping to notify players of a rogue ship")
    @app_commands.checks.has_any_role("Staff")
    async def rogue(self,interaction:discord.Interaction,fleet:int):
        if fleet in self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            Position=self.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(fleet)
            Fleet_Chat=interaction.guild.get_channel(self.Fleet_Chats[Functions.Configuration_Position(interaction.guild.id)][Position])
            Fleet_Role=interaction.guild.get_role(self.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)][Position])
            await Fleet_Chat.send(content=Fleet_Role.mention,embed=discord.Embed(title="<a:siren:1003398319101460520> ATTENTION <a:siren:1003398319101460520>",description="**There is a rogue ship on the server**\n\n**SELL WHAT YOU HAVE AND THEN LEAVE THE GAME\nDO NOT ATTEMPT TO ATTACK/COMMUNICATE WITH THE ROGUE SHIP**",color=0xFF0000).set_thumbnail(url="https://cdn.discordapp.com/attachments/944057671160561694/1033861074912546856/skull_glow.gif").set_image(url='https://cdn.discordapp.com/attachments/987840022076080229/1037533607075528714/Rogue.png'))
            await interaction.response.send_message("✅ Success!",ephemeral=True)
            Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
            await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} used the `/rogue` command."))
        else:
            await interaction.response.send_message(f"❌ Please select any active fleet",ephemeral=True)
    async def cog_app_command_error(self,interaction:discord.Interaction,error):
        if isinstance(error,app_commands.errors.MissingAnyRole):
            await interaction.response.send_message("❌ Only Staff can invoke that command!",ephemeral=True)
        else:
            print(error)
async def setup(bot):
    await bot.add_cog(Background_Tasks(bot))