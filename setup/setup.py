#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 setup script."""

import os
from configparser import ConfigParser
from pathlib import Path

import requests

config_object = ConfigParser()
config_file = Path("config/config.ini")

print('--------------------------')
print('| Pyre Bot Setup Program |')
print('--------------------------')
print('Enter the values to configure the bot')

api = str(input('Discord API token: '))
role = str(input('Privileged Server Role: '))
admin_channel = str(input('Discord Channel ID for admin commands: '))
commands_channel = str(input('Discord Channel ID for normal commands: '))
svraddr = str(input('Server Address: '))
svrport = str(input('Server Port: '))
steamcmd = str(input('Path to SteamCMD folder: '))
ror2ds = str(input('Path to Risk of Rain Server folder: '))
bepinex = str(input('Path to BepInEx folder: '))
logpath = str(input('Path to Server Logs folder: '))  # NEW
chat_channels = str(input('Discord Channel ID(s) for game chat output, separated by commas: '))  # CHANGED

# Stat tracking
stats = True
while stats is True:
    track = str(input('Would you like to track stats? Enter "Yes" or "No": ')).lower()
    if track == "yes":
        linked_id = str(input('Role ID for linked members: '))
        print(' -- DynamoDB information --')
        stats_region = str(input('AWS Region: '))
        stats_endpoint = str(input('AWS Endpoint URL: '))
        print(' -- DynamoDB Table information --')
        stats_server = str(input('Server stats table name: '))
        stats_players = str(input('Linked member table name: '))
        stats_discord = str(input('Member join/leave table name: '))

        config_object["API"] = {
            "discord_token": api
        }
        config_object["AWS"] = {
            "stats_region": stats_region,
            "stats_endpoint": stats_endpoint,
            "stats_table": stats_server,
            "stats_players": stats_players,
            "discord_table": stats_discord
        }
        config_object["General"] = {
            "role": role,
            "linked-id": linked_id,
            "admin-channel": admin_channel,
            "commands-channel": commands_channel,
            "chat-channels": chat_channels,
            "track_stats": "yes"
        }
        config_object["RoR2"] = {
            "server_address": svraddr,
            "server_port": svrport,
            "steamcmd": steamcmd,
            "ror2ds": ror2ds,
            "BepInEx": bepinex,
            "server-logs-path": logpath,
            "auto-start-chat": "true",
            "auto-server-restart": "true",
            "server_restart_time": "7200",
            "hidden_mods": "[] "
        }
        stats = False
    elif track == "no":
        stats = False
    else:
        print('Invalid input')

config_object["API"] = {
    "discord_token": api
}
config_object["General"] = {
    "role": role,
    "admin-channel": admin_channel,
    "commands-channel": commands_channel,
    "chat-channels": chat_channels,
    "track_stats": "no"
}
config_object["RoR2"] = {
    "server_address": svraddr,
    "server_port": svrport,
    "steamcmd": steamcmd,
    "ror2ds": ror2ds,
    "BepInEx": bepinex,
    "server-logs-path": logpath,
    "auto-start-chat": "true",
    "auto-server-restart": "true",
    "server_restart_time": "7200",
    "hidden_mods": "[]"
}

try:
    with open(config_file, 'w') as conf:
        config_object.write(conf)
    print('Settings saved')
except Exception:
    print('Unable to save config.ini!')

install_plugin = str(input('Would you like to install BotCommands? Enter "Yes" or "No": ')).lower()
if install_plugin == 'yes':
    try:
        if bepinex:
            directory = Path(bepinex, 'plugins', 'BotCommands')
            file_dll = Path.joinpath(directory, 'BotCommands.dll')
            file_exe = Path.joinpath(directory, 'BotCommands_Dynamo.exe')
            botcmd = Path.joinpath(directory, 'botcmd.txt')
            os.makedirs(os.path.dirname(file_dll), exist_ok=True)
            os.makedirs(os.path.dirname(file_exe), exist_ok=True)
            print('Downloading files...')
            install_dll = requests.get(
                'https://github.com/SuperRayss/BotCommands/releases/latest/download/BotCommands.dll')
            install_exe = requests.get(
                'https://github.com/SuperRayss/BotCommands/releases/latest/download/BotCommands_Dynamo.exe')
            print('Copying files...')
            with open(file_dll, 'wb') as f:
                f.write(install_dll.content)
            with open(file_exe, 'wb') as f:
                f.write(install_exe.content)
            with open(botcmd, 'w'):
                pass
            print('BotCommands installed')
    except Exception:
        print('Unable to install BotCommands, please visit discord.pyre-bot.com for help.')
