import asyncio
from datetime import datetime
from discord import app_commands, Interaction, Guild, Role, CategoryChannel, TextChannel, VoiceChannel, NotFound, PermissionOverwrite, User, Member, Colour, VoiceState
from discord.utils import utcnow
from discord.ext import tasks
from discord.ext.commands import Cog
from discord.app_commands.errors import MissingAnyRole

from Views import (
    ChannelCloseControlButtons,
    ChannelLockControlButtons
)

from Utils.embed_functions import create_embed


from Utils import (
    send_log_message,
    update_user_in_queue_role,
    update_queue_embed,
    queue_display,
    check_queue_open,
    check_member_in_queue,
    check_banlist_roles,
    check_entered_ship_nums
)


from typing import List, Tuple

from typing import TYPE_CHECKING

from Utils.command_decorators import get_role_ids_by_perms_tier, app_command_requires_role_of_perm_tiers

from State_Management.state_loader import FleetInfo


if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class Staff_Commands(Cog):
    def __init__(self, bot: 'MyBot'):
        self.bot = bot
        self.state = bot.state
        self.config = bot.config
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State
        self.fleet_status.start()

        self.circles = ['🔴','🟠','🟡','🟢','🔵','🟣']


    def _get_next_available_fleet_number(self) -> int:
        fleet_categories = self.fleet_state.category

        used_nums = sorted(fleet_categories.keys())

        if not used_nums:
            fleet_num = 1
        
        else:
            highest_used_num = used_nums[-1]
        
            # Start checking from 1 upward to find the first free number
            for i in range(1, highest_used_num + 2):
                if i not in used_nums:
                    fleet_num = i
                    break
        
        return fleet_num
    


    async def _create_fleet_category(self, guild: Guild, fleet_num: int) -> CategoryChannel:
        mod_roles_id = get_role_ids_by_perms_tier(['tier_3', 'tier_4'])

        fleet_category_overwrites = {
            guild.default_role: PermissionOverwrite(
                connect = False
            )
        }

        for role_id in mod_roles_id:
            if (role := guild.get_role(role_id)):
                fleet_category_overwrites[role] = PermissionOverwrite(
                    connect = True,
                    manage_channels = True
                )
        

        fleet_category = await guild.create_category_channel(
            name = f'✦ 𝙁𝙇𝙀𝙀𝙏 {fleet_num} ✦',
            position = 7,
            overwrites = fleet_category_overwrites
        )

        return fleet_category

    async def _create_fleet_role(self, guild: Guild, fleet_num: int) -> Role:
        fleet_role = await guild.create_role(
            name = f'fleet{fleet_num}',
            mentionable = True
        )

        return fleet_role

    async def _create_fleet_chat(self, guild: Guild, fleet_num: int, fleet_category: CategoryChannel, fleet_role: Role) -> TextChannel:
        staff_role_id = get_role_ids_by_perms_tier(['tier_1'])[0]
        staff_role = guild.get_role(staff_role_id)

        fleet_chat_overwrites = {
            guild.default_role: PermissionOverwrite(
                view_channel = False,
                create_instant_invite = False,
                embed_links = False,
                use_application_commands = True
            ),

            fleet_role: PermissionOverwrite(
                view_channel = True
            ),

            staff_role: PermissionOverwrite(
                view_channel = True
            )
        }
        

        fleet_chat = await fleet_category.create_text_channel(
            name = f'💬︱fleet{fleet_num}-chat',
            overwrites = fleet_chat_overwrites
        )

        return fleet_chat

    async def _create_fleet_control(self, guild: Guild, fleet_num: int, fleet_category: CategoryChannel) -> TextChannel:
        staff_role_id = get_role_ids_by_perms_tier(['tier_1'])[0]
        staff_role = guild.get_role(staff_role_id)

        fleet_control_overwrites = {
            guild.default_role: PermissionOverwrite(
                view_channel = False,
                send_messages = False
            ),

            staff_role: PermissionOverwrite(
                view_channel = True
            )
        }
        

        fleet_control = await fleet_category.create_text_channel(
            name = f'🎛︱fleet-{fleet_num}-control',
            overwrites = fleet_control_overwrites
        )

        return fleet_control

    async def _create_fleet_vcs(self, guild: Guild, fleet_category: CategoryChannel, fleet_role: Role) -> Tuple[List[int], str, str]:
        fleet_vc_ids: List[int] = []

        close_control_message = ''
        lock_control_message = ''

        for i in range(6):
            fleet_vc = await self._create_fleet_vc(
                guild = guild,
                fleet_category = fleet_category,
                fleet_role = fleet_role,
                index = i
            )

            fleet_vc_ids.append(fleet_vc.id)

            close_control_message += f'{i + 1}. {fleet_vc.mention} | Closed\n'
            lock_control_message += f'{i + 1}. {fleet_vc.mention} | 🔒\n'
        
        return fleet_vc_ids, close_control_message, lock_control_message

    async def _create_fleet_vc(self, guild: Guild, fleet_category: CategoryChannel, fleet_role: Role, index: int) -> VoiceChannel:
        staff_role_id = get_role_ids_by_perms_tier(['tier_1'])[0]
        staff_role = guild.get_role(staff_role_id)

        fleet_vc_overwrites = {
            guild.default_role: PermissionOverwrite(
                view_channel = False,
                create_instant_invite = False,
                connect = False,
                speak = True,
                stream = True
            ),

            fleet_role: PermissionOverwrite(
                view_channel = True
            ),

            staff_role: PermissionOverwrite(
                view_channel = True,
                connect = True,
                move_members = True,
                mute_members = True,
                deafen_members = True
            )
        }


        fleet_vc = await fleet_category.create_voice_channel(
            name = f'{self.circles[index]}[CLOSED]',
            overwrites = fleet_vc_overwrites,
            user_limit = 3
        )

        return fleet_vc
        
    async def _send_control_panels(self, guild: Guild, fleet_control: TextChannel, close_control_message: str, lock_control_message: str):
        embed = create_embed(
            title = 'Fleet Voice Channel Open & Close Configuration Panel',
            description = f'**Current Channel Status:**\n{close_control_message}',
            color = 0x00F3FF
        )
        await fleet_control.send(
            embed = embed,
            view = ChannelCloseControlButtons(self.bot)
        )


        embed = create_embed(
            title = 'Fleet Voice Channel Status & Configuration Panel',
            description = f'**Current Channel Status:**\n{lock_control_message}',
            color = 0x00F3FF
        )
        await fleet_control.send(
            embed = embed,
            view = ChannelLockControlButtons(self.bot)
        )


    @tasks.loop(minutes = 1)
    async def fleet_status(self):
        
        guild = self.bot.get_guild(self.config.other.guild_id)

        if not guild:
            return
        
        queue = guild.get_channel(self.config.channels.fleet_queue.queue)

        
    
        if not queue:
            return
        
        try:
            active_ships_panel = await queue.fetch_message(self.config.embeds.active_ships_panel)
        
        except NotFound:
            return

        
        on_duty_role = guild.get_role(self.config.roles.on_duty)

        if not on_duty_role.members:
            message = 'There are currently no Staff Members On Duty\n'
        
        else:
            message = ''

            for index, staff_member in enumerate(on_duty_role.members):
                message += f'{index + 1}. {staff_member.mention}\n'
        
        description = f'__**On Duty Staff:**__\n{message}'

        
        current_message = ''
        
        for fleet_num in self.fleet_state.category:
            vc_ids = self.state.Fleet_State.vcs[fleet_num]
            fleet_vcs = [guild.get_channel(vc_ids[i]) for i in range(6)]

            message = ''

            for vc in fleet_vcs:
                require_members = ''

                vc_name = vc.name
                if '[CLOSED]' not in vc_name:
                    emojis = {
                        2: '<:ship_Sloop:944298920081780799>',
                        3: '<:ship_Brigantine:944298920417321030>',
                        4: '<:ship_Galleon:944298920215986236>'
                    }

                    vc_limit = vc.user_limit
                    
                    emoji = emojis.get(vc_limit, '')

                    if len(vc.members) < vc_limit:
                        require_members = f' |  Needs {vc_limit - len(vc.members)}'

                    if '[' and ']' in vc_name:
                        index = vc_name.index(']')
                        vc_name = vc_name[index + 2:]
                    
                    message += f'\n{emoji} {vc_name}{require_members}'
            
            if message:
                current_message += f'\n\n**Fleet {fleet_num}:**{message}'
        
        if not current_message:
            current_message = '\nThere are currently no active ships'
        
        description += f'\n__**Active Fleet Ships:**__{current_message}'
        

        embed = create_embed(
            description = description,
            colour = 0x00F3FF
        )

        await active_ships_panel.edit(embed = embed)
    

    @app_commands.command(name = 'create', description = 'Higher Staff Only | Creates a fleet')
    @app_command_requires_role_of_perm_tiers(['tier_3', 'tier_4'])
    async def create(self, interaction: Interaction):
        fleet_num = self._get_next_available_fleet_number()

        guild = interaction.guild

        await interaction.response.send_message('✅ Success!', ephemeral = True)
        
        if not self.fleet_state.active_fleet:
            self.fleet_state.active_fleet = True


        fleet_category: CategoryChannel = await self._create_fleet_category(
            guild = guild,
            fleet_num = fleet_num
        )

        fleet_role: Role = await self._create_fleet_role(
            guild = guild,
            fleet_num = fleet_num
        )
        
        fleet_chat: TextChannel = await self._create_fleet_chat(
            guild = guild,
            fleet_num = fleet_num,
            fleet_category = fleet_category,
            fleet_role = fleet_role
        )

        fleet_control: TextChannel = await self._create_fleet_control(
            guild = guild,
            fleet_num = fleet_num,
            fleet_category = fleet_category
        )

        fleet_vc_ids, close_control_message, lock_control_message = await self._create_fleet_vcs(
            guild = guild,
            fleet_category = fleet_category,
            fleet_role = fleet_role
        )
        
        await self._send_control_panels(
            guild = guild,
            fleet_control = fleet_control,
            close_control_message = close_control_message,
            lock_control_message = lock_control_message
        )


        fleet_data = FleetInfo(
            category_id = fleet_category.id,
            control_id = fleet_control.id,
            chat_id = fleet_chat.id,
            role_id = fleet_role.id,
            vc_ids = fleet_vc_ids
        )
        self.bot.state_loader.create_fleet(fleet_num = fleet_num, fleet_data = fleet_data)


        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = f'{interaction.user.mention} created a fleet'
        )


    @app_commands.command(name = 'delete', description = 'Higher Staff Only | Deletes a specific fleet')
    @app_command_requires_role_of_perm_tiers(['tier_3', 'tier_4'])
    async def delete(self, interaction: Interaction, fleet_number: int):
        if fleet_number not in self.fleet_state.category:
            await interaction.response.send_message(f'❌ Fleet {fleet_number} does not exist!', ephemeral = True)
            return
        
        await interaction.response.send_message('✅ Success!', ephemeral = True)
        

        category = interaction.guild.get_channel(self.fleet_state.category[fleet_number])
        

        for channel in category.channels:
            await channel.delete()
        
        await category.delete()
        

        role = interaction.guild.get_role(self.fleet_state.role[fleet_number])
        await role.delete()


        self.bot.state_loader.delete_fleet(fleet_num = fleet_number)
        

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = f'{interaction.user.mention} deleted fleet {fleet_number}'
        )    
    
    
    @app_commands.command(name = 'rename', description = 'Staff Only | Rename a specific Fleet Ship.')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def rename(self, interaction: Interaction, fleet_number: int, ship_number: int, name: str):
        if not await check_entered_ship_nums(
            fleet_state = self.fleet_state,
            interaction = interaction,
            fleet_number = fleet_number,
            ship_number = ship_number
        ):
            return

        
        vc_ids = self.fleet_state.vcs[fleet_number]
        vc = interaction.guild.get_channel(vc_ids[ship_number-1])

        await vc.edit(name = f'{self.circles[ship_number-1]}{name}')

        await interaction.response.send_message('✅ Success', ephemeral = True)

        
        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = f'{interaction.user.mention} renamed Fleet {fleet_number} Ship {ship_number} to `{name}`'
        )


    @app_commands.command(name = 'ship-size', description = 'Staff Only | Changes the Ship Size of a specific Fleet Ship.')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def ship_size(self, interaction: Interaction, limit: int, fleet_number: int, ship_number: int):
        if not await check_entered_ship_nums(
            fleet_state = self.fleet_state,
            interaction = interaction,
            fleet_number = fleet_number,
            ship_number = ship_number
        ):
            return
        

        vc_ids = self.fleet_state.vcs[fleet_number]
        vc = interaction.guild.get_channel(vc_ids[ship_number-1])
        
        await vc.edit(user_limit = limit)

        await interaction.response.send_message('✅ Success', ephemeral = True)


        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = f'{interaction.user.mention} set the ship size for Fleet {fleet_number} Ship {ship_number} to `{limit}`'
        )
    
    
    
    staff_queue_commands = app_commands.Group(name = 'queue', description = 'Staff Only | Manage the join-queue, add/remove members')

    @staff_queue_commands.command(name = 'remove', description = 'Staff Only | Remove a specific member from the queue')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def remove(self, interaction: Interaction, member: Member):
        if not await check_queue_open(
            queue_state = self.queue_state,
            interaction = interaction
        ):
            return
        
        if not await check_member_in_queue(
            queue_state = self.queue_state,
            interaction = interaction,
            member = member
        ):
            return
        

        self.bot.state_loader.user_leave_queue(
            user_id = member.id
        )

        await update_user_in_queue_role(
            interaction = interaction,
            config = self.config,
            member = member,
            queue_role_add = False
        )
        await update_queue_embed(
            interaction = interaction,
            config = self.config,
            queue_state = self.queue_state
        )

        await interaction.response.send_message('✅ Success!', ephemeral = True)



        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = f'**Staff Member:** {interaction.user.mention}\n**Used Command:** `queue_remove` for {member}'
        )
    
    
    @staff_queue_commands.command(name = 'insert', description = 'Staff Only | Insert a specific member into the queue')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def insert(self, interaction: Interaction, member: Member, position: int, activity: str):
        if not await check_queue_open(
            queue_state = self.queue_state,
            interaction = interaction
        ):
            return

        if self.config.other.banlist_toggle:
            if not await check_banlist_roles(
                queue_state = self.queue_state,
                interaction = interaction,
                config = self.config,
                member = member
            ):
                return


        self.bot.state_loader.user_insert_queue(
            user_id = member.id,
            activity = activity,
            position = position
        )


        await update_user_in_queue_role(
            interaction = interaction,
            config = self.config,
            member = member,
            queue_role_add = False
        )
        await update_queue_embed(
            interaction = interaction,
            config = self.config,
            queue_state = self.queue_state
        )

        await interaction.response.send_message('✅ Success!', ephemeral = True)
        

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = f'**Staff Member:** {interaction.user.mention}\n**Used Command:** `queue_insert` for {member}'
        )        
    
    
    @staff_queue_commands.command(name = 'process', description = 'Staff Only | Process members in the queue, once a spot has opened.')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def process(self, interaction: Interaction, member: Member, fleet_number: int, ship_number: int):
        if not await check_queue_open(
            queue_state = self.queue_state,
            interaction = interaction
        ):
            return
        
        if not await check_member_in_queue(
            queue_state = self.queue_state,
            interaction = interaction,
            member = member
        ):
            return
        
        if not await check_entered_ship_nums(
            fleet_state = self.fleet_state,
            interaction = interaction,
            fleet_number = fleet_number,
            ship_number = ship_number
        ):
            return
        
        if self.config.other.banlist_toggle:
            if not await check_banlist_roles(
                queue_state = self.queue_state,
                interaction = interaction,
                config = self.config,
                member = member
            ):
                return
        

        if not (
            1 <= ship_number <= 6 
            and fleet_number in self.fleet_state.category.keys()
        ):
            await interaction.response.send_message('❌ Please select from 6 Ship Channels under any of the active Fleets', ephemeral = True)
            return
        

        self.bot.state_loader.user_leave_queue(
            user_id = member.id
        )
        

        in_queue_role = interaction.guild.get_role(self.config.roles.in_queue)
        
        if in_queue_role in member.roles:
            await member.remove_roles(in_queue_role)


        embed = create_embed(
            title = self.config.preset_messages.queue_title,
            description = self.config.preset_messages.queue_description + queue_display(self.queue_state, interaction.guild),
            colour = 0x00F3FF
        )

        queue_channel = interaction.guild.get_channel(self.config.channels.fleet_queue.queue)
        queue_embed = await queue_channel.fetch_message(self.config.embeds.queue_panel)

        await queue_embed.edit(embed = embed)


        await interaction.response.send_message('✅ Success!', ephemeral = True)


        vc_ids = self.state.Fleet_State.vcs[fleet_number]
        vc_id = vc_ids[ship_number - 1]
        vc = interaction.guild.get_channel(vc_id)
        
        waiting_vc = interaction.guild.get_channel(self.config.channels.fleet_queue.waiting_room)

        if member in waiting_vc.members:
            await member.move_to(vc)
        
        else:
            embed = create_embed(
                description = f'A spot has opened up for you in **Fleet {fleet_number} Ship {vc.name}**. Please join the [Alliance Waiting Room](https://discord.com/channels/933896845644689449/934131108356968518) to be moved to your ship.\n\n \n\nYour spot is currently reserved but will expire <t:{int(datetime.now().timestamp()+180)}:R> if you do not join in time.',
                colour = Colour.green()
            )

            queue_message = await queue_channel.send(content = member.mention, embed = embed)


            def check(check_member: Member, before: VoiceState, after: VoiceState):
                return check_member == member and before.channel != after.channel and after.channel == waiting_vc

            try:
                await self.bot.wait_for('voice_state_update', check = check, timeout = 180)
            
            except asyncio.TimeoutError:
                embed = create_embed(
                    description = f'{member.mention} did not join the vc in time and has been removed from the queue entirely.',
                    color = Colour.red()
                )

                await queue_channel.send(embed = embed, delete_after = 3)

            else:
                await member.move_to(vc)
            
            finally:
                await queue_message.delete()
        
        

        await send_log_message(
            interaction = interaction,
            config = self.config,
            description = f'**Staff Member:** {interaction.user.mention}\n**Used Command:** `queue_process` for {member.mention} to {vc.mention}'
        )   


    async def cog_app_command_error(self, interaction: Interaction, error):
        if isinstance(error, MissingAnyRole):
            await interaction.response.send_message('❌ You are missing a required role to run this command!', ephemeral = True)
        
        else:
            print(error)



async def setup(bot: 'MyBot'):
    await bot.add_cog(Staff_Commands(bot))