import discord,Configuration,Functions
class ChannelCloseControlButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)   
        self.Circles=["🔴","🟠","🟡","🟢","🔵","🟣"]     
    def Fleet(self,interaction):
        Interaction_Fleet_Number=int(interaction.channel.name.replace("🎛︱fleet-","").replace("-control",""))
        Position=interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(Interaction_Fleet_Number)
        return [interaction.guild.get_channel(interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)][Position])]
    @discord.ui.button(label="Open All",style=discord.ButtonStyle.green,emoji="🔓",custom_id="open_all",row=0)
    async def open_all(self,interaction:discord.Interaction,button:discord.ui.Button):
        Fleet_Channels=self.Fleet(interaction)
        Index=0
        Message=""
        for Channel in Fleet_Channels:
            await Channel.edit(name=f"{self.Circles[Index]}  [RB-B] /rename")
            Index+=1
            Message+=f"{Index}. {Channel.mention} | Open\n"
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Open & Close Configuration Panel",description=f"**Current Channel Status:**\n{Message}",color=0x00F3FF).set_footer(text=f"Latest Action: 🔓 Opened all Fleet 1 channels"))
    @discord.ui.button(label="Close All",style=discord.ButtonStyle.red,emoji="🔒",custom_id="close_all",row=0)
    async def close_all(self,interaction:discord.Interaction,button:discord.ui.Button):
        Fleet_Channels=self.Fleet(interaction)
        Index=0
        Message=""
        for Channel in Fleet_Channels:
            await Channel.edit(name=f"{self.Circles[Index]}[CLOSED]")
            Index+=1
            Message+=f"{Index}. {Channel.mention} | Closed\n"
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Open & Close Configuration Panel",description=f"**Current Channel Status:**\n{Message}",color=0x00F3FF).set_footer(text=f"Latest Action: 🔒 Closed all Fleet 1 channels"))
    def Status_Message(self,Fleet_Channels):
        Index=0
        Message=""
        for Channel in Fleet_Channels:
            Index+=1
            if "[CLOSED]" in Channel.name:
                Status="Closed"
            else:
                Status="Open"
            Message+=f"{Index}. {Channel.mention} | {Status}\n"
        return Message
    async def Vc_Control(self,interaction,Ship_Number):
        Fleet_Channels=self.Fleet(interaction)
        if "[CLOSED]" in Fleet_Channels[Ship_Number].name:
            if Ship_Number==5:
                Ship_Type="S"
            else:
                Ship_Type="B"
            await Fleet_Channels[Ship_Number].edit(name=f"{self.Circles[Ship_Number]} [RB-{Ship_Type}] /rename")
            Footer=f"Latest Action: {self.Circles[Ship_Number]} VC is now open"
        else:
            await Fleet_Channels[Ship_Number].edit(name=f"{self.Circles[Ship_Number]}[CLOSED]")
            Footer=f"Latest Action: {self.Circles[Ship_Number]} VC is now closed"
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Open & Close Configuration Panel",description=f"**Current Channel Status:**\n{self.Status_Message(Fleet_Channels)}",color=0x00F3FF).set_footer(text=Footer))
    @discord.ui.button(label="Open/Close VC",style=discord.ButtonStyle.blurple,emoji="🔴",custom_id="open_close_red",row=1)
    async def open_close_red(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Vc_Control(interaction,0)
    @discord.ui.button(label="Open/Close VC",style=discord.ButtonStyle.blurple,emoji="🟠",custom_id="open_close_orange",row=1)
    async def open_close_orange(self, interaction:discord.Interaction,button:discord.ui.Button):
        await self.Vc_Control(interaction,1)
    @discord.ui.button(label="Open/Close VC",style=discord.ButtonStyle.blurple,emoji="🟡",custom_id="open_close_yellow",row=2)
    async def open_close_yellow(self, interaction:discord.Interaction,button:discord.ui.Button):
        await self.Vc_Control(interaction,2)
    @discord.ui.button(label="Open/Close VC",style=discord.ButtonStyle.blurple,emoji="🟢",custom_id="open_close_green",row=2)
    async def open_close_green(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Vc_Control(interaction,3)
    @discord.ui.button(label="Open/Close VC",style=discord.ButtonStyle.blurple,emoji="🔵",custom_id="open_close_blue",row=3)
    async def open_close_blue(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Vc_Control(interaction,4)
    @discord.ui.button(label="Open/Close VC",style=discord.ButtonStyle.blurple,emoji="🟣",custom_id="open_close_purple",row=3)
    async def open_close_purple(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Vc_Control(interaction,5)
    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.blurple,emoji="🔁",custom_id="open_close_refresh",row=0)
    async def refresh(self,interaction:discord.Interaction,button:discord.ui.Button):
        Fleet_Channels=self.Fleet(interaction)    
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Open & Close Configuration Panel",description=f"**Current Channel Status:**\n{self.Status_Message(Fleet_Channels)}",color=0x00F3FF).set_footer(text="Latest Action: 🔁 Refreshed"))
class ChannelLockControlButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.Circles=["🔴","🟠","🟡","🟢","🔵","🟣"]
    def Fleet(self,interaction):
        Interaction_Fleet_Number=int(interaction.channel.name.replace("🎛︱fleet-","").replace("-control",""))
        Position=interaction.client.Active_Fleets[Functions.Configuration_Position(interaction.guild.id)].index(Interaction_Fleet_Number)
        return [interaction.guild.get_channel(interaction.client.Fleet_Vc_1[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_2[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_3[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_4[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_5[Functions.Configuration_Position(interaction.guild.id)][Position]),interaction.guild.get_channel(interaction.client.Fleet_Vc_6[Functions.Configuration_Position(interaction.guild.id)][Position])]
    def Status_Message(self,Fleet_Channels,Role):
        Index=0
        Message=""
        for Channel in Fleet_Channels:
            Index+=1
            Permissions=Channel.overwrites_for(Role)
            if Permissions.connect==False:
                Status="🔒"
            if Permissions.connect==True:
                Status="🔓"
            Message+=f"{Index}. {Channel.mention} | {Status}\n"
        return Message
    @discord.ui.button(label="Unlock All",style=discord.ButtonStyle.green,emoji="🔓",custom_id="unlock_all",row=0)
    async def unlock_all(self,interaction:discord.Interaction,button:discord.ui.Button):
        Fleet_Channels=self.Fleet(interaction)
        Index=0
        Message=""
        for Channel in Fleet_Channels:
            Permissions=Channel.overwrites_for(interaction.guild.default_role)
            Permissions.connect=True
            Permissions.view_channel=True
            await Channel.set_permissions(interaction.guild.default_role,overwrite=Permissions)
            Index+=1
            Message+=f"{Index}. {Channel.mention} | 🔓\n"
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Status & Configuration Panel",description=f"**Current Channel Status:**\n{Message}",color=0x00F3FF).set_footer(text=f"Latest Action: 🔓 Unlocked all Fleet 1 channels"))
    @discord.ui.button(label="Lock All",style=discord.ButtonStyle.red,emoji="🔒",custom_id="lock_all",row=0)
    async def lock_all(self,interaction:discord.Interaction,button:discord.ui.Button):
        Fleet_Channels=self.Fleet(interaction)
        Index=0
        Message=""
        for Channel in Fleet_Channels:
            Permissions=Channel.overwrites_for(interaction.guild.default_role)
            Permissions.connect=False
            Permissions.view_channel=False
            await Channel.set_permissions(interaction.guild.default_role,overwrite=Permissions)
            Index+=1
            Message+=f"{Index}. {Channel.mention} | 🔒\n"
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Status & Configuration Panel",description=f"**Current Channel Status:**\n{Message}",color=0x00F3FF).set_footer(text=f"Latest Action: 🔒 All Fleet 1 channels are now locked"))
    async def Permission_Checker(self,interaction,Ship_Number):
        Fleet_Channels=self.Fleet(interaction)
        Permissions=Fleet_Channels[Ship_Number].overwrites_for(interaction.guild.default_role)
        if Permissions.connect==True:
            Permissions.connect=False
            Permissions.view_channel=False
            Footer=f"Latest Action: {self.Circles[Ship_Number]} VC is now locked"
        elif Permissions.connect==False:
            Permissions.connect=True
            Permissions.view_channel=True
            Footer=f"Latest Action: {self.Circles[Ship_Number]} VC is now unlocked"
        await Fleet_Channels[Ship_Number].set_permissions(interaction.guild.default_role,overwrite=Permissions)        
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Status & Configuration Panel",description=f"**Current Channel Status:**\n{self.Status_Message(Fleet_Channels,interaction.guild.default_role)}",color=0x00F3FF).set_footer(text=Footer))
    @discord.ui.button(label="Lock/Unlock VC",style=discord.ButtonStyle.blurple,emoji="🔴",custom_id="lock_unlock_red",row=1)
    async def lock_unlock_red(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Permission_Checker(interaction,0)
    @discord.ui.button(label="Lock/Unlock VC",style=discord.ButtonStyle.blurple,emoji="🟠",custom_id="lock_unlock_orange",row=1)
    async def lock_unlock_orange(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Permission_Checker(interaction,1)
    @discord.ui.button(label="Lock/Unlock VC",style=discord.ButtonStyle.blurple,emoji="🟡",custom_id="lock_unlock_yellow",row=2)
    async def lock_unlock_yellow(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Permission_Checker(interaction,2)
    @discord.ui.button(label="Lock/Unlock VC",style=discord.ButtonStyle.blurple,emoji="🟢",custom_id="lock_unlock_green",row=2)
    async def lock_unlock_green(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Permission_Checker(interaction,3)
    @discord.ui.button(label="Lock/Unlock VC",style=discord.ButtonStyle.blurple,emoji="🔵",custom_id="lock_unlock_blue",row=3)
    async def lock_unlock_blue(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Permission_Checker(interaction,4)
    @discord.ui.button(label="Lock/Unlock VC",style=discord.ButtonStyle.blurple,emoji="🟣",custom_id="lock_unlock_purple",row=3)
    async def lock_unlock_purple(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.Permission_Checker(interaction,5)
    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.gray,emoji="🔁",custom_id="refresh",row=0)
    async def refresh(self,interaction:discord.Interaction,button:discord.ui.Button):
        Fleet_Channels=self.Fleet(interaction)
        Index=0
        Message=""
        for Channel in Fleet_Channels:
            Permissions=Channel.overwrites_for(interaction.guild.default_role)
            Index+=1
            if Permissions.connect==False:
                Status="🔒"
            if Permissions.connect==True:
                Status="🔓"
            Message+=f"{Index}. {Channel.mention} | {Status}\n"
        await interaction.response.edit_message(embed=discord.Embed(title="Fleet Voice Channel Status & Configuration Panel",description=f"**Current Channel Status:**\n{Message}",color=0x00F3FF).set_footer(text="Latest Action: 🔁 Refreshed"))
class Spiking_Control_Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Lock/Unlock VC",style=discord.ButtonStyle.blurple,custom_id="Spiking_Vc_Control")
    async def spiking(self,interaction:discord.Interaction,button:discord.ui.Button):
        Spiking_Vc=interaction.guild.get_channel(Configuration.Spiking_Vc[Functions.Configuration_Position(interaction.guild.id)])
        Member_Role=interaction.guild.get_role(Configuration.Member_Role[Functions.Configuration_Position(interaction.guild.id)])
        Development_Lead=interaction.guild.get_role(Configuration.Development_Lead[Functions.Configuration_Position(interaction.guild.id)])
        Member_Role_Permissions=Spiking_Vc.overwrites_for(Member_Role)
        Development_Lead_Permissions=Spiking_Vc.overwrites_for(Development_Lead)
        if Member_Role_Permissions.view_channel==True:
            Member_Role_Permissions.view_channel=False
            Development_Lead_Permissions.view_channel=False
            Status="Locked"
            Emoji="🔒"
        elif Member_Role_Permissions.view_channel==False:
            Member_Role_Permissions.view_channel=True
            Development_Lead_Permissions.view_channel=True
            Status="Unlocked"
            Emoji="🔓"
        Footer=f"{Emoji} {interaction.user.name} {Status} the Spiking VC"
        await Spiking_Vc.set_permissions(Member_Role,overwrite=Member_Role_Permissions)
        await Spiking_Vc.set_permissions(Development_Lead,overwrite=Development_Lead_Permissions)
        await interaction.response.edit_message(embed=discord.Embed(title="Spiking Vc",description=f"The Spiking Vc is currently: {Emoji}",colour=0x00F3FF).set_footer(text=Footer))
        Log_channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_channel.send(embed=discord.Embed(description=f"{interaction.user.mention} `{Status}` the Spiking VC"))