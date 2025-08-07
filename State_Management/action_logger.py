import threading, json, os
from pathlib import Path

from datetime import datetime

from typing import Any, Tuple, List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from State_Management.state import BotState

from Utils.datetime_serialization import serialize_datetime, deserialize_datetime



class ActionLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.lock = threading.Lock()  # avoid concurrent writes if multi-threaded

        self._action_handlers = {
        'join_queue': self._handle_join_queue,
        'leave_queue': self._handle_leave_queue,
        'open_queue': self._handle_open_queue,
        'close_queue': self._handle_close_queue,
        'clear_queue': self._handle_clear_queue,
        'create_fleet': self._handle_create_fleet,
        'delete_fleet': self._handle_delete_fleet,
    }
    


    def _handle_join_queue(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        user_id: int = data['user_id']
        activity: str = data['activity']

        if user_id not in bot_state.Queue_State.queue_list:
            bot_state.Queue_State.queue_list.append(user_id)
            bot_state.Queue_State.activity_list.append(activity)
            bot_state.Queue_State.timestamp_list.append(timestamp)
        
        else:
            index = bot_state.Queue_State.queue_list.index(user_id)
            bot_state.Queue_State.activity_list[index] = activity

    def _handle_insert_queue(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        user_id: int = data['user_id']
        activity: str = data['activity']
        position: int = data['position']

        if user_id in bot_state.Queue_State.queue_list:
            index = bot_state.Queue_State.queue_list.index(user_id)

            state_lists = (
                bot_state.Queue_State.queue_list,
                bot_state.Queue_State.activity_list,
                bot_state.Queue_State.timestamp_list
            )
            
            self._pop_by_index(index, *state_lists)
        
        index = position - 1

        bot_state.Queue_State.queue_list.insert(index, user_id)
        bot_state.Queue_State.activity_list.insert(index, activity)
        bot_state.Queue_State.timestamp_list.insert(index, datetime.now())
        
    def _handle_leave_queue(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        user_id: int = data['user_id']

        if user_id in bot_state.Queue_State.queue_list:
            index = bot_state.Queue_State.queue_list.index(user_id)
            
            state_lists = (
                bot_state.Queue_State.queue_list,
                bot_state.Queue_State.activity_list,
                bot_state.Queue_State.timestamp_list
            )
            
            self._pop_by_index(index, *state_lists)


    def _handle_open_queue(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        bot_state.Queue_State.queue_open = True  

    def _handle_close_queue(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        bot_state.Queue_State.queue_open = False
        bot_state.Queue_State.queue_list = []
        bot_state.Queue_State.activity_list = []
        bot_state.Queue_State.timestamp_list = []    

    def _handle_clear_queue(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        bot_state.Queue_State.queue_open = True
        bot_state.Queue_State.queue_list = []
        bot_state.Queue_State.activity_list = []
        bot_state.Queue_State.timestamp_list = []


    def _handle_create_fleet(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        fleet_num = data['fleet_num']
        category = data['category']
        control = data['control']
        chat = data['chat']
        role = data['role']
        vcs = data['vcs']

        bot_state.Fleet_State.active_fleet = True
        bot_state.Fleet_State.category[fleet_num] = category
        bot_state.Fleet_State.control[fleet_num] = control
        bot_state.Fleet_State.chat[fleet_num] = chat
        bot_state.Fleet_State.role[fleet_num] = role
        bot_state.Fleet_State.vcs[fleet_num] = vcs   

    def _handle_delete_fleet(self, data: dict, timestamp: datetime, bot_state: 'BotState'):
        fleet_num = data['fleet_num']
        
        state_lists = (
            bot_state.Fleet_State.category,
            bot_state.Fleet_State.control,
            bot_state.Fleet_State.chat,
            bot_state.Fleet_State.role,
            bot_state.Fleet_State.vcs
        )

        self._pop_by_index(fleet_num, *state_lists)

        if not bot_state.Fleet_State.category:
            bot_state.Fleet_State.active_fleet = False
    


    def _extract_data(self, action: dict) -> Tuple[Any, datetime]:
        data = action['data']
        timestamp = deserialize_datetime(action['timestamp'])

        return data, timestamp
    

    def _pop_by_index(self, index: int, *lists):
        for lst in lists:
            lst.pop(index)



    def log_action(self, action: dict):
        # action must be serializable dict describing an event
        with self.lock, self.log_path.open('a', encoding = 'utf-8') as f:
            json.dump(action, f, default = serialize_datetime)
            f.write('\n')

    def clear_log(self):
        with self.lock:
            self.log_path.write_text('', encoding = 'utf-8')

    def replay_log(self, bot_state: 'BotState'):
        if not self.log_path.exists() or os.stat(self.log_path).st_size == 0:
            return  # nothing to replay

        with self.lock, self.log_path.open('r', encoding = 'utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                action: dict = json.loads(line)
                data, timestamp = self._extract_data(action = action)

                handler = self._action_handlers.get(action['action'])
                if handler:
                    handler(data, timestamp, bot_state)

        self.clear_log()