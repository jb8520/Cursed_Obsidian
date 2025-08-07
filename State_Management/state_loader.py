import os

from datetime import datetime

from dataclasses import dataclass

from pathlib import Path

from typing import List

from discord.ext import tasks

from State_Management.state import BotState


from Utils.action_log import *


from .action_logger import ActionLogger
from .bot_state_dump import BotStateSerializer

STATE_DUMP_PATH = Path('data/state_dump.json')
ACTION_LOG_PATH = Path('data/wal_log.jsonl')



@dataclass
class FleetInfo:
    category_id: int
    control_id: int
    chat_id: int
    role_id: int
    vc_ids: List[int]



class StateLoader:
    def __init__(self):
        self.state = BotState()
        self.action_logger = ActionLogger(ACTION_LOG_PATH)

    def _pop_by_index(self, index: int, *lists):
        for lst in lists:
            lst.pop(index)
    
    @tasks.loop(minutes = 3)
    async def state_dump_loop(self):
        self.save_state()
        print('✅ Saved state to disk.')

    def load_state(self):

        if STATE_DUMP_PATH.exists() and os.stat(STATE_DUMP_PATH).st_size != 0:
            self.state = BotStateSerializer.load_from_file(STATE_DUMP_PATH)
            print('✅ Loaded saved state from disk.')
        
        else:
            print('⚠️ No saved state file found — starting fresh.')
        
        if ACTION_LOG_PATH.exists() and os.stat(ACTION_LOG_PATH).st_size != 0:
            self.action_logger.replay_log(self.state)
            print('🔁 Replayed action log into current state.')

        return self.state
    
    def save_state(self):
        try:
            BotStateSerializer.dump_to_file(self.state, STATE_DUMP_PATH)
        
        except Exception as e:
            print(f'❌ [State Loader] Failed to save state to dump: {type(e).__name__}: {e}')
        
        else:
            self.action_logger.clear_log()



    def user_join_queue(self, user_id: int, activity: str = None):
        timestamp = datetime.now()
        
        if user_id not in self.state.Queue_State.queue_list:
            self.state.Queue_State.queue_list.append(user_id)
            self.state.Queue_State.activity_list.append(activity)
            self.state.Queue_State.timestamp_list.append(timestamp)
        
        else:
            index = self.state.Queue_State.queue_list.index(user_id)

            self.state.Queue_State.activity_list[index] = activity

        # log this action for crash recovery
        action_log = make_join_queue_action(
            user_id = user_id,
            activity = activity,
            timestamp = timestamp
        )

        self.action_logger.log_action(action_log)

    def user_insert_queue(self, user_id: int, activity: str, position: int):
        timestamp = datetime.now()

        if user_id in self.state.Queue_State.queue_list:
            index = self.state.Queue_State.queue_list.index(user_id)

            state_lists = (
                self.state.Queue_State.activity_list,
                self.state.Queue_State.timestamp_list
            )
            
            self._pop_by_index(index, *state_lists)
        
        index = position - 1

        self.state.Queue_State.queue_list.insert(index, user_id)
        self.state.Queue_State.activity_list.insert(index, activity)
        self.state.Queue_State.timestamp_list.insert(index, timestamp)

        # log this action for crash recovery
        action_log = make_insert_queue_action(
            user_id = user_id,
            activity = activity,
            position = position,
            timestamp = timestamp
        )

        self.action_logger.log_action(action_log)

    def user_leave_queue(self, user_id: int):
        timestamp = datetime.now()
        
        index = self.state.Queue_State.queue_list.index(user_id)
        
        state_lists = (
            self.state.Queue_State.queue_list,
            self.state.Queue_State.activity_list,
            self.state.Queue_State.timestamp_list
        )
        
        self._pop_by_index(index, *state_lists)
        
        # log this action for crash recovery
        action_log = make_leave_queue_action(
            user_id = user_id,
            timestamp = timestamp
        )

        self.action_logger.log_action(action_log)


    def queue_open(self):
        timestamp = datetime.now()

        self.state.Queue_State.queue_open = True

        # log this action for crash recovery
        action_log = make_open_queue_action(
            queue_open = True,
            timestamp = timestamp
        )

        self.action_logger.log_action(action_log)

    def queue_close(self):
        timestamp = datetime.now()

        self.state.Queue_State.queue_open = False

        self.state.Queue_State.queue_list = []
        self.state.Queue_State.activity_list = []
        self.state.Queue_State.timestamp_list = []

        # log this action for crash recovery
        action_log = make_close_queue_action(
            queue_open = False,
            timestamp = timestamp
        )
        
        self.action_logger.log_action(action_log)
    
    def queue_clear(self):
        timestamp = datetime.now()

        self.state.Queue_State.queue_open = True

        self.state.Queue_State.queue_list = []
        self.state.Queue_State.activity_list = []
        self.state.Queue_State.timestamp_list = []

        # log this action for crash recovery
        action_log = make_clear_queue_action(
            queue_open = True,
            timestamp = timestamp
        )
        
        self.action_logger.log_action(action_log)


    def create_fleet(self, fleet_num: int, fleet_data: FleetInfo):
        timestamp = datetime.now()

        self.state.Fleet_State.active_fleet = True
        self.state.Fleet_State.category[fleet_num] = fleet_data.category_id
        self.state.Fleet_State.control[fleet_num] = fleet_data.control_id
        self.state.Fleet_State.chat[fleet_num] = fleet_data.chat_id
        self.state.Fleet_State.role[fleet_num] = fleet_data.role_id
        self.state.Fleet_State.vcs[fleet_num] = fleet_data.vc_ids

        # log this action for crash recovery
        action_log = make_create_fleet_action(
            fleet_num = fleet_num,
            category = fleet_data.category_id,
            control = fleet_data.control_id,
            chat = fleet_data.chat_id,
            role = fleet_data.role_id,
            vcs = fleet_data.vc_ids,
            timestamp = timestamp
        )

        self.action_logger.log_action(action_log)

    def delete_fleet(self, fleet_num: int):
        timestamp = datetime.now()

        state_lists = (
            self.state.Fleet_State.category,
            self.state.Fleet_State.control,
            self.state.Fleet_State.chat,
            self.state.Fleet_State.role,
            self.state.Fleet_State.vcs
        )

        self._pop_by_index(fleet_num, *state_lists)

        if not self.state.Fleet_State.category:
            self.state.Fleet_State.active_fleet = False
        
        # log this action for crash recovery
        action_log = make_delete_fleet_action(
            fleet_num = fleet_num,
            timestamp = timestamp
        )

        self.action_logger.log_action(action_log)