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

discord_api = str(input('Discord API token: '))
seq_api = str(input('Seq API token: '))
role = str(input('Privileged Server Role: '))
admin_channels = str(input('Discord Channel ID for admin commands, separated by commas: '))  # CHANGED
commands_channels = str(input('Discord Channel ID for normal commands, separated by commas: '))  # CHANGED
server_addresses = str(input('Server Addresses with ports (i.e. address:port), separated by commas: '))  # CHANGED
logpath = str(input('Path to Server Logs folder: '))  # NEW
chat_channels = str(input('Discord Channel ID(s) for game chat output, separated by commas: '))  # CHANGED

# Stat tracking
stats = True
while stats is True:
    track = str(input('Would you like to track stats? Enter "Y" or "N": ')).lower()
    if track.lower() == "y":  # Added lower since this never seemed to pick up the input correctly
        linked_id = str(input('Role ID for linked members: '))
        print(' -- DynamoDB information --')
        stats_region = str(input('AWS Region: '))
        stats_endpoint = str(input('AWS Endpoint URL: '))
        print(' -- DynamoDB Table information --')
        stats_server = str(input('Server stats table name: '))
        stats_players = str(input('Linked member table name: '))
        stats_discord = str(input('Member join/leave table name: '))

        config_object["API"] = {
            "discord_token": discord_api,
            "seq-api-key": seq_api
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
            "admin-channels": admin_channels,
            "commands-channels": commands_channels,
            "chat-channels": chat_channels,
            "track_stats": "yes"
        }
        config_object["RoR2"] = {
            "server_addresses": server_addresses,
            "server-logs-path": logpath,
            "auto-start-chat": "true",
            "auto-server-restart": "true",
            "server_restart_time": "7200"
        }
        stats = False
    elif track.lower() == "n":
        stats = False
    else:
        print('Invalid input')

# TODO: Change this to not re-write values for every field
config_object["API"] = {
    "discord_token": discord_api,
    "seq-api-key": seq_api
}
config_object["General"] = {
    "role": role,
    "admin-channels": admin_channels,
    "commands-channels": commands_channels,
    "chat-channels": chat_channels,
    "track_stats": "no"
}
config_object["RoR2"] = {
    "server_addresses": server_addresses,
    "server-logs-path": logpath,
    "auto-start-chat": "true",
    "auto-server-restart": "true",
    "server_restart_time": "7200"
}

try:
    with open(config_file, 'w') as conf:
        config_object.write(conf)
    print('Settings saved')
except Exception:
    print('Unable to save config.ini!')
