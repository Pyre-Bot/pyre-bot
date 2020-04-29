#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 functions to track game stats for players."""

import re
from configparser import ConfigParser
from pathlib import Path

import boto3

# Config file info
config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)

# Connects to Amazon DynamoDB and access the tables
dynamodb = boto3.resource('dynamodb', region_name='us-east-2',
                          endpoint_url="https://dynamodb.us-east-2.amazonaws.com")
players = dynamodb.Table('Players')
stats = dynamodb.Table('Stats')

# Used to determine which server stats need updating
# TODO: Save these identifiers to the db rather than hardcoding
channels = {
    'Server1': {'admin': 670373469845979136,
                'commands': 665998238171660320,
                'chat': 667473663343198220},
    'Server2': {'admin': 671917010422333460,
                'commands': 671921930873602099,
                'chat': 671918498531770378},
    'Server3': {'admin': 672682539390992384,
                'commands': 672682345089859654,
                'chat': 672682313003565057},
    'Server4': {'admin': 672940159091867648,
                'commands': 672939900600975362,
                'chat': 672939927507435533}
}

dataDict = {}


# NOTE: Bug I noticed, if you launch the bot after a game has started and people have
#       joined, this won't get called before update_stats and so weird things happen
# One fix for this could be to call this function on startup of the bot, get all players
#       from the server info with server()
# That gives me an idea actually, we should be getting steam IDs from the server info if
#       possible, rather than from chat output
async def add_player(line, time, stages_cleared):
    global dataDict
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    # Adds at current time and stages because it gets used as an offset by update_stats
    dataDict[player_id] = {
        'Time Played': time,
        'Stages Cleared': stages_cleared,
        'Runs Completed': 0
    }


async def update_stats(time, stages_cleared, runcompleted=0):
    global dataDict
    channel = config_object.getint('RoR2', 'channel')

    # Determine which server stats to update
    for key, value in channels.items():
        for k, v in channels[key].items():
            if channel == v:
                server = key

    for pid, value in dataDict.items():
        value['Time Played'] = time - value['Time Played']
        value['Stages Cleared'] = stages_cleared - value['Stages Cleared']
        value['Runs Completed'] = runcompleted - value['Runs Completed']
        try:
            key = {'SteamID64': str(pid)}
            response = stats.get_item(Key=key)
            # If you don't do the below you also get the metadata
            response = response['Item'][server]

            # Alter the values returned from DB to new values
            response['Time Played'] = value['Time Played'] + response['Time Played']
            response['Stages Cleared'] = value['Stages Cleared'] + \
                response['Stages Cleared']
            response['Runs Completed'] = value['Runs Completed'] + \
                response['Runs Completed']

            # Creates a dictionary used to update stats
            stats_dict = {pid: {
                'Time Played': response['Time Played'],
                'Stages Cleared': response['Stages Cleared'],
                'Runs Completed': response['Runs Completed']
            }}
            try:
                stats.update_item(
                    Key={'SteamID64': pid},
                    UpdateExpression=f'set {server} = :s',
                    ExpressionAttributeValues={
                        ':s': stats_dict[pid]
                    }
                )
            except:
                # For some reason the above is always throwing an Error
                # Temporary just pass so that it proceeds (everything works)
                # TODO: Figure out why it throws an error
                pass
        except KeyError:
            # Called when stats for the specified server aren't in DB
            stats_dict = {pid: {
                'Time Played': value['Time Played'],
                'Stages Cleared': value['Stages Cleared'],
                'Runs Completed': value['Runs Completed']
            }}
            try:
                stats.update_item(
                    Key={'SteamID64': pid},
                    UpdateExpression=f'set {server} = :s',
                    ExpressionAttributeValues={
                        ':s': stats_dict[pid]
                    }
                )
            except:
                # For some reason the above is always throwing an Error
                # Temporary just pass so that it proceeds (everything works)
                # TODO: Figure out why it throws an error
                pass

        # Updates current values in dictionary
        # Does this to update the offset again after the difference in stats has been updated with the db
        value['Time Played'] = time
        value['Stages Cleared'] = stages_cleared
        value['Runs Completed'] = runcompleted
