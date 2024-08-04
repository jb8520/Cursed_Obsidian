import discord,Configuration,Functions
from discord.ext import commands
class DutySwitchButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    def On_Duty_Message(self,On_Duty_Role):
        Index=0
        Message=""
        for member in On_Duty_Role.members:
            Index+=1
            Message+=f"{Index}. {member.mention}\n"
        if Index==0:
            Message="None"
        return Message
    @discord.ui.button(label="Apply for On-Duty",style=discord.ButtonStyle.green,custom_id="apply_duty")
    async def apply_duty(self,interaction:discord.Interaction,button:discord.ui.Button):
        On_Duty_Role=interaction.guild.get_role(Configuration.On_Duty_Role[Functions.Configuration_Position(interaction.guild.id)])
        if On_Duty_Role in interaction.user.roles:
            await interaction.response.send_message(f"❌ You already have {On_Duty_Role.mention} role",ephemeral=True)
            return
        await interaction.user.add_roles(On_Duty_Role)
        await interaction.response.edit_message(embed=discord.Embed(description=f"Get or Drop {On_Duty_Role.mention} role by using the buttons below.\n\n__**Current On-Duty Members:**__\n{self.On_Duty_Message(On_Duty_Role)}",color=0x00F3FF).set_footer(text=f"Latest Action: ✅ {interaction.user.name} joined On Duty team"))
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} applied for `on-duty`."))
    @discord.ui.button(label="Resign from On-Duty",style=discord.ButtonStyle.red,custom_id="resign_duty")
    async def resign_duty(self,interaction:discord.Interaction,button:discord.ui.Button):
        On_Duty_Role=interaction.guild.get_role(Configuration.On_Duty_Role[Functions.Configuration_Position(interaction.guild.id)])
        if On_Duty_Role not in interaction.user.roles:
            await interaction.response.send_message(f"❌ You don't have {On_Duty_Role.mention} role",ephemeral=True)
            return
        await interaction.user.remove_roles(On_Duty_Role)
        await interaction.response.edit_message(embed=discord.Embed(title="Duty Switch Configuration Panel",description=f"Get or Drop {On_Duty_Role.mention} role by using the buttons below.\n\n__**Current On-Duty Members:**__\n{self.On_Duty_Message(On_Duty_Role)}",color=0x00F3FF).set_footer(text=f"Latest Action: ⛔ {interaction.user.name} resigned from On Duty team"))
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} resigned from `on-duty`."))
    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.blurple,emoji="🔁",custom_id="refresh_duty")
    async def refresh_duty(self,interaction:discord.Interaction,button:discord.ui.Button):
        On_Duty_Role=interaction.guild.get_role(Configuration.On_Duty_Role[Functions.Configuration_Position(interaction.guild.id)])
        await interaction.response.edit_message(embed=discord.Embed(title="Duty Switch Configuration Panel",description=f"Get or Drop {On_Duty_Role.mention} role by using the buttons below.\n\n__**Current On-Duty Members:**__\n{self.On_Duty_Message(On_Duty_Role)}",color=0x00F3FF).set_footer(text=f"Latest Action: 🔄 Refreshed"))
class InactiveStaff(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    def Inactive_Staff_Message(self,Inactive_Staff_Role):
        Index=0
        Message=""
        for Member in Inactive_Staff_Role.members:
            Index+=1
            Message+=f"{Index}. {Member.mention}\n"
        if Index==0:
            Message="None"
        return Message
    @discord.ui.button(label="Apply for Inactive role",style=discord.ButtonStyle.green,custom_id="apply_inactive")
    async def apply_inactive(self,interaction:discord.Interaction,button:discord.ui.Button):
        Inactive_Staff_Role=interaction.guild.get_role(Configuration.Inactive_Staff_Role[Functions.Configuration_Position(interaction.guild.id)])
        if Inactive_Staff_Role in interaction.user.roles:
            await interaction.response.send_message(f"❌ You already have {Inactive_Staff_Role.mention} role",ephemeral=True)
            return
        await interaction.user.add_roles(Inactive_Staff_Role)
        for Staff_Role_Id in Configuration.Staff_Roles_List[Functions.Configuration_Position(interaction.guild.id)]:
            Staff_Role=interaction.guild.get_role(Staff_Role_Id)
            if Staff_Role in interaction.user.roles:
                await interaction.user.remove_roles(Staff_Role)
        await interaction.response.edit_message(embed=discord.Embed(title="Inactive role selection",description=f"Apply for {Inactive_Staff_Role.mention} role by using the green button below.\nIf you want to rejoin staff in the future, you will need to open a ticket in <#935566068762681394>\n\n**Staff members who are inactive for more than 30 days will automatically be given this role.**\n\n__**Current Inactive Staff Members:**__\n\n{self.Inactive_Staff_Message(Inactive_Staff_Role)}",color=0x00F3FF).set_footer(text=f"Latest Action: ✅ {interaction.user.name} is now Inactive"))
        Log_Channel=interaction.guild.get_channel(Configuration.Bot_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Log_Channel.send(embed=discord.Embed(description=f"{interaction.user.mention} joined `inactive staff`."))
    @discord.ui.button(label="Refresh",style=discord.ButtonStyle.blurple,emoji="🔁",custom_id="refresh_inactive")
    async def refresh_inactive(self,interaction:discord.Interaction,button:discord.ui.Button):
        Inactive_Staff_Role=interaction.guild.get_role(Configuration.Inactive_Staff_Role[Functions.Configuration_Position(interaction.guild.id)])
        await interaction.response.edit_message(embed=discord.Embed(title="Inactive role selection",description=f"Apply for {Inactive_Staff_Role.mention} role by using the green button below.\nIf you want to rejoin staff in the future, you will need to open a ticket in <#935566068762681394>\n\n**Staff members who are inactive for more than 30 days will automatically be given this role.**\n\n__**Current Inactive Staff Members:**__\n\n{self.Inactive_Staff_Message(Inactive_Staff_Role)}",color=0x00F3FF).set_footer(text=f"Latest Action: 🔄 Refreshed"))
class Fleet_Roles(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.Active_Fleets=bot.Active_Fleets
        self.Fleet_Roles=bot.Fleet_Roles
        self.Fleet_Vc_1=bot.Fleet_Vc_1
        self.Fleet_Vc_2=bot.Fleet_Vc_2
        self.Fleet_Vc_3=bot.Fleet_Vc_3
        self.Fleet_Vc_4=bot.Fleet_Vc_4
        self.Fleet_Vc_5=bot.Fleet_Vc_5
        self.Fleet_Vc_6=bot.Fleet_Vc_6
    @commands.Cog.listener("on_voice_state_update")
    async def voice_update_(self,member:discord.Member,before,after):
        for Position in range(len(self.Active_Fleets[Functions.Configuration_Position(member.guild.id)])):
            Fleet_Ships=[member.guild.get_channel(self.Fleet_Vc_1[Functions.Configuration_Position(member.guild.id)][Position]),member.guild.get_channel(self.Fleet_Vc_2[Functions.Configuration_Position(member.guild.id)][Position]),member.guild.get_channel(self.Fleet_Vc_3[Functions.Configuration_Position(member.guild.id)][Position]),member.guild.get_channel(self.Fleet_Vc_4[Functions.Configuration_Position(member.guild.id)][Position]),member.guild.get_channel(self.Fleet_Vc_5[Functions.Configuration_Position(member.guild.id)][Position]),member.guild.get_channel(self.Fleet_Vc_6[Functions.Configuration_Position(member.guild.id)][Position])]
            Fleet_Role=member.guild.get_role(self.Fleet_Roles[Functions.Configuration_Position(member.guild.id)][Position])
            for Channel in Fleet_Ships:
                if before.channel!=after.channel and before.channel==Channel:
                    await member.remove_roles(Fleet_Role)
                    break
            for Channel in Fleet_Ships:
                if before.channel!=after.channel and after.channel==Channel:
                    await member.add_roles(Fleet_Role)
                    break
async def setup(bot):
    await bot.add_cog(Fleet_Roles(bot))