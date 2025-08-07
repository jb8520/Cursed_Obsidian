from datetime import datetime

from typing import Any



def serialize_datetime(obj: datetime | Any):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')

def deserialize_datetime(dt_str) -> datetime:
    return datetime.fromisoformat(dt_str)