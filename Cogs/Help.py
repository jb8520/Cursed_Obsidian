import discord
from discord import app_commands
from discord.ext import commands
class Help(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @app_commands.command(name="help",description="Shows information about other commands")
    @app_commands.choices(commands=[app_commands.Choice(name="Ping",value="ping"),app_commands.Choice(name="Leave",value="leave"),app_commands.Choice(name="Disconnect",value="disconnect"),app_commands.Choice(name="Goldrush",value="goldrush"),app_commands.Choice(name="Spike",value="spike")])
    async def help(self,interaction:discord.Interaction,commands:app_commands.Choice[str]=None):
        if commands is None:
            Embed=discord.Embed(title="__**Bot Commands**__",description="```fix\nPing = Sends the latency of the bot```\n```fix\nGoldrush = A command that shows Goldrush hours for your timezone.```\n```fix\nLeave = A command to notify OnDuty staff that a user has to leave their ship, 10 minutes **before** they need to leave. Can also click on the 'Leave Ship button in the Join-Queue channel'```\n```fix\nDisconnect = A command to notify staff that you were disconnected from your ship voice channel and need to be moved back in.```\n```fix\nSpike = A command that gives you info as to when the next spike will be.```",colour=discord.Colour.orange())
        elif commands.value=="ping":
            Embed=discord.Embed(title="__**Ping:**__",description="Sends the latency of the bot",colour=discord.Colour.orange())
        elif commands.value=="leave":
            Embed=discord.Embed(title="__**Leave:**__",description="A command to notify OnDuty staff that a user has to leave their ship, 10 minutes **before** they need to leave. Can also click on the 'Leave Ship button in the Join-Queue channel'",colour=discord.Colour.orange())
        elif commands.value=="disconnect":
            Embed=discord.Embed(title="__**Disconnect:**__",description="A command to notify staff that you were disconnected from your ship voice channel and need to be moved back in.",colour=discord.Colour.orange())     
        elif commands.value=="goldrush":
            Embed=discord.Embed(title="__**Goldrush:**__",description="A command that shows Goldrush hours for your timezone.",colour=discord.Colour.orange())
        elif commands.value=="spike":
            Embed=discord.Embed(title="__**Spike:**__",description="A command that gives you info as to when the next spike will be.",colour=discord.Colour.orange())
        await interaction.response.send_message(embed=Embed,ephemeral=True)
async def setup(bot):
    await bot.add_cog(Help(bot))