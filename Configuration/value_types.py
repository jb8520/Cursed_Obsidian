from dataclasses import dataclass

from typing import List



@dataclass
class Roles:
    member: int
    staff: int
    admin: int
    senior_mod: int
    mod: int
    officer: int
    helper: int
    in_queue: int
    on_duty: int
    staff_verified: int
    xbox_linked: int


@dataclass
class PermRoles:
    # values are lists of str that map to role in Roles
    tier_0: List[str]
    tier_1: List[str]
    tier_2: List[str]
    tier_3: List[str]
    tier_4: List[str]


@dataclass
class Categories:
    logs: int
    fleet_staff: int
    fleet_queue: int


@dataclass
class Logs:
    bot: int
    queue: int
    banlist: int

@dataclass
class FleetStaff:
    queue_manager: int
    spiking_queue: int
    on_duty_chat: int

@dataclass
class FleetQueue:
    queue: int
    spiking_vc: int
    waiting_room: int

@dataclass
class Channels:
    logs: Logs
    fleet_staff: FleetStaff
    fleet_queue: FleetQueue


@dataclass
class Embeds:
    staff_queue_controls: int
    duty_switch_panel: int
    fleet_status_panel: int
    queue_panel: int
    spiking_vc_control: int
    spiking_queue_panel: int


@dataclass
class PresetMessages:
    queue_title: str
    queue_description: str

@dataclass
class Other:
    guild_id: int
    banlist_toggle: bool

@dataclass
class ConfigTypes:
    roles: Roles
    perm_roles: PermRoles
    categories: Categories
    channels: Channels
    embeds: Embeds
    preset_messages: PresetMessages
    other: Other