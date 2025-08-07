import json
from pathlib import Path
from types import SimpleNamespace
from typing import Dict


from .value_types import ConfigTypes


Config_Path = Path('Configuration/values.json')


class ConfigNamespace(SimpleNamespace):
    def __init__(self, data: Dict):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigNamespace(value))
            else:
                setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigNamespace):
                d[key] = value.to_dict()
            elif isinstance(value, list):
                d[key] = [item.to_dict() if isinstance(item, ConfigNamespace) else item for item in value]
            else:
                d[key] = value
        return d

    def update(self, data: Dict):
        for key, value in data.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(attr, ConfigNamespace) and isinstance(value, dict):
                    attr.update(value)
                else:
                    setattr(self, key, value)
            else:
                if isinstance(value, dict):
                    setattr(self, key, ConfigNamespace(value))
                else:
                    setattr(self, key, value)


class ConfigManager(ConfigNamespace):
    def __init__(self):
        if not Config_Path.exists():
            raise FileNotFoundError(f'Configuration file not found at {Config_Path}')
        with Config_Path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        super().__init__(data)

    def reload(self):
        self.__dict__.clear()
        self.__init__()

    def _save(self):
        with Config_Path.open('w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)

    def update(self):
        self._save()
        self.reload()

config = ConfigManager() # type: ConfigTypes
roles = config.roles
perm_roles = config.perm_roles