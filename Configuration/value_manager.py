import json
from pathlib import Path
from types import SimpleNamespace

from typing import Optional, Any, List, Dict



DEFAULT_VALUE_PATH = Path('Configuration/values.json')



class ValueNamespace(SimpleNamespace):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = ValueNamespace(**value)  # recursively convert
            setattr(self, key, value)
    
    def get(self, key, default = None):
        return getattr(self, key, default)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __contains__(self, key):
        return hasattr(self, key)



def _dict_to_namespace(d: dict) -> ValueNamespace:
    ns = {}
    for key, value in d.items():
        if isinstance(value, dict):
            ns[key] = _dict_to_namespace(value)

        elif isinstance(value, list):
            ns[key] = [
                _dict_to_namespace(item) if isinstance(item, dict) else item for item in value
            ]

        else:
            ns[key] = value

    return ValueNamespace(**ns)


def _namespace_to_dict(ns: SimpleNamespace) -> dict:
    d = {}
    for key, value in vars(ns).items():
        if isinstance(value, SimpleNamespace):
            d[key] = _namespace_to_dict(value)
        
        elif isinstance(value, list):
            d[key] = [
                _namespace_to_dict(item) if isinstance(item, SimpleNamespace) else item for item in value
            ]
        
        else:
            d[key] = value
            
    return d


def _find_path_to_target(config, target_ns: SimpleNamespace, path = None) -> Optional[List[str]]:
    path = path or []
    if isinstance(config, dict):
        for key, value in config.items():
            if isinstance(value, dict):
                result = _find_path_to_target(value, target_ns, path + [key])
                if result:
                    return result

    elif isinstance(config, SimpleNamespace):
        for key in vars(config):
            val = getattr(config, key)
            if val is target_ns:
                return path + [key]
            if isinstance(val, SimpleNamespace):
                result = _find_path_to_target(val, target_ns, path + [key])
                if result:
                    return result
    
    return None


def _update_nested(d: Dict, path: Optional[List[str]], updated_dict: Dict) -> Any:
    if not path:
        return updated_dict
    key = path[0]
    if len(path) == 1:
        d[key] = updated_dict
    
    else:
        _update_nested(d[key], path[1:], updated_dict)
    
    return d



def update_value(config, updated_ns: SimpleNamespace) -> None:
    with DEFAULT_VALUE_PATH.open('r', encoding = 'utf-8') as f:
        full_data = json.load(f)

    if config is updated_ns:
        path = None
    
    else:
        path = _find_path_to_target(config, updated_ns)
        if not path:
            raise ValueError('Provided namespace not found in config')

    updated_dict = _namespace_to_dict(updated_ns)

    updated_full_data = _update_nested(full_data, path, updated_dict)

    with DEFAULT_VALUE_PATH.open('w', encoding = 'utf-8') as f:
        json.dump(updated_full_data, f, indent = 2)

def load_values(path: Path = DEFAULT_VALUE_PATH):
    if not path.exists():
        raise FileNotFoundError(f'Configuration Values files not found at {path}')
    
    with path.open('r', encoding = 'utf-8') as f:
        raw_data = json.load(f)

    ns = _dict_to_namespace(raw_data)
    config = ns._config
    
    # Fallback in case BanList feature is disabled (roles not set)
    config.roles.xbox_linked = getattr(config.roles, 'xbox_linked', 0) or 0
    config.roles.staff_verified = getattr(config.roles, 'staff_verified', 0) or 0

    return config