import discord,Configuration,Functions
import Cogs.General,Cogs.Roles,Views.Queue,Views.Channel_Control
from discord import app_commands
from discord.ext import commands
class Setup_Commands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.Active_Fleets=bot.Active_Fleets
        self.Fleet_Vc_1=bot.Fleet_Vc_1
        self.Fleet_Vc_2=bot.Fleet_Vc_2
        self.Fleet_Vc_3=bot.Fleet_Vc_3
        self.Fleet_Vc_4=bot.Fleet_Vc_4
        self.Fleet_Vc_5=bot.Fleet_Vc_5
        self.Fleet_Vc_6=bot.Fleet_Vc_6
    @commands.group(invoke_without_command=True,aliases=["s"],case_insensitive=True)
    @commands.has_any_role("Admin","Development Lead")
    async def Embed_Setup(self,ctx):
        await ctx.message.delete(delay=0.5)
        await ctx.author.send("The setup command syntax is: !Embed_Setup <Embed>")
    @Embed_Setup.command(name="inactive")
    @commands.has_any_role("Admin","Development Lead")
    async def inactive(self,ctx):
        await ctx.message.delete(delay=0.5)
        await ctx.guild.get_channel(Configuration.Inactive_Staff[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(title="Inactive Staff Role Selection",description=f"Apply for <@{Configuration.Inactive_Staff_Role[Functions.Configuration_Position(ctx.guild.id)]}> role by using the green button below.\nIf you want to rejoin staff in the future, you will need to open a ticket in <#935566068762681394>\n\n**Staff members who are inactive for more than 30 days will automatically be given this role.**\n\n__**Current Inactive Staff Members:**__\n",color=0x00F3FF),view=Cogs.Roles.InactiveStaff())
    @Embed_Setup.command(name="queue-manager")
    @commands.has_any_role("Admin","Development Lead")
    async def queue_manager(self,ctx):
        await ctx.message.delete(delay=0.5)
        await ctx.guild.get_channel(Configuration.Fleet_Manager[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(title="Staff Queue Buttons",description="Use the Buttons below to control the queue",color=0x00F3FF),view=Views.Queue.StaffQueueButtons())
        await ctx.guild.get_channel(Configuration.Fleet_Manager[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(title="Duty Switch Configurationuration Panel",description=f"Get or Drop <@{Configuration.On_Duty_Role[Functions.Configuration_Position(ctx.guild.id)]}> role by using the buttons below.\n\n__**Current On-Duty Members:**__\n",color=0x00F3FF),view=Cogs.Roles.DutySwitchButtons())
    @Embed_Setup.command(name="queue")
    @commands.has_any_role("Admin","Development Lead")
    async def queue(self,ctx):
        await ctx.message.delete(delay=0.5)
        try:
            Description=""
            Message=""
            On_Duty_Role=ctx.guild.get_role(Configuration.On_Duty_Role[Functions.Configuration_Position(ctx.guild.id)])
            Index=0
            for Staff_Member in On_Duty_Role.members:
                Index+=1
                Message+=f"{Index}. {Staff_Member.mention}\n"
            if Message=="":
                Message="There are currently no Staff Members On Duty\n"
            Description+=f"__**On Duty Staff:**__\n{Message}"
            Message=""
            for Fleet in self.Active_Fleets:
                Position=self.Active_Fleets.index(Fleet)
                Fleet_Ships=[ctx.guild.get_channel(self.Fleet_Vc_1[Functions.Configuration_Position(ctx.guild.id)][Position]),ctx.guild.get_channel(self.Fleet_Vc_2[Functions.Configuration_Position(ctx.guild.id)][Position]),ctx.guild.get_channel(self.Fleet_Vc_3[Functions.Configuration_Position(ctx.guild.id)][Position]),ctx.guild.get_channel(self.Fleet_Vc_4[Functions.Configuration_Position(ctx.guild.id)][Position]),ctx.guild.get_channel(self.Fleet_Vc_5[Functions.Configuration_Position(ctx.guild.id)][Position]),ctx.guild.get_channel(self.Fleet_Vc_6[Functions.Configuration_Position(ctx.guild.id)][Position])]
                Message+=f"\n\n**Fleet {Fleet}:**"
                Current_Message=Message
                for Ship in Fleet_Ships:
                    Require_Crew=""
                    if "[CLOSED]" not in Ship.name:
                        Emoji=""
                        if Ship.user_limit==4:
                            Emoji="<:ship_Galleon:944298920215986236>"
                        if Ship.user_limit==3:
                            Emoji="<:ship_Brigantine:944298920417321030>"
                        if Ship.user_limit==2:
                            Emoji="<:ship_Sloop:944298920081780799>"
                        if len(Ship.members)<Ship.user_limit:
                            Require_Crew=f" |  Needs {Ship.user_limit-len(Ship.members)}"
                        Name=Ship.name
                        if "[" and "]" in Name:
                            Position=Name.index("]")
                            Name=Name[Position+2:]
                        Message+=f"\n{Emoji} {Name}{Require_Crew}"
                if Message==Current_Message:
                    Message=Message.replace(f"\n\n**Fleet {Fleet}:**","")
            if Message=="":
                Message="\nThere are currently no active ships"
            Description+=f"\n__**Active Fleet Ships:**__{Message}"
            Active_Ships_Embed=await ctx.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(description=Description,colour=0x00F3FF))
        except:
            Active_Ships_Embed=await ctx.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(description="Description",colour=0x00F3FF))
        Queue_Embed=await ctx.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description,color=0x00F3FF),view=Views.Queue.OpenQueueButtons())
        Configuration_File=open("Cursed_Obsidian/Configuration.py")
        Contents=Configuration_File.readlines()
        Length=len(Contents)
        Configuration_File.close()
        Line=Contents[Length-3]
        Id_List=Line.replace("Queue_Embed=","").replace("[","").replace("]","").split(",")
        Id_List[Functions.Configuration_Position(ctx.guild.id)]=Queue_Embed.id
        New_List=[]
        for Id in Id_List:
            New_List.append(int(Id))
        Contents[Length-3]=f"Queue_Embed={New_List}\n"
        Line=Contents[Length-2]
        Id_List=Line.replace("Active_Ships_Embed=","").replace("[","").replace("]","").split(",")
        Id_List[Functions.Configuration_Position(ctx.guild.id)]=Active_Ships_Embed.id
        New_List=[]
        for Id in Id_List:
            New_List.append(int(Id))
        Contents[Length-2]=f"Active_Ships_Embed={New_List}\n"
        Contents="".join(Contents)
        Configuration_File=open("Cursed_Obsidian/Configuration.py","w",encoding='utf-8')
        Configuration_File.write(Contents)
        Configuration_File.close()
    @Embed_Setup.command(name="spiking-manager")
    @commands.has_any_role("Admin","Development Lead")
    async def spiking_manager(self,ctx):
        await ctx.message.delete(delay=0.5)
        Spiking_Vc=ctx.guild.get_channel(Configuration.Spiking_Vc[Functions.Configuration_Position(ctx.guild.id)])
        Member_Role=ctx.guild.get_role(Configuration.Member_Role[Functions.Configuration_Position(ctx.guild.id)])
        Permissions=Spiking_Vc.overwrites_for(Member_Role)
        if Permissions.view_channel==True:
            Emoji="🔓"
        elif Permissions.view_channel==False:
            Emoji="🔒"
        await ctx.guild.get_channel(Configuration.Spiking_Queue[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(title="Spiking Vc",description=f"The Spiking Vc is currently: {Emoji}",colour=0x00F3FF),view=Views.Channel_Control.Spiking_Control_Button())
        Spiking_Embed=await ctx.guild.get_channel(Configuration.Spiking_Queue[Functions.Configuration_Position(ctx.guild.id)]).send(embed=discord.Embed(title="Spiking Queue",description=f"Join {ctx.get_channel((Configuration.Spiking_Vc)[Functions.Configuration_Position(ctx.guild.id)]).mention} to join this Queue.\n\n**Capacity: 0 / 99**",color=0x00F3FF))
        Configuration_File=open("Cursed_Obsidian/Configuration.py")
        Contents=Configuration_File.readlines()
        Length=len(Contents)
        Configuration_File.close()
        Line=Contents[Length-1]
        Id_List=Line.replace("Spiking_Embed=","").replace("[","").replace("]","").split(",")
        Id_List[Functions.Configuration_Position(ctx.guild.id)]=Spiking_Embed.id
        New_List=[]
        for Id in Id_List:
            New_List.append(int(Id))
        Contents[Length-1]=f"Spiking_Embed={New_List}\n"
        Contents="".join(Contents)
        Configuration_File=open("Cursed_Obsidian/Configuration.py","w",encoding='utf-8')
        Configuration_File.write(Contents)
        Configuration_File.close()
    async def cog_command_error(self,ctx,error):
        if isinstance(error,app_commands.errors.MissingAnyRole):
            await ctx.author.send("❌ Only Admins can invoke that command!",ephemeral=True)
        else:
            print(error)
async def setup(bot):
    await bot.add_cog(Setup_Commands(bot))