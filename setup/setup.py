import os
import tkinter as tk
from configparser import ConfigParser
from pathlib import Path
from tkinter import messagebox

import requests

config_object = ConfigParser()
config_file = Path("config/config.ini")

window = tk.Tk()
window.title('Discord Bot Setup')
window.geometry('400x475')

api = ''
role = ''
admin_channel = ''
commands_channel = ''
svraddr = ''
svrport = ''
steamcmd = ''
ror2ds = ''
bepinex = ''
channel = ''
file = ''


def save():
    """Saves the settings to the configuration file."""
    global bepinex
    api = api_entry.get()
    role = role_entry.get()
    admin_channel = admin_entry.get()
    commands_channel = commands_entry.get()
    svraddr = svraddr_entry.get()
    svrport = svrport_entry.get()
    steamcmd = steamcmd_entry.get()
    ror2ds = ror2ds_entry.get()
    bepinex = bepinex_entry.get()
    channel = channel_entry.get()

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
        "hidden_mods": "['R2API', 'Configuration', 'DeployableOwnerInformation', 'FluffyLabsConfigManagerTools', 'SteamBuildID', 'MiniRpcLib', 'HjUpdaterAPI']"
    }
    with open(config_file, 'w') as conf:
        config_object.write(conf)

    confirmation()


def confirmation():
    """Shows window stating if file was created or not."""
    if os.path.exists(config_file):
        messagebox.showinfo('Settings Saved', 'Settings saved successfully!')
    else:
        messagebox.showerror('Error', 'Unable to save config.ini file!')


def botcmd():
    """Installs the BotCommands plugin."""
    global file
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
        botcmd_confirmation()


def botcmd_confirmation():
    """Confirms plugin was isntalled"""
    if os.path.exists(file):
        messagebox.showinfo('Plugin installed',
                            'Installed BotCommands plugin successfully!')
    else:
        messagebox.showerror('Error', 'Unable to install plugin')


label = tk.Label(
    window, text="Use the following options to configue your bot settings")
api_label = tk.Label(
    window, text="Discord API Token")
api_entry = tk.Entry(window, width=50, textvariable=api)
role_label = tk.Label(
    window, text="Priveledged Server Role")
role_entry = tk.Entry(window, width=50, textvariable=role)
admin_label = tk.Label(
    window, text="Discord Channel ID for admin commands")
admin_entry = tk.Entry(window, width=50, textvariable=admin_channel)
commands_label = tk.Label(
    window, text="Discord Channel ID for normal commands")
commands_entry = tk.Entry(window, width=50, textvariable=commands_channel)
svraddr_label = tk.Label(
    window, text="Server Address")
svraddr_entry = tk.Entry(window, width=50, textvariable=role)
svrport_label = tk.Label(
    window, text="Server Port")
svrport_entry = tk.Entry(window, width=50, textvariable=role)
steamcmd_label = tk.Label(
    window, text="Path to SteamCMD folder")
steamcmd_entry = tk.Entry(window, width=50, textvariable=role)
ror2ds_label = tk.Label(
    window, text="Path to Risk of Rain Server folder")
ror2ds_entry = tk.Entry(window, width=50, textvariable=role)
bepinex_label = tk.Label(
    window, text="Path to BepInEx folder")
bepinex_entry = tk.Entry(window, width=50, textvariable=role)
channel_label = tk.Label(
    window, text="Discord Channel ID for game chat output")
channel_entry = tk.Entry(window, width=50, textvariable=role)


save = tk.Button(window, text="Save Settings", command=save)
botcmd = tk.Button(window, text="Install BotCommands Plugin", command=botcmd)

label.pack()
api_label.pack()
api_entry.pack()
role_label.pack()
role_entry.pack()
admin_label.pack()
admin_entry.pack()
commands_label.pack()
commands_entry.pack()
svraddr_label.pack()
svraddr_entry.pack()
svrport_label.pack()
svrport_entry.pack()
steamcmd_label.pack()
steamcmd_entry.pack()
ror2ds_label.pack()
ror2ds_entry.pack()
bepinex_label.pack()
bepinex_entry.pack()
channel_label.pack()
channel_entry.pack()
save.pack()
botcmd.pack()

window.mainloop()
