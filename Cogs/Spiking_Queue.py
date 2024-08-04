import discord,Configuration,Functions,datetime,asyncio
from discord.ext import commands
class Spiking(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.spiking_queue=[]
    async def Message_Updater(self,member,Spiking_Embed,Footer):
        Spiking_Vc=member.guild.get_channel((Configuration.Spiking_Vc)[Functions.Configuration_Position(member.guild.id)])
        Index=0
        Message=""
        for Member_Id in self.spiking_queue:
            Index+=1
            if member.guild.get_member(member.id) is not None:
                Message+=f"{Index}. {member.guild.get_member(Member_Id).mention}\n"
            else:
                self.spiking_queue.pop(Index)
        await Spiking_Embed.edit(embed=discord.Embed(title="Spiking Queue",description=f"Join {Spiking_Vc.mention} to join this Queue.\n\n**Capacity: {Index} / 99**\n{Message}",color=0x00F3FF).set_footer(text=Footer))
    @commands.Cog.listener()
    async def on_voice_state_update(self,member:discord.Member,before,after):
        Spiking_Vc=member.guild.get_channel(Configuration.Spiking_Vc[Functions.Configuration_Position(member.guild.id)])
        Spiking_Queue=member.guild.get_channel(Configuration.Spiking_Queue[Functions.Configuration_Position(member.guild.id)])
        Footer=None
        if before.channel!=after.channel and before.channel!=Spiking_Vc and after.channel==Spiking_Vc and member.id not in self.spiking_queue:
            self.spiking_queue.append(member.id)
            Footer=f"Latest Action: {member.name} has joined Spiking Queue"
        elif before.channel!=after.channel and before.channel==Spiking_Vc and after.channel!=Spiking_Vc:
            def check(Member,before,after):
                return Member==member and before.channel!=after.channel and after.channel.name==Spiking_Vc.name
            try:
                await self.bot.wait_for("voice_state_update",check=check,timeout=180)
                return
            except:
                self.spiking_queue.remove(member.id)
                Footer=f"Latest Action: {member.name} has left the Spiking Queue"
        if Footer is None:
            return
        Spiking_Embed=await Spiking_Queue.fetch_message(Configuration.Spiking_Embed[Functions.Configuration_Position(member.guild.id)])
        try:
            if discord.utils.utcnow()>=Spiking_Embed.edited_at+datetime.timedelta(seconds=30):
                await self.Message_Updater(member,Spiking_Embed,Footer)
        except:
            await self.Message_Updater(member,Spiking_Embed,Footer)
        else:
            await asyncio.sleep(30)
            if discord.utils.utcnow()<Spiking_Embed.edited_at+datetime.timedelta(seconds=30):
                return
            else:
                await self.Message_Updater(member,Spiking_Embed,Footer)
async def setup(bot):
    await bot.add_cog(Spiking(bot))