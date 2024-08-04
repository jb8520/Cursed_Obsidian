import discord,datetime,Configuration,Functions,Views.Channel_Control,Views.Queue
from discord import app_commands
from discord.ext import commands,tasks
class Staff_Commands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.Fleet_Status_Message=bot.Fleet_Status_Message
        self.Active_Fleets=bot.Active_Fleets
        self.Fleet_Vc_1=bot.Fleet_Vc_1
        self.Fleet_Vc_2=bot.Fleet_Vc_2
        self.Fleet_Vc_3=bot.Fleet_Vc_3
        self.Fleet_Vc_4=bot.Fleet_Vc_4
        self.Fleet_Vc_5=bot.Fleet_Vc_5
        self.Fleet_Vc_6=bot.Fleet_Vc_6
        self.Time=bot.Time
    @tasks.loop(minutes=1)
    async def Fleet_Status(self):
        for Server in self.Fleet_Status_Message:
            Description=""
            Message=""
            Guild=self.bot.get_guild(Functions.Guild_Id(Server))
            On_Duty_Role=Guild.get_role(Configuration.On_Duty_Role[Server])
            Index=0
            for Staff_Member in On_Duty_Role.members:
                Index+=1
                Message+=f"{Index}. {Staff_Member.mention}\n"
            if Message=="":
                Message="There are currently no Staff Members On Duty\n"
            Description+=f"__**On Duty Staff:**__\n{Message}"
            Message=""
            for Fleet in self.Active_Fleets[Server]:
                Position=self.Active_Fleets[Server].index(Fleet)
                Fleet_Ships=[self.bot.get_channel(self.Fleet_Vc_1[Server][Position]),self.bot.get_channel(self.Fleet_Vc_2[Server][Position]),self.bot.get_channel(self.Fleet_Vc_3[Server][Position]),self.bot.get_channel(self.Fleet_Vc_4[Server][Position]),self.bot.get_channel(self.Fleet_Vc_5[Server][Position]),self.bot.get_channel(self.Fleet_Vc_6[Server][Position])]
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
            Active_Ships_Embed=await self.bot.get_channel(Configuration.Join_Queue[Server]).fetch_message(Configuration.Active_Ships_Embed[Server])
            await Active_Ships_Embed.edit(embed=discord.Embed(description=Description,colour=0x00F3FF))
    @app_commands.command(name="apply",description="Admin Only | Sends the staff recruitment message")
    @app_commands.checks.has_any_role("Admin","Development Lead")
    async def apply(self,interaction:discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(title="<a:cheergi:1044959262796943461>__**HELP WANTED**__<a:cheergi:1044959262796943461>",description=f"<a:speed_L:1058114911877746758>__**Join our Team**__<a:speed_R:1058114924724879430>\nWe are looking for individuals who are active, responsible, and committed to helping our community thrive. To apply, open an application in {interaction.guild.get_channel(Configuration.Apply_For_Staff[Functions.Configuration_Position(interaction.guild.id)]).mention}.\n\n<a:speed_L:1058114911877746758>__**Helper Duties**__<a:speed_R:1058114924724879430>\nYour main duty as staff is to help spike servers and monitor our fleet queue, which are some of the most important tasks.\n\n<a:speed_L:1058114911877746758>__**Requirements**__<a:speed_R:1058114924724879430>\n- Active member in our server for 2 weeks.\n- Must have 2-factor authentication enabled on Discord.\n\n<a:speed_L:1058114911877746758>__**Benefits**__<a:speed_R:1058114924724879430>\n- Learn new skills, such as moderation and community management, that can be transferred to other areas in life.\n- Staff members are leaders within the server, and this experience can be valuable in developing leadership skills.\n- Contributing to the success and growth of a server can bring a sense of fulfillment and satisfaction.",color=0x00F3FF).set_image(url="https://cdn.discordapp.com/attachments/987840022076080229/1037425048706895932/apply-staff.png"))
    @app_commands.command(name="startup")
    @app_commands.checks.has_any_role("Admin","Moderator","Development Lead")
    async def startup(self,interaction:discord.Interaction):
        Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
        Queue_Title=Queue_Embed.embeds[0].title
        interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        if Queue_Title==Configuration.Queue_Title:
            interaction.client.Queue_State[Functions.Configuration_Position(interaction.guild.id)]="open"
            Description=Queue_Embed.embeds[0].description
            if Description!=Configuration.Queue_Description:
                Description=Description.split("**MEMBERS CURRENTLY IN QUEUE:**\n",1)[1].split("\n")
                for i in range(len(Description)):
                    Description[i]=Description[i][5:]
                    Position=Description[i].index("> ")
                    interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].append(int(Description[i][:Position]))
                    Description[i]=Description[i][Position+1:]
                    Position=len(Description[i])-Description[i].find("<t:")
                    interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].append(Description[i][-Position:])
                    Description[i]=Description[i][3:-3-Position]
                    interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].append(Description[i])
            Queue_Description=Configuration.Queue_Description+Functions.Queue_Display(interaction)
            Colour=0x00F3FF
        else:
            Queue_Title="__**Cursed Obsidian Queue**__"
            Queue_Description="The queue is currently closed"
            Colour=discord.Colour.red()
            interaction.client.Queue_State[Functions.Configuration_Position(interaction.guild.id)]="closed"
        await Queue_Embed.edit(embed=discord.Embed(title=Queue_Title,description=Queue_Description,colour=Colour))
        interaction.client.Fleet_Status_Message.append(Functions.Configuration_Position(interaction.guild.id))
        interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Categories[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Controls[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Chats[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)].clear()
        Categories=interaction.guild.categories
        for Category in Categories:
            if "✦ 𝙁𝙇𝙀𝙀𝙏 " in Category.name:
                if Category.name not in ["✦ 𝙁𝙇𝙀𝙀𝙏 | 𝙎𝙏𝘼𝙁𝙁-𝙊𝙉𝙇𝙔 ✦","✦ 𝙁𝙇𝙀𝙀𝙏 𝙌𝙐𝙀𝙐𝙀 ✦"]:
                    interaction.client.Fleet_Categories[Functions.Configuration_Position(interaction.guild.id)].append(Category.id)
                    Fleet_Number=Category.name.replace("✦ 𝙁𝙇𝙀𝙀𝙏 ","").replace(" ✦","")
                    interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].append(int(Fleet_Number))
                    Roles=interaction.guild.roles
                    for Role in Roles:
                        if f"fleet{Fleet_Number}"==Role.name:
                            interaction.client.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)].append(Role.id)
                            break
                    for Channel in Category.channels:
                        if Channel.name==f"💬︱fleet{Fleet_Number}-chat":
                            interaction.client.Fleet_Chats[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
                        elif Channel.name==f"🎛︱fleet-{Fleet_Number}-control":
                            interaction.client.Fleet_Controls[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
                        elif "🔴" in Channel.name:
                            interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
                        elif "🟠" in Channel.name:
                            interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
                        elif "🟡" in Channel.name:
                            interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
                        elif "🟢" in Channel.name:
                            interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
                        elif "🔵" in Channel.name:
                            interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
                        elif "🟣" in Channel.name:
                            interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)].append(Channel.id)
        await interaction.response.send_message("✅ Success!",ephemeral=True)
        if self.Fleet_Status.is_running()==False:
            await self.Fleet_Status.start()
        Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_channel.send(embed=discord.Embed(description=f"{interaction.user.mention} used the `/startup` command"))
    @app_commands.command(name="create",description="Higher Staff Only | Creates a fleet")
    @app_commands.checks.has_any_role("Admin","Moderator","Senior Officer","Development Lead")
    async def create(self,interaction:discord.Interaction):
        Categories=[]
        Count=0
        Fleet=0
        for Category in interaction.guild.categories:
            if "✦ 𝙁𝙇𝙀𝙀𝙏 " in Category.name:
                if Category.name not in ["✦ 𝙁𝙇𝙀𝙀𝙏 | 𝙎𝙏𝘼𝙁𝙁-𝙊𝙉𝙇𝙔 ✦","✦ 𝙁𝙇𝙀𝙀𝙏 𝙌𝙐𝙀𝙐𝙀 ✦"]:
                    Fleet_Number=Category.name.replace("✦ 𝙁𝙇𝙀𝙀𝙏 ","").replace(" ✦","")
                    Categories.append(int(Fleet_Number))
        Categories.sort()
        if Categories==[]:
            Fleet=1
        else:
            for Fleet_Number in Categories:
                Count+=1
                if Fleet_Number!=Count:
                    Fleet=Count
                    break
            if Fleet==0:
                Fleet=Categories[len(Categories)-1]+1
        await interaction.response.send_message("✅ Success!",ephemeral=True)
        Guild_Position=Functions.Configuration_Position(interaction.guild.id)
        if Guild_Position not in interaction.client.Fleet_Status_Message:
            interaction.client.Fleet_Status_Message.append(Guild_Position)
        interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].append(Fleet)
        Fleet_Category_Overwrites={interaction.guild.default_role:discord.PermissionOverwrite(connect=False),interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][2]):discord.PermissionOverwrite(connect=True,manage_channels=True)}
        Fleet_Category=await interaction.guild.create_category_channel(name=f"✦ 𝙁𝙇𝙀𝙀𝙏 {Fleet} ✦",position=7,overwrites=Fleet_Category_Overwrites)
        interaction.client.Fleet_Categories[Functions.Configuration_Position(interaction.guild.id)].append(Fleet_Category.id)
        Fleet_Role=await interaction.guild.create_role(name=f"fleet{Fleet}",mentionable=True)
        interaction.client.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)].append(Fleet_Role.id)
        Fleet_Chat_Overwrites={interaction.guild.default_role:discord.PermissionOverwrite(view_channel=False,create_instant_invite=False,embed_links=False,use_application_commands=True),Fleet_Role:discord.PermissionOverwrite(view_channel=True),interaction.guild.get_role(Configuration.Staff_Role[Functions.Configuration_Position(interaction.guild.id)]):discord.PermissionOverwrite(view_channel=True)}
        Fleet_Chat=await Fleet_Category.create_text_channel(name=f"💬︱fleet{Fleet}-chat",overwrites=Fleet_Chat_Overwrites)
        interaction.client.Fleet_Chats[Functions.Configuration_Position(interaction.guild.id)].append(Fleet_Chat.id)
        Fleet_Control_Overwrites={interaction.guild.default_role:discord.PermissionOverwrite(view_channel=False,send_messages=False),interaction.guild.get_role(Configuration.Staff_Role[Functions.Configuration_Position(interaction.guild.id)]):discord.PermissionOverwrite(view_channel=True)}
        Fleet_Control=await Fleet_Category.create_text_channel(name=f"🎛︱fleet-{Fleet}-control",overwrites=Fleet_Control_Overwrites)
        interaction.client.Fleet_Controls[Functions.Configuration_Position(interaction.guild.id)].append(Fleet_Control.id)
        Fleet_Vc_Overwrites={interaction.guild.default_role:discord.PermissionOverwrite(view_channel=False,create_instant_invite=False,connect=False,speak=True,stream=True),Fleet_Role:discord.PermissionOverwrite(view_channel=True),interaction.guild.get_role(Configuration.Staff_Role[Functions.Configuration_Position(interaction.guild.id)]):discord.PermissionOverwrite(view_channel=True,connect=True,move_members=True,mute_members=True,deafen_members=True)}
        Vc_1=await Fleet_Category.create_voice_channel(name="🔴[CLOSED]",overwrites=Fleet_Vc_Overwrites,user_limit=3)
        interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)].append(Vc_1.id)
        Vc_2=await Fleet_Category.create_voice_channel(name="🟠[CLOSED]",overwrites=Fleet_Vc_Overwrites,user_limit=3)
        interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)].append(Vc_2.id)
        Vc_3=await Fleet_Category.create_voice_channel(name="🟡[CLOSED]",overwrites=Fleet_Vc_Overwrites,user_limit=3)
        interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)].append(Vc_3.id)
        Vc_4=await Fleet_Category.create_voice_channel(name="🟢[CLOSED]",overwrites=Fleet_Vc_Overwrites,user_limit=3)
        interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)].append(Vc_4.id)
        Vc_5=await Fleet_Category.create_voice_channel(name="🔵[CLOSED]",overwrites=Fleet_Vc_Overwrites,user_limit=3)
        interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)].append(Vc_5.id)
        Vc_6=await Fleet_Category.create_voice_channel(name="🟣[CLOSED]",overwrites=Fleet_Vc_Overwrites,user_limit=2)
        interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)].append(Vc_6.id)
        Fleet_Channels=[Vc_1,Vc_2,Vc_3,Vc_4,Vc_5,Vc_6]
        Index=0
        Close_Control_Message=""
        Lock_Control_Message=""
        for Channel in Fleet_Channels:
            Index+=1
            if "[CLOSED]" in Channel.name:
                Close_Status="Closed"
            else:
                Close_Status="Open"
            Permission=Channel.overwrites_for(interaction.guild.default_role)
            if Permission.connect==False:
                Lock_Status="🔒"
            else:
                Lock_Status="🔓"
            Close_Control_Message+=f"{Index}. {Channel.mention} | {Close_Status}\n"
            Lock_Control_Message+=f"{Index}. {Channel.mention} | {Lock_Status}\n"
        await Fleet_Control.send(embed=discord.Embed(title="Fleet Voice Channel Open & Close Configurationuration Panel",description=f"**Current Channel Status:**\n{Close_Control_Message}",color=0x00F3FF),view=Views.Channel_Control.ChannelCloseControlButtons())
        await Fleet_Control.send(embed=discord.Embed(title="Fleet Voice Channel Status & Configurationuration Panel",description=f"**Current Channel Status:**\n{Lock_Control_Message}",color=0x00F3FF),view=Views.Channel_Control.ChannelLockControlButtons())
        Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_channel.send(embed=discord.Embed(description=f"{interaction.user.mention} created a fleet"))
    @app_commands.command(name="delete",description="Higher Staff Only | Deletes a specific fleet")
    async def delete(self,interaction:discord.Interaction,fleet:int):
        if fleet not in interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            await interaction.response.send_message(f"❌ Fleet {fleet} does not exist!",ephemeral=True)
            return
        await interaction.response.send_message("✅ Success!",ephemeral=True)
        Position=interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(fleet)
        Category=interaction.guild.get_channel(interaction.client.Fleet_Categories[Functions.Configuration_Position(interaction.guild.id)][Position])
        for Channel in Category.channels:
            await Channel.delete()
        await Category.delete()
        await interaction.guild.get_role(interaction.client.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)][Position]).delete()
        Guild_Position=Functions.Configuration_Position(interaction.guild.id)
        if Guild_Position in interaction.client.Fleet_Status_Message:
            interaction.client.Fleet_Status_Message.remove(Guild_Position)
        interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Chats[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Controls[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Roles[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        interaction.client.Fleet_Categories[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
        Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_channel.send(embed=discord.Embed(description=f"{interaction.user.mention} deleted fleet {fleet}"))    
    @app_commands.command(name="rename",description="Staff Only | Rename a specific Fleet Ship.")
    @app_commands.checks.has_any_role("Staff")
    async def rename(self,interaction:discord.Interaction,fleet:int,ship:int,name:str):
        if 1<=ship<=6 and fleet in interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            Position=interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(fleet)
            Fleet_Ships=[interaction.guild.get_channel(interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)][Position])]
            Circles=["🔴","🟠","🟡","🟢","🔵","🟣"]
            await Fleet_Ships[ship-1].edit(name=f"{Circles[ship-1]}{name}")
            await interaction.response.send_message("✅ Success",ephemeral=True)
            Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
            await Log_channel.send(embed=discord.Embed(description=f"{interaction.user.mention} renamed Fleet {fleet} Ship {ship} to `{name}`"))
        else:
            await interaction.response.send_message("❌ Please select from 6 Ship Channels under Fleet 1 or 2",ephemeral=True)
    @app_commands.command(name="ship-size",description="Staff Only | Changes the Ship Size of a specific Fleet Ship.")
    @app_commands.checks.has_any_role("Staff")
    async def ship_size(self,interaction:discord.Interaction,limit:int,fleet:int,ship:int):
        if 1<=ship<=6 and fleet in interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            Position=interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(fleet)
            Fleet_Ships=[interaction.guild.get_channel(interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)][Position])]
            await Fleet_Ships[ship-1].edit(user_limit=limit)
            await interaction.response.send_message("✅ Success",ephemeral=True)
            Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
            await Log_channel.send(embed=discord.Embed(description=f"{interaction.user.mention} set the ship size for Fleet {fleet} Ship {ship} to `{limit}`"))
        else:
            await interaction.response.send_message("❌ Please select from 6 Ship Channels under Fleet 1 or 2",ephemeral=True)
    Staff_Queue_Commands=app_commands.Group(name="queue",description="Staff Only | Manage the join-queue, add/remove members")
    @Staff_Queue_Commands.command(name="remove",description="Staff Only | Remove a specific member from the queue")
    @app_commands.checks.has_any_role("Staff")
    async def remove(self,interaction:discord.Interaction,member:discord.User):
        if interaction.client.Queue_State[Functions.Configuration_Position(interaction.guild.id)]=="open":
            if member.id in interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)]:
                Position=interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].index(member.id)
                interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
                interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
                interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
                Queue_Role=interaction.guild.get_role(Configuration.Queue[Functions.Configuration_Position(interaction.guild.id)])
                await member.remove_roles(Queue_Role)
                Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
                await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description+Functions.Queue_Display(interaction),colour=0x00F3FF))
                await interaction.response.send_message("✅ Success!",ephemeral=True)
                Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
                await Log_channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `queue_remove` for {member}"))
            else:
                await interaction.response.send_message(f"❌ {member.mention} is not in the queue!",ephemeral=True)
        else:
            await interaction.response.send_message("❌ This command can not be used while the queue is closed",ephemeral=True)
    @Staff_Queue_Commands.command(name="insert",description="Staff Only | Insert a specific member into the queue")
    @app_commands.checks.has_any_role("Staff")
    async def insert(self,interaction:discord.Interaction,member:discord.User,position:int,activity:str):
        if interaction.client.Queue_State[Functions.Configuration_Position(interaction.guild.id)]=="open":
            if member.id in interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)]:
                Position=interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].index(member.id)
                interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
                interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
                interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
            else:
                Queue_Role=interaction.guild.get_role(Configuration.Queue[Functions.Configuration_Position(interaction.guild.id)])
                await member.add_roles(Queue_Role)
            interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].insert(position-1,member.id)
            interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].insert(position-1,activity)
            interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].insert(position-1,f"<t:{int(datetime.datetime.timestamp(datetime.datetime.now()))}:R>")
            Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
            await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description+Functions.Queue_Display(interaction),colour=0x00F3FF))
            await interaction.response.send_message("✅ Success!",ephemeral=True)
            Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
            await Log_channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `queue_insert` for {member}"))
        else:
            await interaction.response.send_message("❌ This command can not be used while the queue is closed",ephemeral=True)
    @Staff_Queue_Commands.command(name="process",description="Staff Only | Process members in the queue, once a spot has opened.")
    @app_commands.checks.has_any_role("Staff")
    async def process(self,interaction:discord.Interaction,member:discord.Member,fleet:int,ship:int):
        if interaction.client.Queue_State[Functions.Configuration_Position(interaction.guild.id)]=="closed":
            await interaction.response.send_message("❌ This command can't be used while the queue is closed",ephemeral=True)
            return
        if member.id not in interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)]:
            await interaction.response.send_message(f"❌ {member.mention} isn't in the queue",ephemeral=True)
            return
        if interaction.guild.get_role(Configuration.Xbox_Linked_Role[Functions.Configuration_Position(interaction.guild.id)]) not in member.roles and interaction.guild.get_role(Configuration.Development_Lead[Functions.Configuration_Position(interaction.guild.id)]) not in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} doesn't have the Xbox-Linked Role.",ephemeral=True)
            return
        if interaction.guild.get_role(Configuration.Staff_Verified_Role[Functions.Configuration_Position(interaction.guild.id)]) not in member.roles and interaction.guild.get_role(Configuration.Development_Lead[Functions.Configuration_Position(interaction.guild.id)]) not in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} isn't staff verified. Please verify them with the `/user-check` command.",ephemeral=True)
            return
        if 1<=ship<=6 and fleet in interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)]:
            Position=interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(fleet)
            Fleet_Ships=[interaction.guild.get_channel(interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)][Position])]
            Position=interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].index(member.id)
            interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
            interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
            interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
            Queue_Role=interaction.guild.get_role(Configuration.Queue[Functions.Configuration_Position(interaction.guild.id)])
            await member.remove_roles(Queue_Role)
            Queue_Channel=interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)])
            Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
            Voice_Channel=Fleet_Ships[ship-1]
            await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description+Functions.Queue_Display(interaction),colour=0x00F3FF))
            await interaction.response.send_message("✅ Success",ephemeral=True)
            Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
            await Log_channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `queue_process` for {member.mention} to {Voice_Channel.mention}"))
            Waiting_Channel=interaction.guild.get_channel(Configuration.Waiting_Room[Functions.Configuration_Position(interaction.guild.id)])
            if member not in Waiting_Channel.members:
                def check(Member,before,after):
                    return Member==member and before.channel!=after.channel and after.channel.name==Waiting_Channel.name
                try:
                    Queue_Message=await Queue_Channel.send(content=member.mention,embed=discord.Embed(description=f'A spot has opened up for you in **Fleet {fleet} Ship {Voice_Channel.name}**. Please join the [Alliance Waiting Room](https://discord.com/channels/933896845644689449/934131108356968518) to be moved to your ship.\n\n \n\nYour spot is currently reserved but will expire <t:{int(datetime.datetime.now().timestamp()+180)}:R> if you do not join in time.',color=discord.Color.green()))
                    await self.bot.wait_for("voice_state_update",check=check,timeout=180)
                    await member.move_to(Voice_Channel)
                except:
                    await Queue_Channel.send(embed=discord.Embed(description=f"{member.mention} did not join the vc in time and has been removed from the queue entirely.",color=discord.Color.red()),delete_after=3)
                await Queue_Message.delete()
            else:
                await member.move_to(Voice_Channel)
        else:
            await interaction.response.send_message("❌ Please select from 6 Ship Channels under any active Fleet",ephemeral=True)
    async def cog_app_command_error(self,interaction:discord.Interaction,error):
        if isinstance(error,app_commands.errors.MissingAnyRole):
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
        else:
            print(error)
async def setup(bot):
    await bot.add_cog(Staff_Commands(bot))