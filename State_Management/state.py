from datetime import datetime
from typing import List, Dict


from Utils import XboxClientWrapper

class BotState:
    def __init__(self):
        # Adds FleetState and QueueState containers to manage fleet and queue data within BotState
        self.Fleet_State = FleetState()
        self.Queue_State = QueueState()

        # Timestamp marking when the bot came online; used to calculate uptime
        self.time: datetime = datetime.now()
        
        self.xbox_wrapper = XboxClientWrapper()



class FleetState:
    def __init__(self):
        # Indicates whether any fleets are currently active
        self.active_fleet: bool = False

        # These dictionaries are updated when fleets are created/deleted via /create and /delete
        # Key = fleet number; value = corresponding Discord ID
        self.category: Dict[int, int] = {}
        self.control: Dict[int, int] = {}
        self.chat: Dict[int, int] = {}
        self.role: Dict[int, int] = {}

        # Each fleet number maps to a list of 6 VC IDs for that fleet
        self.vcs: Dict[int, List[int]] = {}



class QueueState:
    def __init__(self):
        # Indicates whether the queue is currently open
        self.queue_open: bool = False

        # Tracks users in the queue by their Discord ID, activity, and queue join timestamp
        # Index 0 = first in queue
        self.queue_list: List[int] = []
        self.activity_list: List[str] = []
        self.timestamp_list: List[datetime] = []