from datetime import datetime

from discord import Guild, Interaction, Member

from Configuration.value_types import ConfigTypes

from typing import Literal, List

from Utils.command_decorators import get_role_names_by_perms_tier

from Utils.embed_functions import create_embed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from State_Management.state import QueueState, FleetState



async def queue_check_requires_role_of_perm_tiers(interaction: Interaction, tiers: List[Literal['tier_0', 'tier_1', 'tier_2', 'tier_3', 'tier_4']] = None) -> bool:
    perm_role_names = get_role_names_by_perms_tier(tiers = tiers)

    if not hasattr(interaction, 'guild') or not hasattr(interaction.user, 'roles'):
        await interaction.response.send_message(
            '❌ You are missing a required role use this button!',
            ephemeral = True
        )

        return False


    if interaction.user == interaction.guild.owner:
        return True
    
    user_roles_names = [role.name.lower() for role in interaction.user.roles]

    if any(role in user_roles_names for role in perm_role_names):
        return True
    
    await interaction.response.send_message(
        '❌ You are missing a required role use this button!',
        ephemeral = True
    )

    return False


async def check_queue_open(queue_state: 'QueueState', interaction: Interaction) -> bool:
    if not queue_state.queue_open:
        await interaction.response.send_message(
            '❌ This command can\'t be used while the queue is closed',
            ephemeral = True
        )
        
        return False
    
    return True

async def check_member_in_queue(queue_state: 'QueueState', interaction: Interaction, member: Member) -> bool:
    if member.id not in queue_state.queue_list:
        await interaction.response.send_message(
            f'❌ {member.mention} isn\'t in the queue!',
            ephemeral = True
        )

        return False
    
    return True

async def check_banlist_roles(queue_state: 'QueueState', interaction: Interaction, config: ConfigTypes, member: Member) -> bool:
    if interaction.guild.get_role(config.roles.xbox_linked) not in member.roles:
        await interaction.response.send_message(
            f'❌ {member.mention} doesn\'t have the Xbox-Linked Role.',
            ephemeral = True
        )

        return False
    
    if interaction.guild.get_role(config.roles.staff_verified) not in member.roles:
        await interaction.response.send_message(
            f'❌ {member.mention} isn\'t staff verified. Please verify them with the `/user-check` command.',
            ephemeral = True
        )

        return False

    return True

async def check_entered_ship_nums(fleet_state: 'FleetState', interaction: Interaction, fleet_number: int, ship_number: int) -> bool:
    if not (
        1 <= ship_number <= 6 
        and fleet_number in fleet_state.category.keys()
    ):
        await interaction.response.send_message('❌ Please select from 6 Ship Channels under any of the active Fleets', ephemeral = True)
        
        return False
    
    return True



async def update_user_in_queue_role(interaction: Interaction, config: ConfigTypes, member: Member, queue_role_add: bool = None):
    if queue_role_add is not None:
        in_queue_role = interaction.guild.get_role(config.roles.in_queue)
        
        if queue_role_add:
            await member.add_roles(in_queue_role)
        
        else:
            if in_queue_role in member.roles:
                await member.remove_roles(in_queue_role)

async def update_queue_embed(interaction: Interaction, config: ConfigTypes, queue_state: 'QueueState'):
    queue_channel = interaction.guild.get_channel(config.channels.fleet_queue.queue)
    queue_embed = await queue_channel.fetch_message(config.embeds.queue_panel)
    
    description = config.preset_messages.queue_description + queue_display(queue_state, interaction.guild)

    embed = create_embed(
        title = config.preset_messages.queue_title,
        description = description,
        colour = 0x00F3FF
    )

    await queue_embed.edit(embed = embed)


def queue_display(queue_state: 'QueueState', guild: Guild) -> str:
    message = ''

    for user_id in queue_state.queue_list:

        index = queue_state.queue_list.index(user_id)

        member = guild.get_member(user_id)
        activity = queue_state.activity_list[index]
        timestamp = queue_state.timestamp_list[index]

        if not member:
            lists = (
                queue_state.queue_list,
                queue_state.activity_list,
                queue_state.timestamp_list
                )

            for lst in lists:
                lst.pop(index)
                continue

        message += f'\n{index + 1}.   {member.mention}   |   {activity}   |   <t:{int(datetime.timestamp(timestamp))}:R>'
            
    return message