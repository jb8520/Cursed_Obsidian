import discord
from discord.ext.commands import Cog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class Fleet_Roles(Cog):
    def __init__(self, bot):
        self.bot: 'MyBot' = bot


    @Cog.listener('on_voice_state_update')
    async def voice_update_(self, member: discord.Member, before, after):
        if self.bot.state.Fleet_State.active_fleet:
            for fleet_num in self.bot.state.Fleet_State.category:
                for vc_id in self.bot.state.Fleet_State.vcs[fleet_num]:
                    fleet_role = member.guild.get_role(self.bot.state.Fleet_State.role[fleet_num])
                    vc = member.guild.get_role(vc_id)

                    if before.channel != after.channel and before.channel == vc:
                        await member.remove_roles(fleet_role)
                        break
                    
                    if before.channel != after.channel and after.channel == vc:
                        await member.add_roles(fleet_role)
                        break



async def setup(bot: 'MyBot'):
    await bot.add_cog(Fleet_Roles(bot))