import discord,Configuration,Functions,datetime,os
from discord import app_commands
from discord.ext import commands
class General(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.Cog.listener()
    async def on_member_join(self,member):
        Welcome_Channel=self.bot.get_channel(Configuration.Welcome_Channel[Functions.Configuration_Position(member.guild.id)])
        Embed=discord.Embed(title="**Welcome to Cursed Obsidian!**",description=f"Welcome {member.mention}",color=0x00F3FF).set_thumbnail(url=str(member.display_avatar.url)).add_field(name="Account Created",value=f"<t:{round(member.created_at.timestamp())}:R>",inline=False).set_footer(text=f"ID: {str(member.id)}")
        Embed.timestamp=datetime.datetime.now()
        await Welcome_Channel.send(embed=Embed)
    @app_commands.command(name="ping",description="Sends the latency of the bot")
    async def ping(self,interaction: discord.Interaction):
        await interaction.response.send_message(f"Latency: {round(self.bot.latency*1000)}ms",ephemeral=True)
    @app_commands.command(name="bot-info",description="Shows info about the bot")
    async def botinfo(self,interaction:discord.Interaction):
        Uptime_TimeStamp=f"<t:{int(datetime.datetime.timestamp(interaction.client.Time))}:R>"
        Ping=f"{round(interaction.client.latency*1000)}ms"
        Total_Lines=0
        for Filename in os.listdir("./Cursed_Obsidian"):
            if Filename.endswith(".py"):
                with open("./Cursed_Obsidian/"+Filename,'r') as File:
                    Total_Lines+=len(File.readlines())
        for Filename in os.listdir("./Cursed_Obsidian/Cogs"):
            if Filename.endswith(".py"):
                with open("./Cursed_Obsidian/Cogs/"+Filename,'r') as File:
                    Total_Lines+=len(File.readlines())
        for Filename in os.listdir("./Cursed_Obsidian/Views"):
            if Filename.endswith(".py"):
                with open("./Cursed_Obsidian/Views/"+Filename,'r') as File:
                    Total_Lines+=len(File.readlines())
        await interaction.response.send_message(embed=discord.Embed(title="Bot Status",description=f"Bot Uptime: {Uptime_TimeStamp}\nLines of code: {Total_Lines}\nPing: {Ping}",color=0x00F3FF),ephemeral=True)
    @app_commands.command(name="server-info",description="Shows info about the server")
    async def serverinfo(self,interaction:discord.Interaction):
        Embed=discord.Embed(title=f"Server info for {interaction.guild.name}",color=0x00F3FF).add_field(name="**<:CO:1046185442774634567>Owner**",value=f"{interaction.guild.owner.mention}",inline=True).add_field(name="**🎂 Created**",value=f"<t:{round(interaction.guild.created_at.timestamp())}:R>",inline=True).add_field(name="**<:TV:1060579195312410664>Channels**",value=f"Text:{len(interaction.guild.text_channels)}\nVoice:{len(interaction.guild.voice_channels)}").add_field(name="**👥Members**",value=f"{interaction.guild.member_count}").add_field(name="**🧻Roles**",value=f"{len(interaction.guild.roles)}").add_field(name="**<:Boost:1060577591045652621>Boosters**",value=f"{interaction.guild.premium_subscription_count}").set_image(url=interaction.guild.banner).set_footer(text=f"ID: {interaction.guild_id}")
        Embed.timestamp=datetime.datetime.now()
        await interaction.response.send_message(embed=Embed)
async def setup(bot):
    await bot.add_cog(General(bot))