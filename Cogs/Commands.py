import discord,Configuration,Functions,datetime
from discord import app_commands
from discord.ext import commands
class Commands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @app_commands.command(name="goldrush",description="A command that shows when the next Goldrush hour will be")
    @app_commands.checks.has_any_role("Members")
    async def goldrush(self,interaction:discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(title="Goldrush Hours",description="Hours for Goldrush (shown for your timezone)\n\n**<t:2563290000:t>-<t:2563293600:t>** and **<t:2563318800:t>-<t:2563322400:t>**",color=0xffd700).set_image(url="https://media1.giphy.com/media/2LnaiD9MmlVeCkDPYz/giphy.gif?cid=ecf05e470v7xhzbtv0zjdodc29mrc91naz8ff8bi5yxg4ncf&rid=giphy.gif&ct=g"),ephemeral=False)
    @app_commands.command(name="spike",description="Sends a message about when the next fleet/spike will be")
    @app_commands.checks.has_any_role("Members")
    async def spike(self,interaction:discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(description="A staff member will ping when they are able to spike and host a server. If you want to be notified of server spikes, grab the `@Spiking` or `@Alliance Ping` role from <#984437310756118528>. Also, please read the <#974661594015481896> If you haven't already done so. Thanks.",color=0x00F3FF),ephemeral=True)
    @app_commands.command(name="disconnect",description="Notify staff that you were disconnected from your ship voice channel and need moving back in.")
    @app_commands.checks.has_any_role("Members")
    async def disconnect(self,interaction:discord.Interaction):
        On_Duty_Channel=interaction.guild.get_channel(Configuration.On_Duty_Chat[Functions.Configuration_Position(interaction.guild.id)])
        On_Duty_Role=interaction.guild.get_role(Configuration.On_Duty_Role[Functions.Configuration_Position(interaction.guild.id)])
        await On_Duty_Channel.send(f"{On_Duty_Role.mention} {interaction.user.mention} has been disconnected from their ship.")
        await interaction.response.send_message("✅ Please join the waiting room & wait to be moved.",ephemeral=True)
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} used `/disconnect`."))
    @app_commands.command(name="leave",description="Notify staff that you have to leave your ship, 10 minutes **before** you need to leave.")
    @app_commands.checks.has_any_role("Members")
    async def leave(self,interaction:discord.Interaction):
        Ship=""
        for Position in range(len(interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)])):
            if interaction.guild.get_role(interaction.client.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)][Position]) in interaction.user.roles:
                Fleet_Ships=[interaction.guild.get_channel(interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)][Position])]
                for Channel in Fleet_Ships:
                    if interaction.user in Channel.members:
                        Ship=Channel.mention
                        break
                Join_Queue=interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)])
                On_Duty_Role=interaction.guild.get_role(Configuration.On_Duty_Role[Functions.Configuration_Position(interaction.guild.id)])
                await Join_Queue.send(f"{On_Duty_Role.mention} {interaction.user.mention} has to leave {Ship} in <t:{int(datetime.datetime.timestamp(discord.utils.utcnow()+datetime.timedelta(minutes=10)))}:R>",delete_after=600)
                await interaction.response.send_message("✅ Submitted leave request",ephemeral=True)
                Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
                await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} used `/leave` - {Ship}."))
                return
        await interaction.response.send_message(f"**{interaction.user.name}**, you aren't on a ship!",ephemeral=True)
async def setup(bot):
    await bot.add_cog(Commands(bot))