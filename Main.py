import discord,datetime,os
import Cogs.Roles,Views.Queue,Views.Channel_Control
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv() 

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".",intents=discord.Intents.all(),case_insensitive=True)
    async def setup_hook(self):
        Buttons=[Cogs.Roles.DutySwitchButtons(),Cogs.Roles.InactiveStaff(),Views.Queue.OpenQueueButtons(),Views.Queue.ClosedQueueButton(),Views.Queue.StaffQueueButtons(),Views.Channel_Control.ChannelCloseControlButtons(),Views.Channel_Control.ChannelLockControlButtons(),Views.Channel_Control.Spiking_Control_Button()]
        for Button in Buttons:
            self.add_view(Button)
        bot.Active_Fleets=[[],[]]
        bot.Fleet_Status_Message=[]
        bot.Fleet_Categories=[[],[]]
        bot.Fleet_Controls=[[],[]]
        bot.Fleet_Chats=[[],[]]
        bot.Fleet_Roles=[[],[]]
        bot.Fleet_Vc_1=[[],[]]
        bot.Fleet_Vc_2=[[],[]]
        bot.Fleet_Vc_3=[[],[]]
        bot.Fleet_Vc_4=[[],[]]
        bot.Fleet_Vc_5=[[],[]]
        bot.Fleet_Vc_6=[[],[]]
        bot.Queue_List=[[],[]]
        bot.Activity_List=[[],[]]
        bot.Timestamp_List=[[],[]]
        bot.Queue_State=[["open"],["open"]]
        bot.Time=datetime.datetime.now()
        Extension="Cogs: "
        Count_Cogs=0
        View="Views: "
        Count_Views=0
        for Filename in os.listdir("./Cogs"):
            if Filename.endswith(".py"):
                try:
                    await self.load_extension(f"Cogs.{Filename[:-3]}")
                    Extension+=f"{Filename[:-3]}, "
                    Count_Cogs+=1
                except Exception as Error:
                    print(f"Failed to load extension {Filename[:-3]}\n{type(Error).__name__}: {Error}")
        for Filename in os.listdir("./Views"):
            if Filename.endswith(".py"):
                View+=f"{Filename[:-3]}, "
                Count_Views+=1
        print(f"Successfully loaded {Count_Cogs} {Extension[:-2]}\nSuccessfully loaded {Count_Views} {View[:-2]}")
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="Sea of Thieves"))
        print(f"{self.user} is online, latency is {round(self.latency*1000)}ms")
bot=MyBot()
@bot.command()
@commands.has_any_role("Admin")
async def say(ctx,Message):
    await ctx.message.delete()
    await ctx.send(Message)
@bot.command()
@commands.has_any_role("Admin")
async def sync(ctx):
    await ctx.message.delete()
    await bot.tree.sync()
    Server_Ids=[933896845644689449]
    for Id in Server_Ids:
        await bot.tree.sync(guild=discord.Object(id=Id))
    print("Synced Commands to the Tree")
bot.run(os.environ["BOT_TOKEN"])