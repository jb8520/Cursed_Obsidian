import discord,Configuration,Functions,datetime
class ActivityModal(discord.ui.Modal,title="Join Fleet Queue"):
    Activity=discord.ui.TextInput(label="TYPE YOUR DESIRED ACTIVITY",style=discord.TextStyle.short,placeholder="You can change this at any time later using the button without losing your place in the queue",required=True)
    async def on_submit(self,interaction:discord.Interaction):
        Log_Channel=interaction.guild.get_channel(Configuration.Queue_Logs[Functions.Configuration_Position(interaction.guild.id)])
        if interaction.user.id in interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)]:
            Position=interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].index(interaction.user.id)
            interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)][Position]=f"{self.Activity}"
            Position=interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].index(interaction.user.id)
            Activity=interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)][Position]
            await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} updated their activity to {Activity}."))
        else:
            interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].append(interaction.user.id)
            interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].append(f"{self.Activity}")
            interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].append(f"<t:{int(datetime.datetime.timestamp(datetime.datetime.now()))}:R>")
            Queue_Role=interaction.guild.get_role(Configuration.Queue[Functions.Configuration_Position(interaction.guild.id)])
            await interaction.user.add_roles(Queue_Role)
            Position=interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].index(interaction.user.id)
            Activity=interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)][Position]
            await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} queued for {Activity}."))
        Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
        await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description+Functions.Queue_Display(interaction),colour=0x00F3FF))
        await interaction.response.send_message("✅ Success!",ephemeral=True)
class OpenQueueButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Join Queue/Update Queue",style=discord.ButtonStyle.green,custom_id="join_queue",row=1)
    async def join_queue(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.guild.get_role(Configuration.Member_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles:
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
            return
        await interaction.response.send_modal(ActivityModal())
    @discord.ui.button(label="Leave Queue",style=discord.ButtonStyle.red,custom_id="leave_queue",row=1)
    async def leave_queue(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.guild.get_role(Configuration.Member_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles:
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
            return
        if interaction.user.id not in interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)]:
            await interaction.response.send_message(f"**{interaction.user.name}**, you aren't in the queue!",ephemeral=True)
        else:
            Position=interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].index(interaction.user.id)
            interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
            interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
            interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].pop(Position)
            Queue_Role=interaction.guild.get_role(Configuration.Queue[Functions.Configuration_Position(interaction.guild.id)])
            await interaction.user.remove_roles(Queue_Role)
            Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
            await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description+Functions.Queue_Display(interaction),colour=0x00F3FF))
            await interaction.response.send_message("✅ Success!",ephemeral=True)
            Log_Channel=interaction.guild.get_channel(Configuration.Queue_Logs[Functions.Configuration_Position(interaction.guild.id)])
            await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} left the queue."))
    @discord.ui.button(label="Leave Ship",style=discord.ButtonStyle.blurple,custom_id="leave_ship",row=2)
    async def leave_ship(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.guild.get_role(Configuration.Member_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles:
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
            return
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
    @discord.ui.button(label="Disconnected",style=discord.ButtonStyle.grey,custom_id="disconnect",row=2)
    async def disconnect(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.guild.get_role(Configuration.Member_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Role[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles:
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
            return
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        On_Duty_Channel=interaction.guild.get_channel(Configuration.On_Duty_Chat[Functions.Configuration_Position(interaction.guild.id)])
        On_Duty_Role=interaction.guild.get_role(Configuration.On_Duty_Role[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} used `/disconnect`."))
        await On_Duty_Channel.send(f"{On_Duty_Role.mention} {interaction.user.mention} has been disconnected from their ship.")
        await interaction.response.send_message("✅ Please join the waiting room & wait to be moved.",ephemeral=True)
class ClosedQueueButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Queue",style=discord.ButtonStyle.green,emoji="🔓",custom_id="open_queue")
    async def open_queue(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][0]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][1]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][2]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][3]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Development_Lead[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles:
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
            return
        Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
        await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description,colour=0x00F3FF),view=OpenQueueButtons())
        await interaction.response.edit_message(embed=discord.Embed(title="Staff Queue Buttons",description="Use the Buttons below to control the queue",color=0x00F3FF).set_footer(text=f"Latest Action: ✅ Queue opened by {interaction.user.name}"),view=StaffQueueButtons())
        interaction.client.Queue_State[Functions.Configuration_Position(interaction.guild.id)]="open"
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} `opened` the queue."))
class StaffQueueButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.blurple,emoji="🔄",custom_id="refresh_queue")
    async def refresh_queue(self,interaction:discord.Interaction,button:discord.ui.Button):
        Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
        await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description+Functions.Queue_Display(interaction),colour=0x00F3FF))
        await interaction.response.edit_message(embed=discord.Embed(title="Staff Queue Buttons",description="Use the Buttons below to control the queue",color=0x00F3FF).set_footer(text=f"Latest Action: 🔁 refreshed the queue"))
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} `refreshed` the queue."))
    @discord.ui.button(label="Close Queue",style=discord.ButtonStyle.red,emoji="🔒",custom_id="close_queue")
    async def close_queue(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][0]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][1]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][2]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][3]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Development_Lead[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles:
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
            return
        Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
        await Queue_Embed.edit(embed=discord.Embed(title="__**Cursed Obsidian Queue**__",description="The queue is currently closed",colour=discord.Colour.red()),view=None)
        await interaction.response.edit_message(embed=discord.Embed(title="Staff Queue Buttons",description="Use the Buttons below to control the queue",color=0x00F3FF).set_footer(text=f"Latest Action: ❌ Queue closed by {interaction.user.name}"),view=ClosedQueueButton())
        interaction.client.Queue_State[Functions.Configuration_Position(interaction.guild.id)]="closed"
        interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        Queue_Role=interaction.guild.get_role(Configuration.Queue[Functions.Configuration_Position(interaction.guild.id)])
        for Member in Queue_Role.members:
            await Member.remove_roles(Queue_Role)
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} `closed` the queue."))  
    @discord.ui.button(label="Clear Queue",style=discord.ButtonStyle.gray,emoji="🧹",custom_id="clear_queue")
    async def clear_queue(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][0]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][1]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][2]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)][3]) not in interaction.user.roles and interaction.guild.get_role(Configuration.Development_Lead[Functions.Configuration_Position(interaction.guild.id)]) not in interaction.user.roles:
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
            return
        Queue_Embed=await interaction.guild.get_channel(Configuration.Join_Queue[Functions.Configuration_Position(interaction.guild.id)]).fetch_message(Configuration.Queue_Embed[Functions.Configuration_Position(interaction.guild.id)])
        await Queue_Embed.edit(embed=discord.Embed(title=Configuration.Queue_Title,description=Configuration.Queue_Description,colour=0x00F3FF))
        await interaction.response.edit_message(embed=discord.Embed(title="Staff Queue Buttons",description="Use the Buttons below to control the queue",color=0x00F3FF).set_footer(text=f"Latest Action: 🧹 Queue cleared by {interaction.user.name}"))
        interaction.client.Queue_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Activity_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        interaction.client.Timestamp_List[Functions.Configuration_Position(interaction.guild.id)].clear()
        Queue_Role=interaction.guild.get_role(Configuration.Queue[Functions.Configuration_Position(interaction.guild.id)])
        for Member in Queue_Role.members:
            await Member.remove_roles(Queue_Role)
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} `cleared` the queue."))