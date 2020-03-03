import json
import re
from configparser import ConfigParser
from pathlib import Path

players = []
dict = {}


class Player:
    def __init__(self, id, start_time):
        self.id = id
        self.time = start_time


config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]
general = config_object["General"]
server_address = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')

db = Path.cwd().joinpath('data.json')


async def load_json():
    global dict
    try:
        with open('data.json', 'r') as f:
            dict = json.load(f)
    except Exception:
        print('No JSON file')


async def add_player(line, time):
    global players
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    players.append(Player(player_id, time))


async def update_json(player_id):
    global dict
    for player in players:
        if player.id == player_id:
            player_dict = dict[player.id]
            player_dict['time'] += player.time
            dict[player.id] = player_dict
            players.remove(player)
            with open('data.json', 'w') as f:
                json.dump(dict, f, indent=4)
            await load_json()


async def player_leave(line, time):
    global players
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    for player in players:
        if player.id == player_id:
            player.time = time - player.time
            await update_json(player.id)
        else:
            print('Doesnt match')
            