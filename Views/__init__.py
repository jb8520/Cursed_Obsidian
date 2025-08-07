from .channel_close_control import ChannelCloseControlButtons
from .channel_lock_control import ChannelLockControlButtons
from .spiking_control import SpikingControlButton
from .confirm import ConfirmView, VerifyView
from .queue import OpenQueueButtons, StaffQueueButtons
from .roles import DutySwitchButtons


import os

import inspect

import importlib

from discord.ui import View, Modal, Select



persistent_views = []

# Folder path relative to this __init__.py
views_path = os.path.dirname(__file__)

# Go through every .py file in Views/ except __init__.py
for filename in os.listdir(views_path):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'Views.{filename[:-3]}'  # Strip .py and add full import path

        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f'❌ [View Loader] Failed to import {module_name}: {type(e).__name__}: {e}')
            continue

        for _, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and obj.__module__ == module.__name__
                and issubclass(obj, View)
                and not issubclass(obj, Modal)
                and not issubclass(obj, Select)
                and obj is not View
            ):
                persistent_views.append(obj)