import json
import re
from configparser import ConfigParser
from pathlib import Path

players = []
dataDict = {}


class Player:
    def __init__(self, player_id, start_time):
        self.id = player_id
        self.time = start_time


config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]
general = config_object["General"]
server_address = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')


async def load_json():
    global dataDict
    try:
        with open('data.json', 'r') as f:
            dataDict = json.load(f)
    except Exception:
        print('No JSON file')


async def add_player(player_id, time):
    global players
    players.append(Player(player_id, time))


async def update_json(player_id):
    global dataDict
    for player in players:
        if player.id == player_id:
            player_dict = dataDict[player.id]
            player_dict['time'] += player.time
            dataDict[player.id] = player_dict
            players.remove(player)
            with open('data.json', 'w') as f:
                json.dump(dataDict, f, indent=4)
            await load_json()


async def player_leave(player_id, time):
    global players
    for player in players:
        if player.id == player_id:
            player.time = time - player.time
            await update_json(player.id)
        else:
            print("Doesn't match")
