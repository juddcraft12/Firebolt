
import os
import time
from os.path import join, dirname
import json
import requests

import discord
from discord.ext import tasks
from discord.ext import commands as dcmd
from dotenv import load_dotenv
import firebolt
from itertools import cycle
from flask import Flask
from threading import Thread


app = Flask('')

@app.route('/')
def home():
	return 'Im in!'

def run():
  app.run(
		host='0.0.0.0',
		port=8080
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()
keep_alive()
print(f"""
______ _          _           _ _   
|  ___(_)        | |         | | |  
| |_   _ _ __ ___| |__   ___ | | |_ 
|  _| | | '__/ _ \ '_ \ / _ \| | __|
| |   | | | |  __/ |_) | (_) | | |_ 
\_|   |_|_|  \___|_.__/ \___/|_|\__|
                                  
    by Antimatter
Running Firebolt.py {firebolt.version()}
""")

req = requests.get(f'https://api.github.com/repos/RedCokeDevelopment/Teapot.py/tags')
response = json.loads(req.text)
if req.status_code == 200:
    if response[0]['name'] == firebolt.version():
        print("You are currently running the latest version of Teapot.py!\n")
    else:
        versionlisted = False
        for x in response:
            if x['name'] == firebolt.version():
                versionlisted = True
                print("You are not using our latest version! :(\n")
        if not versionlisted:
            print("You are currently using an unlisted version!\n")
elif req.status_code == 404:
    # 404 Not Found
    print("Latest Teapot.py version not found!\n")
elif req.status_code == 500:
    # 500 Internal Server Error
    print("An error occurred while fetching the latest Teapot.py version. [500 Internal Server Error]\n")
elif req.status_code == 502:
    # 502 Bad Gateway
    print("An error occurred while fetching the latest Teapot.py version. [502 Bad Gateway]\n")
elif req.status_code == 503:
    # 503 Service Unavailable
    print("An error occurred while fetching the latest Teapot.py version. [503 Service Unavailable]\n")
else:
    print("An unknown error has occurred when fetching the latest Teapot.py version\n")
    print("HTML Error Code:" + str(req.status_code))

load_dotenv(join(dirname(__file__), '.env'))

if os.getenv('CONFIG_VERSION') != firebolt.config_version():
    if os.path.isfile('.env'):
        print("Missing environment variables. Please backup and delete .env, then run Teapot.py again.")
        quit(2)
    print("Unable to find required environment variables. Running setup.py...")  # if .env not found
    firebolt.setup.__init__() # run setup.py

print("Initializing bot...")
if firebolt.config.storage_type() == "mysql": # if .env use mysql, create the table if table not exists
    time_start = time.perf_counter()
    database = firebolt.managers.database.__init__()
    db = firebolt.managers.database.db(database)
    db.execute('ALTER DATABASE `' + firebolt.config.db_schema() + '` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute(
        'CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `guild_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute(
        'CREATE TABLE IF NOT EXISTS `channels` (`channel_id` BIGINT, `channel_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute(
        "CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `user_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci, `user_discriminator` INT) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    db.execute(
        "CREATE TABLE IF NOT EXISTS `bot_logs` (`timestamp` TEXT, `type` TINYTEXT, `class` TINYTEXT, `message` MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    firebolt.managers.database.create_table(
        "CREATE TABLE IF NOT EXISTS `guild_logs` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")

    print(
        f"Connected to database ({firebolt.config.db_host()}:{firebolt.config.db_port()}) in {round(time.perf_counter() - time_start, 2)}s")

    db.execute("INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
               (firebolt.time(), "BOT_START", __name__, "Initialized bot"))
    database.commit()

intents = discord.Intents.default()
intents.members = True
intents.typing = False
bot = dcmd.Bot(intents=intents, command_prefix="g!",help_command=None)
status = cycle(["g!help | Gaybot | By Antimatter","g!help | Gaybot | By Antimatter","g!help | Gaybot | By Antimatter"])
@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))
@bot.event
async def on_ready():
    change_status.start()
    print(f"Connected to Discord API in {round(time.perf_counter() - discord_time_start, 2)}s")
    time_start = time.perf_counter()
    #firebolt.events.__init__(bot)
    for filename in os.listdir('./firebolt/cogs'):
      if filename.endswith('.py'):
        bot.load_extension(f'firebolt.cogs.{filename[:-3]}')
    
      else:
        print(f'Unable to load {filename[:-3]}')
    if firebolt.config.storage_type() == "mysql":
        for guild in bot.guilds:
            firebolt.managers.database.create_guild_table(guild)
    elif firebolt.config.storage_type() == "sqlite":
        print("[!] Warning: SQLite storage has not been implemented yet. MySQL is recommended")  # WIP
    print(f"Registered commands and events in {round(time.perf_counter() - time_start, 2)}s")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(firebolt.config.bot_status()))  # Update Bot status


try:
    discord_time_start = time.perf_counter()
    bot.run(firebolt.config.bot_token())
except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    if firebolt.config.storage_type() == "mysql":
        db.execute("INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
                   (firebolt.time(), "ERROR", __name__, e))
    time.sleep(5)
    exit(1)