'''
env_loader.py - Handles loading and validating environment variables.

Example: EnvLoader[key: str]
'''



import os

from dotenv import load_dotenv
load_dotenv()



def get_env_or_fail(key: str, fallback = None) -> str:
    if key in os.environ:
        value = os.environ[key]
        if value.strip() == '':
            raise RuntimeError(
                f'⚠️ Environment variable \'{key}\' is set but empty — check your .env file.'
            )
        return value
    
    elif fallback is not None:
        return fallback
    
    else:
        raise RuntimeError(
            f'⚠️ Missing environment variable: \'{key}\' in config.py - check your .env file.'
        )

class EnvLoader:
    BOT_TOKEN: str = get_env_or_fail('BOT_TOKEN')

    DATABASE_HOST: str = get_env_or_fail('DATABASE_HOST')
    DATABASE_USER: str = get_env_or_fail('DATABASE_USER')
    DATABASE_PASSWORD: str = get_env_or_fail('DATABASE_PASSWORD')
    DATABASE_NAME: str = get_env_or_fail('DATABASE_NAME')