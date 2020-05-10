import ast
from configparser import ConfigParser
from pathlib import Path

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
    role = general["role"]
    admin_channel = int(general["admin-channel"])
    commands_channel = int(general["commands-channel"])
    track_stats = general["track_stats"]
    server_address = config_object.get(
        'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')
    steamcmd = Path(ror2["steamcmd"])
    ror2ds = Path(ror2["ror2ds"])
    bepinex = Path(ror2["bepinex"])
    chat_channel = ror2["channel"]
    chat_autostart = ror2["auto-start-chat"]
    server_restart = ror2["auto-server-restart"]
    server_restart_interval = ror2["server_restart_time"]
    hidden_mods = ast.literal_eval(config_object.get('RoR2', 'hidden_mods'))

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
    botcmd = Path.joinpath(bepinex, 'plugins', 'BotCommands')
    logfile = (bepinex / "LogOutput.log")
    request_url = 'https://steamid.io/lookup/'
except KeyError:
    pass
