import ast
from configparser import ConfigParser
from pathlib import Path
import os

import boto3


# Base configuration variables
config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)

# Assigns the variables. Try/Except is used in case the config.ini file doesn't exist
try:
    api = config_object["API"]
    aws = config_object["AWS"]
    general = config_object["General"]
    ror2 = config_object["RoR2"]

    discord_token = api["discord_token"]
    seq_api = api["seq-api-key"]  # NEW
    role = general["role"]
    # Creating ordered lists, will create dict objects for each one
    admin_channels = general["admin-channels"].split(',')  # CHANGED TO LIST
    commands_channels = general["commands-channels"].split(',')  # CHANGED TO LIST
    chat_channels = general["chat-channels"].split(',')  # CHANGED TO LIST, MOVED TO GENERAL
    track_stats = general["track_stats"]
    server_addresses = config_object.get(
        'RoR2', 'server_addresses').split(',')  # CHANGED TO LIST
    logpath = Path(ror2["server-logs-path"])  # NEW
    chat_autostart = ror2["auto-start-chat"]
    server_restart = ror2["auto-server-restart"]
    server_restart_interval = ror2["server_restart_time"]

    # Stat tracking variables. Try/Except used in case stat tracking is disabled
    try:
        linked_id = int(general["linked-id"])
        stats_region = aws["stats_region"]
        stats_endpoint = aws["stats_endpoint"]
        dynamodb = boto3.resource('dynamodb', region_name=stats_region, endpoint_url=stats_endpoint)
        stats_table = dynamodb.Table(aws["stats_table"])
        stats_players = dynamodb.Table(aws["stats_players"])
        discord_table = dynamodb.Table(aws["discord_table"])
    except KeyError:
        pass

    # Other configuration variables not set by setup.py
    request_url = 'https://steamid.io/lookup/'
    server_list = []
    for i in range(len(server_addresses)):
        server_address = server_addresses[i].split(':')
        server_address[1] = int(server_address[1])
        server_address = tuple(server_address)
        server_list.append(
            {
                "server_address": server_address,
                "admin_channel": admin_channels[i],
                "commands_channel": commands_channels[i],
                "chat_channel": chat_channels[i]
            }
        )
except KeyError:
    pass
