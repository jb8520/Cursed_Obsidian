from typing import Literal, List

from discord import Interaction
from discord.ext.commands import check as ext_command_check
from discord.app_commands import check as app_command_check

from Configuration.config_classes import roles, perm_roles


def get_role_ids_by_perms_tier(tiers: List[Literal['tier_0','tier_1','tier_2','tier_3','tier_4']] = None) -> List[int]:
    if tiers is None:
        tiers = ['tier_0']
    
    ids_with_perms = []

    for tier in tiers:
        role_names = getattr(perm_roles, tier, [])
        for role_name in role_names:
            role_id = getattr(roles, role_name, None)
            if role_id is not None:
                ids_with_perms.append(role_id)
    
    return ids_with_perms

def get_role_names_by_perms_tier(tiers: List[str] = None) -> List[str]:
    if tiers is None:
        tiers = ['tier_0']

    names_with_perms = []

    for tier in tiers:
        
        role_names = getattr(perm_roles, tier, [])
        if not role_names:
            continue

        for role_name in role_names:
            role_id = getattr(roles, role_name, None)
            if role_id is not None:
                names_with_perms.append(role_name)
    
    return names_with_perms



def make_is_owner_or_has_role_predicate(perm_role_names: List[str]):
    async def predicate(interaction: Interaction):
        if not hasattr(interaction, 'guild'):
            return False
        
        if not hasattr(interaction.user, 'roles'):
            return False

        if interaction.user == interaction.guild.owner:
            return True
        
        user_roles_names = [role.name.lower() for role in interaction.user.roles]

        return any(role in user_roles_names for role in perm_role_names)
    
    return predicate



def ext_command_requires_role_of_perm_tiers(tiers: List[Literal['tier_0', 'tier_1', 'tier_2', 'tier_3', 'tier_4']] = None):
    perm_role_names = get_role_names_by_perms_tier(tiers = tiers)

    return ext_command_check(predicate = make_is_owner_or_has_role_predicate(perm_role_names = perm_role_names))


def app_command_requires_role_of_perm_tiers(tiers: List[Literal['tier_0', 'tier_1', 'tier_2', 'tier_3', 'tier_4']] = None):
    perm_role_names = get_role_names_by_perms_tier(tiers = tiers)
    
    return app_command_check(predicate = make_is_owner_or_has_role_predicate(perm_role_names = perm_role_names))