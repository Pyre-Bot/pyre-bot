import json
import re
from configparser import ConfigParser
from pathlib import Path

players = []
dataDict = {}

# NOTE: stages_cleared currently counts stage progression in the sense that if you join the lobby and then start stage 1, you have "cleared" 1 stage, since the value uses the current stage number
# TODO: Come up with way to save time and stages progressed when the run ends, rather than a player leaving. Maybe create a global counters that operate separately of stagenum and run_timer, independently for each player object
class Player:
    def __init__(self, player_id, start_time, stages_cleared):
        self.player_id = player_id
        self.time = start_time
        self.stages_cleared = stages_cleared


config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]
general = config_object["General"]
server_address = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')


async def add_player(line, time, stages_cleared):
    global players
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    players.append(Player(player_id, time, stages_cleared))
    

async def player_leave(line, time, stages_cleared):
#    print('stages_cleared: ' + str(stages_cleared))  # DEBUG
    global players
    global dataDict
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    try:
        with open('data.json', 'r') as f:
            dataDict = json.load(f)
#        print('player_leave JSON file loaded')  # DEBUG
    except Exception:
        print('No JSON file')  # DEBUG
    try:  # Just some early groundwork until a real way to handle it is done
        print('Player joined - ' + str(dataDict[player_id]))
    except:
#        print('could not print, likely doesnt exist')
        dataDict[player_id] = {
        'Time Played' : 0,
        'Stages Cleared' : 0
        }
    for player in players:
        if player.player_id == player_id:
            for pid,value in dataDict.items():
                if pid == player.player_id:
#                    print('pid match')  # DEBUG
                    player.time = (time - player.time) + value['Time Played']
                    player.stages_cleared = (stages_cleared - player.stages_cleared) + value['Stages Cleared']
#                    print('player_leave complete')  # DEBUG
                    await update_json(player.player_id)
#        else:
#            print("Doesn't match")  # DEBUG


async def update_json(player_id):
    global players
    global dataDict
    for player in players:
        if player.player_id == player_id:
            dataDict[player.player_id] = {
                'Time Played' : player.time,
                'Stages Cleared' : player.stages_cleared
                }
#            print('writing dataDict: ' + str(dataDict))  # DEBUG
            players.remove(player)
            with open('data.json', 'w') as f:
                json.dump(dataDict, f, indent=4)
#            print('update_json complete')  # DEBUG
