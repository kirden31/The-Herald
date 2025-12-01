__all__ = ('to_bool',)

import os


def to_bool(env_name, default):
    env_value = os.getenv(env_name, str(default)).lower()
    return env_value in {'true', '1', 'yes', 'y'}
