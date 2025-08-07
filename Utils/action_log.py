from datetime import datetime

from typing import List


def make_join_queue_action(user_id: int, activity: str, timestamp: datetime):
    return {
        "action": "join_queue",
        "data": {
            "user_id": user_id,
            "activity": activity
        },
        "timestamp": timestamp
    }

def make_insert_queue_action(user_id: int, activity: str, position: int, timestamp: datetime):
    return {
        "action": "insert_queue",
        "data": {
            "user_id": user_id,
            "activity": activity,
            "position": position
        },
        "timestamp": timestamp
    }

def make_leave_queue_action(user_id: int, timestamp: datetime):
    return {
        "action": "leave_queue",
        "data": {
            "user_id": user_id
        },
        "timestamp": timestamp
    }


def make_open_queue_action(queue_open: bool, timestamp: datetime):
    return {
        "action": "open_queue",
        "data": {
            "queue_open": queue_open
        },
        "timestamp": timestamp
    }

def make_close_queue_action(queue_open: bool, timestamp: datetime):
    return {
        "action": "close_queue",
        "data": {
            "queue_open": queue_open
        },
        "timestamp": timestamp
    }

def make_clear_queue_action(queue_open: bool, timestamp: datetime):
    return {
        "action": "clear_queue",
        "data": {
            "queue_open": queue_open
        },
        "timestamp": timestamp
    }


def make_create_fleet_action(fleet_num: int, category: int, control: int, chat: int, role: int, vcs: List[int], timestamp: datetime):
    return {
        "action": "create_fleet",
        "data": {
            "fleet_num": fleet_num,
            "category": category,
            "control": control,
            "chat": chat,
            "role": role,
            "vcs": vcs
        },
        "timestamp": timestamp
    }

def make_delete_fleet_action(fleet_num: int, timestamp: datetime):
    return {
        "action": "delete_fleet",
        "data": {
            "fleet_num": fleet_num
        },
        "timestamp": timestamp
    }