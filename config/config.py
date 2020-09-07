from pathlib import Path
import os

import boto3


# Assigns the variables
try:
    discord_token = os.environ.get('DISCORD_TOKEN')
    seq_api = os.environ.get('SEQ_API')
    role = os.environ.get('ADMIN_ROLE')
    # Creating ordered lists, will create dict objects for each one
    admin_channels = os.environ.get('ADMIN_CHANNELS').split(',')  # CHANGED TO LIST
    commands_channels = os.environ.get('COMMANDS_CHANNELS').split(',')  # CHANGED TO LIST
    chat_channels = os.environ.get('CHAT_CHANNELS').split(',')  # CHANGED TO LIST, MOVED TO GENERAL
    track_stats = os.environ.get('TRACK_STATS')
    server_addresses = os.environ.get('SERVER_ADDRESSES').split(',')  # CHANGED TO LIST
    logpath = Path(os.environ.get('LOG_PATH'))  # NEW
    chat_autostart = os.environ.get('CHAT_AUTOSTART')
    server_restart = os.environ.get('SERVER_RESTART')
    server_restart_interval = os.environ.get('SERVER_RESTART_TIME')

    # Stat tracking variables. Try/Except used in case stat tracking is disabled
    try:
        linked_id = int(os.environ.get('LINKED_ID'))
        stats_region = os.environ.get('STATS_REGION')
        stats_endpoint = os.environ.get('STATS_ENDPOINT')
        dynamodb = boto3.resource('dynamodb', region_name=stats_region, endpoint_url=stats_endpoint)
        stats_table = dynamodb.Table(os.environ.get('STATS_TABLE'))
        stats_players = dynamodb.Table(os.environ.get('PLAYERS_TABLE'))
        discord_table = dynamodb.Table(os.environ.get('DISCORD_TABLE'))
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
                "server_name": "Server" + str(i + 1),
                "server_address": server_address,
                "admin_channel": admin_channels[i],
                "commands_channel": commands_channels[i],
                "chat_channel": chat_channels[i]
            }
        )
except KeyError:
    pass
