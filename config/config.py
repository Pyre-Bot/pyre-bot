from pathlib import Path
import os
import logging

from pytz import timezone
import boto3


tz = timezone('US/Eastern')  # Sets timezone to Eastern
t_fmt = '%Y-%m-%d %H:%M:%S %Z%z'  # Configures time output format
i_fmt = '%I:%M%p %Z'  # Configures time format for info

# Assigns the variables
try:
    discord_token = os.environ.get('DISCORD_TOKEN')
    seq_api = os.environ.get('SEQ_API')
    role = os.environ.get('ADMIN_ROLE')
    admin_channels = os.environ.get('ADMIN_CHANNELS').split(',')
    commands_channels = os.environ.get('COMMANDS_CHANNELS').split(',')
    track_stats = os.environ.get('TRACK_STATS')
    server_addresses = os.environ.get('SERVER_ADDRESSES').split(',')
    print('addresses:' + str(server_addresses))  # DEBUG
    admin_update_channel = int(os.environ.get('SERVER_UPDATES'))
    print('admin:' + str(admin_update_channel))  # DEBUG
    server_update_channel = int(os.environ.get('SERVER_CHANNEL'))
    print('updates:' + str(server_update_channel))  # DEBUG
    leaderboard_update_channel = int(os.environ.get('LEADERBOARD_CHANNEL'))

    # Logging level
    if os.environ.get('LOG_LEVEL') == 'info':
        log_level = logging.getLevelName('INFO')
    elif os.environ.get('LOG_LEVEL') == 'debug':
        log_level = logging.getLevelName('DEBUG')

    # Stat tracking variables. Try/Except used in case stat tracking is disabled
    try:
        linked_id = int(os.environ.get('LINKED_ID'))
        stats_region = os.environ.get('STATS_REGION')
        stats_endpoint = os.environ.get('STATS_ENDPOINT')
        dynamodb = boto3.resource('dynamodb', region_name=stats_region, endpoint_url=stats_endpoint)
        stats_table = dynamodb.Table(os.environ.get('STATS_TABLE'))
        stats_players = dynamodb.Table(os.environ.get('PLAYERS_TABLE'))
        discord_table = dynamodb.Table(os.environ.get('DISCORD_TABLE'))
        ban_table = dynamodb.Table(os.environ.get('BAN_TABLE'))
        leaderboard_table = dynamodb.Table(os.environ.get('LEADERBOARD_TABLE'))
    except KeyError:
        pass

    request_url = 'https://steamid.io/lookup/'
    server_list = []
    for i in range(len(server_addresses)):
        server_address = server_addresses[i].split(':')
        server_address[1] = int(server_address[1])
        server_address = tuple(server_address)
        server_list.append(
            {
                "server_name": "Server" + str(i + 1),  # Change to use steam info fetch?
                "server_address": server_address,
                "admin_channel": admin_channels[i],
                "commands_channel": commands_channels[i]
            }
        )

except KeyError:
    pass
