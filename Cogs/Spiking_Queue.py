import asyncio

from discord import Member, VoiceState, VoiceChannel, Message
from discord.ext.commands import Cog
from datetime import datetime, timedelta
from Utils.embed_functions import create_embed, set_embed_attr

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class Spiking(Cog):
    def __init__(self, bot: 'MyBot'):
        self.bot = bot
        self.config = bot.config
        
        self.queue = []

    def _member_join_spiking_queue_check(self, member: Member, before: VoiceState, after: VoiceState, spiking_vc: VoiceChannel) -> bool:
        return (
            before.channel != after.channel 
            and after.channel == spiking_vc
            and member.id not in self.queue
        )

    def _member_leave_spiking_queue_check(self, member: Member, before: VoiceState, after: VoiceState, spiking_vc: VoiceChannel) -> bool:
        return (
            before.channel != after.channel
            and before.channel == spiking_vc
            and member.id in self.queue
        )
    

    async def Message_Updater(self, member: Member, spiking_vc: VoiceChannel,spiking_embed: Message, footer):
        index = 0
        message = ''
        spiking_vc = member.guild.get_channel(self.config.channels.fleet_queue.spiking_vc)

        for user_id in self.spiking_queue:
            index += 1
            user = member.guild.get_member(user_id)

            if not member.guild.get_member(member.id):
                self.spiking_queue.pop(index)

            else:
                message += f'{index}. {user.mention}\n'
        embed = create_embed(
            title = 'Spiking Queue',
            description = f'Join {spiking_vc.mention} to join this Queue.\n\n**Capacity: {index} / 99**\n{message}',
            color = 0x00F3FF
        )
        embed = set_embed_attr(
            embed = embed,
            footer = {
                'text': footer
            }
        )

        await spiking_embed.edit(embed = embed)
    
    
    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        spiking_vc = member.guild.get_channel(self.config.channels.fleet_queue.spiking_vc)
        
        update_embed = False
        footer = None

        if self._member_join_spiking_queue_check(member, before, after, spiking_vc):
            self.queue.append(member.id)
            footer = f'Latest Action: {member.name} has joined Spiking Queue'
            update_embed = True
        
        elif self._member_leave_spiking_queue_check(member, before, after, spiking_vc):
            def member_joins_back_check(check_member: Member, before: VoiceState, after: VoiceState) -> bool:
                return check_member == member and before.channel != after.channel and after.channel == spiking_vc
            
            try:
                await self.bot.wait_for('voice_state_update', check = member_joins_back_check, timeout = 180)
            
            except asyncio.TimeoutError:
                self.queue.remove(member.id)
                footer = f'Latest Action: {member.name} has left the Spiking Queue'
                
                update_embed = True

        if not update_embed:
            return
        
        spiking_queue = member.guild.get_channel(self.config.channels.fleet_staff.spiking_queue)
        spiking_embed = await spiking_queue.fetch_message(self.config.embeds.spiking_queue_panel)

        minimum_refresh_time = timedelta(seconds = 30)

        time_now = datetime.now()
        embed_last_edited_time = spiking_embed.edited_at
        
        if not embed_last_edited_time:
            await self.Message_Updater(member, spiking_vc, spiking_embed, footer)
        
        else:
            if time_now >= (embed_last_edited_time + minimum_refresh_time):
                await self.Message_Updater(member, spiking_vc, spiking_embed, footer)
            
            else:
                await asyncio.sleep(30)
                time_now = datetime.now()
                embed_last_edited_time = spiking_embed.edited_at
                
                if time_now >= (embed_last_edited_time + minimum_refresh_time):
                    await self.Message_Updater(member, spiking_vc, spiking_embed, footer)



async def setup(bot: 'MyBot'):
    await bot.add_cog(Spiking(bot))