import time

import firebolt


def __init__():
    print('\n' * 100)
    print("""
    
      _____                      _      ____             __ _                       _             
     |_   _|__  __ _ _ __   ___ | |_   / ___|___  _ __  / _(_) __ _ _   _ _ __ __ _| |_ ___  _ __ 
       | |/ _ \\/ _` | '_ \\ / _ \\| __| | |   / _ \\| '_ \\| |_| |/ _` | | | | '__/ _` | __/ _ \\| '__|
       | |  __/ (_| | |_) | (_) | |_  | |__| (_) | | | |  _| | (_| | |_| | | | (_| | || (_) | |   
       |_|\\___|\\__,_| .__/ \\___/ \\__|  \\____\\___/|_| |_|_| |_|\\__, |\\__,_|_|  \\__,_|\\__\\___/|_|   
                    |_|    © 2020-2021 Red Coke Development    |___/                               
    
                      NOTE: You can change the settings later in .env
    
    """)

    # Declare default configuration
    input_mysql_host = "127.0.0.1"
    input_mysql_port = "3306"
    input_mysql_schema = "teapot"
    input_mysql_user = "root"
    input_mysql_password = ""

    input_bot_token = input("Discord bot token: ")
    input_bot_prefix = input("Command Prefix: ")
    input_bot_status = input("Bot status: (Playing xxx) ")
    input_storage_type = input("Use MySQL? [Y/n] ")
    if input_storage_type.lower() == "y" or input_storage_type.lower() == "yes":
        input_storage_type = "mysql"
        input_mysql_host = input("Database Host: ")
        input_mysql_port = input("Database Port: ")
        input_mysql_schema = input("Database Schema: ")
        input_mysql_user = input("Database User: ")
        input_mysql_password = input("Database Password: ")
    elif input_storage_type.lower() == "n" or input_storage_type.lower() == "no":
        input_storage_type = "flatfile"
    else:
        print("[!] Your input was invalid, and has been automagically set to flatfile storage.")
        input_storage_type = "flatfile"
    input_lavalink_host = input("Lavalink Host: ")
    input_lavalink_port = input("Lavalink Port: ")
    input_lavalink_password = input("Lavalink Password: ")

    input_osu_api_key = input("osu!api Key")

    try:
        config = f"""CONFIG_VERSION={firebolt.config_version()}
BOT_TOKEN={input_bot_token}
BOT_PREFIX={input_bot_prefix}
BOT_STATUS={input_bot_status}
STORAGE_TYPE={input_storage_type}

DB_HOST={input_mysql_host}
DB_PORT={input_mysql_port}
DB_SCHEMA={input_mysql_schema}
DB_USER={input_mysql_user}
DB_PASSWORD={input_mysql_password}

LAVALINK_HOST={input_lavalink_host}
LAVALINK_PORT={input_lavalink_port}
LAVALINK_PASSWORD={input_lavalink_password}

OSU_API_KEY={input_osu_api_key}
"""
        open('./.env', 'w').write(config)
        print("\n[*] Successfully created .env file!")
        print("Teapot.py setup complete! Starting bot in 5 seconds...")
        time.sleep(5)
        print('\n' * 100)
    except Exception as e:
        print("\n[!] An error occurred when creating config file.\n" + str(e))
        quit()
