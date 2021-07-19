import os

import teapot


def bot_owner():
    return os.environ['BOT_OWNER']


def bot_token():
    return os.environ['BOT_TOKEN']

def bot_prefix():
    return os.environ['BOT_PREFIX']


def bot_status():
    default_prefix = f'{", ".join(teapot.config.bot_prefix())} | Teapot.py {teapot.version()}'
    try:
        return os.environ['BOT_STATUS']
    except:
        return os.environ['BOT_STATUS']


def storage_type():
    if os.environ['STORAGE_TYPE'] != "mysql":
        os.environ['STORAGE_TYPE'] = "flatfile"
    return os.environ['STORAGE_TYPE']


def db_host():
    return os.environ['DB_HOST']


def db_port():
    return os.environ['DB_PORT']


def db_schema():
    return os.environ['DB_SCHEMA']


def db_user():
    return os.environ['DB_USER']


def db_password():
    return os.environ['DB_PASSWORD']


def lavalink_host():
    return os.environ['LAVALINK_HOST']


def lavalink_port():
    return os.environ['LAVALINK_PORT']


def lavalink_password():
    return os.environ['LAVALINK_PASSWORD']
