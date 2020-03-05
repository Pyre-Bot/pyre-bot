import json
import re

dataDict = {}

# NOTE: Bug I noticed, if you launch the bot after a game has started and people have joined, this won't get called before update_stats and so weird things happen
# One fix for this could be to call this function on startup of the bot, get all players from the server info with server()
# That gives me an idea actually, we should be getting steam IDs from the server info if possible, rather than from chat output
async def add_player(line, time, stages_cleared):
    global dataDict
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    dataDict[player_id] = {
    'Time Played' : time,
    'Stages Cleared' : stages_cleared,
    'Runs Completed' : 0
    }

# TODO: Save stats at the end of a run using IL hooking on run_end (if possible, otherwise find another way)
async def update_stats(time, stages_cleared, runcompleted=0):
    global dataDict
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
        value['Runs Completed'] = runcompleted - value['Runs Completed']
        jsonvalue = loadJSON.get(pid)
        if jsonvalue != None:
            jsonvalue['Time Played'] = value['Time Played'] + jsonvalue['Time Played']
            jsonvalue['Stages Cleared'] = value['Stages Cleared'] + jsonvalue['Stages Cleared']
            jsonvalue['Runs Completed'] = value['Runs Completed'] + jsonvalue['Runs Completed']
#            loadJSON[pid] = {
#                'Time Played' : jsonvalue['Time Played'],
#                'Stages Cleared' : jsonvalue['Stages Cleared'],
#                'Runs Completed' : jsonvalue['Runs Completed']
#            }
        else:
            loadJSON[pid] = {
                'Time Played' : value['Time Played'],
                'Stages Cleared' : value['Stages Cleared'],
                'Runs Completed' : value['Runs Completed']
            }
        value['Time Played'] = time
        value['Stages Cleared'] = stages_cleared
        value['Runs Completed'] = runcompleted
#    print('player_leave complete')  # DEBUG
    await write_json(loadJSON)


async def write_json(jsonobj):
#    print('writing jsonobj: ' + str(jsonobj))  # DEBUG
    with open('data.json', 'w') as f:
        json.dump(jsonobj, f, indent=4)
#    print('write_json complete')  # DEBUG
