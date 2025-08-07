import traceback
from datetime import datetime
from discord.ext.commands import Cog
from discord.app_commands import command
from discord import Interaction

from discord import TextChannel, Guild
from Utils.embed_functions import create_embed
from Utils.command_decorators import app_command_requires_role_of_perm_tiers

from typing import Literal, Optional

from Configuration import *

from Views import (
    ConfirmView,
    SpikingControlButton,
    OpenQueueButtons,
    StaffQueueButtons,
    DutySwitchButtons
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class Setup(Cog):
    def __init__(self, bot: 'MyBot'):
        self.bot = bot
        self.state = bot.state
        self.config = bot.config
        self.fleet_state = bot.state.Fleet_State
        self.queue_state = bot.state.Queue_State

    async def _check_discord_obj_valid(
        self,
        guild: Guild,
        obj_type: Literal['role', 'channel', 'message'],
        ns,
        name: str,
        channel: Optional[TextChannel] = None
    ) -> bool:
        if obj_type == 'message' and not channel:
            raise TypeError(
                '❌ Expected a channel object to be passed for message checks, but one was not supplied'
            )
        
        if hasattr(ns, name):
            funcs = {
                'role': guild.get_role,
                'channel': guild.get_channel
            }

            if channel:
                funcs['message'] = channel.fetch_message


            func = funcs[obj_type]

            try:
                id = getattr(ns, name)
                if obj_type == 'message':
                    return bool(await func(id))
                
                else:
                    return (bool(func(id)))
            
            except:
                return False
            
        return False
            

    @command(name = 'setup-all', description = 'Creates or recreates/fixes all the infrastructure the bot needs to function.')
    @app_command_requires_role_of_perm_tiers(['tier_4'])
    async def setup_all(self, interaction: Interaction):
        if not interaction.guild:
            await interaction.response.send_message('❌ This command can only be run in a server', ephemeral = True)
            return
        
        embed = create_embed(
            title = 'Setup Confirmation',
            description = 'On confirmation, the bot will create or recreate/fix the infrastructure it needs to operate. This is detailed as per below.\n\n## Channels\n### Logs:\n> banlist\n> queue\n> bot\n### Fleet Staff\n> queue_manager\n> spiking_queue\n> on_duty_chat\n### Fleet Queue\n> queue\n> spiking vc\n> waiting room\n\n## Roles\n> in_queue\n> on_duty\n> staff_verified',
            colour = 0x00F3FF,
        )

        view = ConfirmView(
            bot = self.bot,
            confirm_message = 'Setup Confirmed',
            cancel_message = 'Setup Cancelled'
        )

        await interaction.response.send_message(embed = embed, view = view)

        await view.wait()
        if not view.confirmed:
            return
        

        created_items = []
        failed_attrs = []

        guild = interaction.guild


        # === Roles ===
        required_roles = {
            'in_queue': in_queue_name,
            'on_duty': on_duty_name,
            'staff_verified': staff_verified_name,
        }

        for key, role_name in required_roles.items():
            if not await self._check_discord_obj_valid(
                guild = guild,
                obj_type = 'role',
                ns = self.config.roles,
                name = key
            ):
                
                try:
                    role = await guild.create_role(
                        name = role_name
                    )
                    setattr(self.config.roles, key, role.id)
                
                except Exception as e:
                    failed_attrs.append(role_name)
                    print(f'[Setup Error] Failed to create {role_name}: {e}')
                    traceback.print_exc()
                
                else:
                    created_items.append(f'Created role `{role_name}: id = {role.id}')


        # === Categories ===
        required_categories = {
            'logs': (logs_category_name, logs_category_position),
            'fleet_staff': (fleet_staff_category_name, fleet_staff_category_position),
            'fleet_queue': (fleet_queue_category_name, fleet_queue_category_position)
        }

        for key, (category_name, category_position) in required_categories.items():
            if not await self._check_discord_obj_valid(
                guild = guild,
                obj_type = 'channel',
                ns = self.config.categories,
                name = key
            ):
                try:
                    category = await guild.create_category(
                        name = category_name,
                        position = category_position
                    )

                    setattr(self.config.categories, key, category.id)

                except Exception as e:
                    failed_attrs.append(category_name)
                    print(f'[Setup Error] Failed to create {category_name}: {e}')
                    traceback.print_exc()
                
                else:
                    created_items.append(f'Created category `{category_name}: id = {category.id}')
        
        
        # === Channels ===
        logs_overwrites = {

        }

        fleet_staff_overwrites = {

        }

        fleet_queue_overwrites = {

        }

        required_channels = {
            ('logs', 'bot'): (bot_logs_name, 'text', logs_overwrites),
            ('logs', 'queue'): (queue_logs_name, 'text', logs_overwrites),
            ('logs', 'banlist'): (banlist_logs_name, 'text', logs_overwrites),

            ('fleet_staff', 'queue_manager'): (fs_queue_manager_name, 'text', fleet_staff_overwrites),
            ('fleet_staff', 'spiking_queue'): (fs_spiking_queue_name, 'text', fleet_staff_overwrites),
            ('fleet_staff', 'on_duty_chat'): (fs_on_duty_chat_name, 'text', fleet_staff_overwrites),

            ('fleet_queue', 'queue'): (fq_queue_name, 'text', fleet_queue_overwrites),
            ('fleet_queue', 'spiking_vc'): (fq_spiking_vc_name, 'voice', fleet_queue_overwrites),
            ('fleet_queue', 'waiting_room'): (fq_waiting_room_name, 'voice', fleet_queue_overwrites)
        }

        for (category_name, key), (channel_name, type_, overwrites) in required_channels.items():
            category_id = getattr(self.config.categories, category_name, None)
            category = guild.get_channel(category_id) if category_id else None
            if category:
                ns = getattr(self.config.channels, category_name)
                
                if not await self._check_discord_obj_valid(
                    guild = guild,
                    obj_type = 'channel',
                    ns = ns,
                    name = key
                ):
                    try:
                        if type_ == 'text':
                            channel = await guild.create_text_channel(
                                name = channel_name,
                                category = category,
                                overwrites = overwrites
                            )
                        
                        elif type_ == 'voice':
                            channel = await guild.create_voice_channel(
                                name = channel_name,
                                category = category,
                                overwrites = overwrites
                            )
                        
                        setattr(ns, key, channel.id)

                    except Exception as e:
                        failed_attrs.append(channel_name)
                        print(f'[Setup Error] Failed to create {channel_name}: {e}')
                        traceback.print_exc()

                    else:
                        created_items.append(f'Created channel `{channel_name}: id = {channel.id}')

        
        # === Embeds ===
        on_duty_role = guild.get_role(self.config.roles.on_duty)
        queue = guild.get_channel(self.config.channels.fleet_queue.queue)
        queue_manager = guild.get_channel(self.config.channels.fleet_staff.queue_manager)
        spiking_queue = guild.get_channel(self.config.channels.fleet_staff.spiking_queue)
        spiking_vc = guild.get_channel(self.config.channels.fleet_queue.spiking_vc)

        embed_defs = [
            {
                'name': 'staff_queue_controls',
                'channel': queue_manager,
                'embed': create_embed(
                    title = 'Staff Queue Buttons',
                    description = 'Use the Buttons below to control the queue',
                    color = 0x00F3FF
                ),

                'view': StaffQueueButtons(self.bot)
            },

            {
                'name': 'duty_switch_panel',
                'channel': queue_manager,
                'embed': create_embed(
                    title = 'Duty Switch Configuration Panel',
                    description = f'Get or Drop {on_duty_role.mention} role by using the buttons below.\n\n__**Current On-Duty Members:**__\n',
                    color = 0x00F3FF
                ),

                'view': DutySwitchButtons(self.bot)
            },

            {
                'name': 'active_ships_panel',
                'channel': queue,
                'embed': create_embed(
                    description = '__**On Duty Staff:**__\nThere are currently no Staff Members On Duty\n\n__**Active Fleet Ships:**__\nThere are currently no active ships',
                    color = 0x00F3FF
                ),

                'view': None
            },

            {
                'name': 'queue_panel',
                'channel': queue,
                'embed': create_embed(
                    title = self.config.preset_messages.queue_title,
                    description = self.config.preset_messages.queue_description,
                    color = 0x00F3FF
                ),

                'view': OpenQueueButtons(self.bot)
            },

            {
                'name': 'spiking_vc_control',
                'channel': spiking_queue,
                'embed': create_embed(
                    title = 'Spiking Vc',
                    description = 'The Spiking Vc is currently: 🔒',
                    color = 0x00F3FF
                ),

                'view': SpikingControlButton(self.bot)
            },

            {
                'name': 'spiking_queue_panel',
                'channel': spiking_queue,
                'embed': create_embed(
                    title = 'Spiking Queue',
                    description = f'Join {spiking_vc.mention} to join this Queue.\n\n**Capacity: 0 / 99**',
                    color = 0x00F3FF
                ),

                'view': None
            }
        ]
        
        for embed_def in embed_defs:
            name = embed_def['name']
            channel = embed_def['channel']
            embed = embed_def['embed']
            view = embed_def['view']

            if not await self._check_discord_obj_valid(
                guild = guild,
                obj_type = 'message',
                ns = self.config.embeds,
                name = name,
                channel = channel
            ):
                try:
                    sent_embed = await channel.send(embed = embed, view = view)
                    setattr(self.config.embeds, name, sent_embed.id)
                
                except Exception as e:
                    failed_attrs.append(name)
                    print(f'[Setup Error] Failed to create {name}: {e}')
                    traceback.print_exc()

                else:
                    created_items.append(f'🟢 Sent `{name}` embed: id = {sent_embed.id}')
        

        if not created_items and not failed_attrs:
            await interaction.edit_original_response(
                content = '⚠️ There was nothing to create! The bot should already be correctly setup.',
                embed = None
            )

            return
        
        self.queue_state.queue_open = True

        self.config.update()


        log_message = f'{interaction.user.mention} used the setup command'

        if failed_attrs:
            log_message += '\n\n❌ The following attrs failed to be created:\n'
            for attr in failed_attrs:
                log_message += f'{attr}\n'

        log_channel = interaction.guild.get_channel(self.config.channels.logs.bot)

        embed = create_embed(
            description = log_message,
            timestamp = datetime.now()
        )

        await log_channel.send(embed = embed)


async def setup(bot: 'MyBot'):
    await bot.add_cog(Setup(bot))