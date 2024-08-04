import discord,os,Configuration,Functions,mysql.connector
from discord import app_commands
from discord.ext import commands

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.common.signed_session import SignedSession
from xbox.webapi.scripts import CLIENT_ID as Client_Id,CLIENT_SECRET as Client_Secret

from dotenv import load_dotenv
load_dotenv()

class Friends_Check_Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value=None
    @discord.ui.button(label="Verify",style=discord.ButtonStyle.green)
    async def confirm(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(content="Verification Granted",view=None)
        self.value=True
        self.stop()
    @discord.ui.button(label="Reject",style=discord.ButtonStyle.red)
    async def cancel(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(content="Verification Denied",view=None)
        self.value=False
        self.stop()
class BanList(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    def DataBase_Connection(self):
        return mysql.connector.connect(host=os.environ["DATABASE_HOST"],user=os.environ["DATABASE_USER"],password=os.environ["DATABASE_PASSWORD"],database=os.environ["DATABASE_NAME"])
    @app_commands.command(name="user-check",description="Staff Only | Checks a user against the banlist")
    @app_commands.checks.has_any_role('Staff')
    async def check(self,interaction:discord.Interaction,user:discord.User=None,xbox:str=None):
        Staff_Verified_Role=interaction.guild.get_role(Configuration.Staff_Verified_Role[Functions.Configuration_Position(interaction.guild.id)])
        await interaction.response.defer(ephemeral=True)
        DataBase=self.DataBase_Connection()
        Cursor=DataBase.cursor()
        Friends_Check=False
        Colour=0x02ff00
        Embeds=[]
        Arguments=""
        Message=""
        if user is not None or xbox is not None:
            if user is not None:
                Arguments+=f"Discord User: {user.mention}\n"
                Cursor.execute(f"SELECT * FROM banlist WHERE discord_id='{user.id}'")
                Discord_Fetch=Cursor.fetchall()
                if Discord_Fetch==[]:
                    Message+=f"✅ {user.mention} is not on the banlist\n"
                else:
                    Message+=f"❌ {user.mention} is on the banlist\n"
                    for Ban in Discord_Fetch:
                        Data=[]
                        for i in Ban:
                            Data.append(i)
                        Message+=f"Case Id: {Data[4]}\n"
                    Colour=0xff0000
            if xbox is not None:
                Arguments+=f"Xbox Gamertag: {xbox}"
                Xbox_Query=xbox.replace("'","")
                Cursor.execute(f"SELECT * FROM banlist WHERE xbox_name='{Xbox_Query}'")
                Xbox_Fetch=Cursor.fetchall()
                if Xbox_Fetch==[]:
                    Message+=f"✅ {xbox} is not on the banlist"
                else:
                    Message+=f"❌ {xbox} is on the banlist\n"
                    for Ban in Xbox_Fetch:
                        Data=[]
                        for i in Ban:
                            Data.append(i)  
                        Message+=f"Case Id: {Data[4]}\n"
                    Colour=0xff0000
                async with SignedSession() as Session:
                    Authentication_Manager=AuthenticationManager(Session,Client_Id,Client_Secret,"")
                    with open("tokens.json") as Token_File:
                        Tokens=Token_File.read()
                    Authentication_Manager.oauth=OAuth2TokenResponse.parse_raw(Tokens)
                    try:
                        await Authentication_Manager.refresh_tokens()
                    except:
                        print(f"Could not refresh tokens\nYou might have to delete the tokens file and re-authenticate if refresh token is expired")
                        return
                    with open("tokens.json",mode="w") as Token_File:
                        Token_File.write(Authentication_Manager.oauth.json())
                    try:
                        Xbox_Client=XboxLiveClient(Authentication_Manager)
                        Xbox_User=await Xbox_Client.profile.get_profile_by_gamertag(xbox)
                        Xuid=Xbox_User.profile_users[0].id
                    except:
                        Count=-1
                    try:
                        Friend_list=await Xbox_Client.people.get_friends_by_xuid(Xuid)
                    except:
                        Count=-2
                    else:
                        Friends=[]
                        for Friend in Friend_list.people:
                            Friends.append(Friend.modern_gamertag)
                        Count=0
                        Xbox_Friends_Message=""
                        for Xbox_Gamertag in Friends:
                            Xbox_Query=str(Xbox_Gamertag).replace("'","")
                            Cursor.execute(f"SELECT * FROM banlist WHERE xbox_name='{Xbox_Query}'")
                            Xbox_Fetch=Cursor.fetchall()
                            if Xbox_Fetch!=[]:
                                Count+=1
                                Xbox_Friends_Message+=f"❌ {Xbox_Gamertag} is on the banlist\n"
                                for Ban in Xbox_Fetch:
                                    Data=[]
                                    for i in Ban:
                                        Data.append(i)  
                                    Xbox_Friends_Message+=f"Case Id: {Data[4]}\n"
                await Session.close()
                if Count==-2:
                    Embeds.append(discord.Embed(title=f"Xbox Friends Check",description=f"❌ {xbox} has their xbox friends hidden",colour=0x00F3FF))
                elif Count==-1:
                    Embeds.append(discord.Embed(title=f"Xbox Friends Check",description=f"❌ {xbox} is not a valid xbox gamertag or they have their profile private.",color=0x00F3FF))
                elif Count==0:
                    Embeds.append(discord.Embed(title=f"Xbox Friends Check",description=f"✅ {xbox} has no banned xbox friends",colour=0x02ff00))
                    Friends_Check=True
                else:
                    Embeds.append(discord.Embed(title=f"Xbox Friends Check",description=f"{Count} of {xbox}'s friends are on the banlist\n{Xbox_Friends_Message}",colour=0xff0000))
            Cursor.close()
            DataBase.close()
            Embeds.insert(0,discord.Embed(title="Banlist Check",description=f"{Message}",colour=Colour))       
        if len(Embeds)==0:
            await interaction.followup.send("❌ You need to provide at least one account: xbox or discord")
        else:
            await interaction.followup.send(embeds=Embeds)
        Banlist_Log_Channel=interaction.guild.get_channel(Configuration.Banlist_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Banlist_Log_Channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `user-check` for:\n{Arguments}"))
        if user is not None and xbox is not None and Colour==0x02ff00:
            if Friends_Check:
                try:
                    if Staff_Verified_Role not in user.roles:
                        await user.add_roles(Staff_Verified_Role)
                except:
                    return
            else:
                View=Friends_Check_Confirm()
                await interaction.followup.send(view=View,ephemeral=True)
                await View.wait()
                try:
                    if View.value and Staff_Verified_Role not in user.roles:
                        await user.add_roles(Staff_Verified_Role)
                    elif not View.value and Staff_Verified_Role in user.roles:
                        await user.remove_roles(Staff_Verified_Role)
                except:
                    return
        elif user is not None and xbox is not None and Colour==0xff0000 and Staff_Verified_Role in user.roles:
            await user.remove_roles(Staff_Verified_Role)
    @app_commands.command(name="banlist-case",description="Staff Only | Shows the information about a specific ban case")
    @app_commands.checks.has_any_role('Staff')
    async def case(self,interaction:discord.Interaction,case:int):
        DataBase=self.DataBase_Connection()
        Cursor=DataBase.cursor()
        Cursor.execute(f"SELECT * FROM banlist WHERE ban_id={case}")
        Ban_case=Cursor.fetchall()
        if Ban_case==[]:
            await interaction.response.send_message(f"❌ There is no ban case with id {case}",ephemeral=True)
            return
        Data=[]
        for Ban in Ban_case:
            for i in Ban:
                Data.append(i)
        await interaction.response.send_message(embed=discord.Embed(title=f"Ban Id {case}",description=f"**Discord Name:** {Data[0]}\n**Discord Id:** {Data[1]}\n**Xbox:** {Data[2]}\n**Reason:** {Data[3]}",colour=0xff0000),ephemeral=True)
        Cursor.close()
        DataBase.close()
        Banlist_Log_Channel=interaction.guild.get_channel(Configuration.Banlist_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Banlist_Log_Channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `banlist-case` for case {case}"))
    @app_commands.command(name="banlist-add",description="Staff Only | Adds a ban entry to the banlist")
    @app_commands.checks.has_any_role('Admin','Moderator','Senior Officer','Development Lead')
    async def add(self,interaction:discord.Interaction,user:discord.User=None,xbox:str=None,reason:str=None):
        Arguments=""
        if user!=None:
            Arguments+=f"Discord User: {user.mention}\n"
            User_Name=user.name
            User_Id=user.id
        else:
            User_Name="Not Recorded"
            User_Id="Not Recorded"
        if xbox!=None:
            Arguments+=f"Xbox Gamertag: {xbox}"
            Xbox_Add=xbox
        else:
            xbox="Not Recorded"
            Xbox_Add="Not Recorded"
        if Arguments=="":
            await interaction.followup.send("❌ You need to provide at least one account: xbox or discord")
            return
        DataBase=self.DataBase_Connection()
        Cursor=DataBase.cursor()
        Cursor.execute("INSERT INTO banlist(discord_name,discord_id,xbox_name,reason) VALUES (%s,%s,%s,%s)",(User_Name,User_Id,Xbox_Add,reason))
        Cursor.close()
        DataBase.commit()
        DataBase.close()
        await interaction.response.send_message(f"✅ Success",ephemeral=True)
        Banlist_Log_Channel=interaction.guild.get_channel(Configuration.Banlist_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Banlist_Log_Channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `banlist-add` for:\n{Arguments}"))
    @app_commands.command(name="banlist-delete",description="Staff Only | Deletes a ban from the banlist")
    @app_commands.checks.has_any_role('Admin','Moderator','Senior Officer','Development Lead')
    async def delete(self,interaction:discord.Interaction,case:int):
        DataBase=self.DataBase_Connection()
        Cursor=DataBase.cursor()
        Cursor.execute(f"DELETE FROM banlist WHERE ban_id={case}")
        Cursor.close()
        DataBase.commit()
        DataBase.close()
        await interaction.response.send_message(f"✅ Success",ephemeral=True)
        Banlist_Log_Channel=interaction.guild.get_channel(Configuration.Banlist_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Banlist_Log_Channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `banlist-delete` for case {case}"))
    @app_commands.command(name="lookup",description="Staff Only | Shows deatiled information about a xbox account")
    @app_commands.checks.has_any_role("Staff")
    async def lookup(self,interaction:discord.Interaction,xbox:str):
        async with SignedSession() as Session:
            Authentication_Manager=AuthenticationManager(Session,Client_Id,Client_Secret,"")
            with open("tokens.json") as Token_File:
                Tokens=Token_File.read()
            Authentication_Manager.oauth=OAuth2TokenResponse.parse_raw(Tokens)
            try:
                await Authentication_Manager.refresh_tokens()
            except:
                print(f"""Could not refresh tokens\nYou might have to delete the tokens file and re-authenticate if refresh token is expired""")
                return
            with open("Cursed_Obsidian/tokens.json",mode="w") as Token_File:
                Token_File.write(Authentication_Manager.oauth.json())
            Xbox_Client=XboxLiveClient(Authentication_Manager)
            try:
                Xbox_User=await Xbox_Client.profile.get_profile_by_gamertag(xbox)
                Xuid=Xbox_User.profile_users[0].id
                GameScore=Xbox_User.profile_users[0].settings[7].value
                Profile_Picture=Xbox_User.profile_users[0].settings[8].value
                Reputation=Xbox_User.profile_users[0].settings[11].value
                Embed=(discord.Embed(description=f"Xbox Id: {Xuid}\nGameScore: {GameScore}\nReputation: {Reputation}").set_author(name=xbox,icon_url=Profile_Picture))
            except:
                Embed=(discord.Embed(description=f"❌ {xbox} is not a valid xbox gamertag or they have their profile private.",color=0x00F3FF))
        await interaction.response.send_message(embed=Embed,ephemeral=True)
        Banlist_Log_Channel=interaction.guild.get_channel(Configuration.Banlist_Logs[Functions.Configuration_Position(interaction.guild.id)])
        await Banlist_Log_Channel.send(embed=discord.Embed(description=f"**Staff Member:** {interaction.user.mention}\n**Used Command:** `/lookup` for the xbox account: {xbox}"))
    async def cog_app_command_error(self,interaction:discord.Interaction,error):
        if isinstance(error,app_commands.errors.MissingAnyRole):
            await interaction.response.send_message("❌ You are missing a required role to run this command!",ephemeral=True)
        else:
            print(error)
async def setup(bot:commands.Bot):
    await bot.add_cog(BanList(bot),guilds=[discord.Object(id=933896845644689449),discord.Object(id=1106689170585432076),discord.Object(id=1090782551599231067)])