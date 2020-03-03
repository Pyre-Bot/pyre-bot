import json
import re
from configparser import ConfigParser
from pathlib import Path

config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]
general = config_object["General"]
server_address = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')

dataDict = {}

# TODO: Come up with way to save time and stages progressed when the run ends, rather than a player leaving. Maybe create a global counters that operate separately of stagenum and run_timer, independently for each player object

async def add_player(line, time, stages_cleared):
    global dataDict
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    dataDict[player_id] = {
    'Time Played' : time,
    'Stages Cleared' : stages_cleared
    }

# TODO: Save stats at the end of a run using IL hooking on run_end (if possible, otherwise find another way)
async def update_stats(time, stages_cleared):
    global dataDict
    stages_cleared = stages_cleared - 1  # Required currently due to the way stages_cleared works
    try:
        with open('data.json', 'r') as fr:
            loadJSON = json.load(fr)
#        print('player_leave JSON file loaded')  # DEBUG
    except Exception:
        with open('data.json', 'w') as fw:
            json.dump(dataDict, fw, indent=4)
        with open('data.json', 'r') as fr:
            loadJSON = json.load(fr)
        print('JSON file created')  # DEBUG
    for pid, value in dataDict.items():
        value['Time Played'] = time - value['Time Played']
        value['Stages Cleared'] = stages_cleared - value['Stages Cleared']
        jsonvalue = loadJSON.get(pid)  # I do not at all understand how the commented out code below is not required to reassign those values to loadJSON. Somehow this works without it. I'm not galaxy brained enough to get it, but okay
        if jsonvalue != None:
            jsonvalue['Time Played'] = value['Time Played'] + jsonvalue['Time Played']
            jsonvalue['Stages Cleared'] = value['Stages Cleared'] + jsonvalue['Stages Cleared']
#            loadJSON[pid] = {
#                'Time Played' : jsonvalue['Time Played'],
#                'Stages Cleared' : jsonvalue['Stages Cleared'],
#            }
        else:
            loadJSON[pid] = {
                'Time Played' : value['Time Played'],
                'Stages Cleared' : value['Stages Cleared']
            }
        value['Time Played'] = time
        value['Stages Cleared'] = stages_cleared

#    print('player_leave complete')  # DEBUG
    await write_json(loadJSON)


async def write_json(jsonobj):
#    print('writing jsonobj: ' + str(jsonobj))  # DEBUG
    with open('data.json', 'w') as f:
        json.dump(jsonobj, f, indent=4)
#    print('write_json complete')  # DEBUG
