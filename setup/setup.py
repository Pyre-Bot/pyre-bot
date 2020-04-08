#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 setup script."""

import os
from configparser import ConfigParser
from pathlib import Path

import requests

config_object = ConfigParser()
config_file = Path("config/config.ini")

print('----------------------')
print('Pyre Bot Setup Program')
print('----------------------')
print('Enter the values to configure the bot')

api = str(input('Discord API token: '))
role = str(input('Priveledged Server Role: '))
admin_channel = str(input('Discord Channel ID for admin commands: '))
commands_channel = str(input('Discord Channel ID for normal commands: '))
svraddr = str(input('Server Address: '))
svrport = str(input('Server Port: '))
steamcmd = str(input('Path to SteamCMD folder: '))
ror2ds = str(input('Path to Risk of Rain Server folder: '))
bepinex = str(input('ath to BepInEx folder: '))
channel = str(input('Discord Channel ID for game chat output: '))

config_object["API"] = {
    "discord_token": api
}
config_object["General"] = {
    "role": role,
    "admin-channel": admin_channel,
    "commands-channel": commands_channel
}
config_object["RoR2"] = {
    "server_address": svraddr,
    "server_port": svrport,
    "steamcmd": steamcmd,
    "ror2ds": ror2ds,
    "BepInEx": bepinex,
    "channel": channel,
    "auto-start-chat": "true",
    "auto-server-restart": "true",
    "hidden_mods": "['R2API', 'Configuration', 'DeployableOwnerInformation', 'FluffyLabsConfigManagerTools', 'MiniRpcLib', 'HjUpdaterAPI']"
}
try:
    with open(config_file, 'w') as conf:
        config_object.write(conf)
    print('Settings saved')
except Exception:
    print('Unable to save config.ini!')

install_plugin = input('Would you like to install BotCommands (y or n)? ')
if install_plugin == 'y' or install_plugin == 'Y':
    try:
        if bepinex:
            directory = Path(bepinex, 'plugins', 'BotCommands')
            file = Path.joinpath(directory, 'BotCommands.dll')
            botcmd = Path.joinpath(directory, 'botcmd.txt')
            os.makedirs(os.path.dirname(file), exist_ok=True)
            install = requests.get(
                'https://github.com/SuperRayss/BotCommands/releases/download/v0.1.2/BotCommands.dll')
            with open(file, 'wb') as f:
                f.write(install.content)
            with open(botcmd, 'w'):
                pass
            print('BotCommands installed')
    except Exception:
        print('Unable to install BotCommands, please visit discord.pyre-bot.com for help.')
