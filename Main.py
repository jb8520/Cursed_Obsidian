'''
Main bot entrypoint

Features:
- Adds persistent UI components as views
- Loads all cogs from the Cogs directory
- Loads all views from the Views directory
- Sets up bot state container
- Defines admin/owner only command: say, sync
'''

from typing import List
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import Context

from Configuration.env_loader import EnvLoader

from Configuration.config_classes import ConfigManager
from Configuration.value_types import ConfigTypes

from State_Management.state_loader import StateLoader

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from State_Management.state import BotState

from Views import persistent_views


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = '.', intents = discord.Intents.all(), case_insensitive = True)
        self.config: 'ConfigTypes' = ConfigManager()
        self.state_loader = StateLoader()
    
    async def loadExtension(self, extension_name: str) -> List[str]:
        extension_list = []
        path = Path(extension_name)
        for file in path.glob('*.py'):
            filename = file.stem
            if filename == '__init__':
                continue

            if extension_name == 'Cogs':
                if filename == 'Banlist' and not(self.config.other.banlist_toggle):
                    continue
                
                try:
                    await self.load_extension(f'{extension_name}.{filename}')
                    extension_list.append(filename)
                
                except Exception as error:
                    print(f'❌ Failed to load Cog {filename}\n{type(error).__name__}: {error}')
            
            elif extension_name == 'Views':
                extension_list.append(filename)
        
        return extension_list
    

    async def setup_hook(self):
        self.state: 'BotState' = self.state_loader.load_state()
        bot.state_loader.state_dump_loop.start()
        
        if self.config.other.banlist_toggle:
            try:
                await self.state.xbox_wrapper.initialize()
            
            except Exception as e:
                raise f'Failed to initialize Xbox client: {e}'

        for view_class in persistent_views:
            self.add_view(view_class(self))
        
        loaded_cogs = await self.loadExtension(extension_name = 'Cogs')
        loaded_views = await self.loadExtension(extension_name = 'Views')
        
        if not loaded_cogs:
             print(f'⚠️ No extensions found in Cogs')
        
        else:
            print(f'✅ Successfully loaded {len(loaded_cogs)} cogs: {", ".join(loaded_cogs)}')
        
        if not loaded_views:
             print(f'⚠️ No extensions found in Views')
        
        else:
            print(f'✅ Successfully loaded {len(loaded_views)} views: {", ".join(loaded_views)}')    


    async def on_ready(self):
        await self.change_presence(activity = discord.Game(name = 'Sea of Thieves'))
        print(f'{self.user} is connected to Discord, current latency is {round(self.latency * 1000)}ms')



bot = MyBot()



@bot.command()
@commands.has_guild_permissions(administrator = True)
async def say(ctx: Context, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)


@bot.command()
@commands.is_owner()
async def sync(ctx: Context):
    await ctx.message.delete()

    await bot.tree.sync()
    print('Synced Commands to the Tree')

@bot.command()
@commands.is_owner()
async def shutdown(ctx: Context):
    await ctx.message.delete()
    print('🛑 Shutting down...')
    
    bot.state_loader.save_state()
    await bot.close()


if __name__ == '__main__':
    bot.run(EnvLoader.BOT_TOKEN)