import json
from pathlib import Path

from typing import Dict

from State_Management.state import BotState

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from State_Management.state import BotState

from Utils.datetime_serialization import serialize_datetime, deserialize_datetime


STATE_DUMP_PATH = Path('data/state_dump.json')

def _convert_keys_to_int(d: Dict) -> Dict:
    return {int(key): value for key, value in d.items()}

class BotStateSerializer:
    @staticmethod
    def to_dict(bot_state: 'BotState') -> Dict:
        return {
            'Fleet_State': {
                'active_fleet': bot_state.Fleet_State.active_fleet,
                'fleet_categories': bot_state.Fleet_State.category,
                'fleet_controls': bot_state.Fleet_State.control,
                'fleet_chats': bot_state.Fleet_State.chat,
                'fleet_roles': bot_state.Fleet_State.role,
                'fleet_vcs': bot_state.Fleet_State.vcs,
            },
            'Queue_State': {
                'queue_open': bot_state.Queue_State.queue_open,
                'queue_list': bot_state.Queue_State.queue_list,
                'activity_list': bot_state.Queue_State.activity_list,
                'timestamp_list': [timestamp.isoformat() for timestamp in bot_state.Queue_State.timestamp_list],
            }
        }


    @staticmethod
    def from_dict(data: dict) -> 'BotState':
        bot_state = BotState()
        fleet = data['Fleet_State']
        queue = data['Queue_State']

        bot_state.Fleet_State.active_fleet = fleet['active_fleet']
        bot_state.Fleet_State.category = _convert_keys_to_int(fleet['fleet_categories'])
        bot_state.Fleet_State.control = _convert_keys_to_int(fleet['fleet_controls'])
        bot_state.Fleet_State.chat = _convert_keys_to_int(fleet['fleet_chats'])
        bot_state.Fleet_State.role = _convert_keys_to_int(fleet['fleet_roles'])
        bot_state.Fleet_State.vcs = _convert_keys_to_int(fleet['fleet_vcs'])

        bot_state.Queue_State.queue_open = queue['queue_open']
        bot_state.Queue_State.queue_list = queue['queue_list']
        bot_state.Queue_State.activity_list = queue['activity_list']
        bot_state.Queue_State.timestamp_list = [deserialize_datetime(ts) for ts in queue['timestamp_list']]

        return bot_state

    @staticmethod
    def dump_to_file(bot_state: 'BotState', path: Path = STATE_DUMP_PATH):
        data = BotStateSerializer.to_dict(bot_state)
        with path.open('w', encoding = 'utf-8') as f:
            json.dump(data, f, default = serialize_datetime, indent = 4)

    @staticmethod
    def load_from_file(path: Path) -> 'BotState':
        if not path.exists():
            raise FileNotFoundError(f'No state dump found at {path}')
        
        with path.open('r', encoding = 'utf-8') as f:
            data = json.load(f)
        return BotStateSerializer.from_dict(data)