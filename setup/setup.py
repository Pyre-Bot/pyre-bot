import os
import tkinter as tk
from configparser import ConfigParser
from pathlib import Path
from tkinter import messagebox

config_object = ConfigParser()
config_file = Path("config/config.ini")

window = tk.Tk()
window.title('Discord Bot Setup')
window.geometry('400x425')

api = ''
role = ''
svraddr = ''
svrport = ''
steamcmd = ''
ror2ds = ''
bepinex = ''
botcmd = ''
channel = ''


def save():
    api = api_entry.get()
    role = role_entry.get()
    svraddr = svraddr_entry.get()
    svrport = svrport_entry.get()
    steamcmd = steamcmd_entry.get()
    ror2ds = ror2ds_entry.get()
    bepinex = bepinex_entry.get()
    botcmd = botcmd_entry.get()
    channel = channel_entry.get()

    config_object["API"] = {
        "discord_token": api
    }
    config_object["General"] = {
        "role": role
    }
    config_object["RoR2"] = {
        "server_address": svraddr,
        "server_port": svrport,
        "steamcmd": steamcmd,
        "ror2ds": ror2ds,
        "BepInEx": bepinex,
        "botcmd": botcmd,
        "channel": channel,
        "auto-start-chat": "true",
        "auto-server-restart": "true",
        "hidden_mods": "['R2API', 'Configuration', 'DeployableOwnerInformation', 'FluffyLabsConfigManagerTools', 'SteamBuildID', 'MiniRpcLib', 'HjUpdaterAPI']"
    }
    with open(config_file, 'w') as conf:
        config_object.write(conf)

    confirmation()


def confirmation():
    if os.path.exists(config_file):
        messagebox.showinfo('Settings Saved', 'Settings saved successfully!')
    else:
        messagebox.showerror('Error', 'Unable to save config.ini file!')


label = tk.Label(
    window, text="Use the following options to configue your bot settings")
api_label = tk.Label(
    window, text="Discord API Token")
api_entry = tk.Entry(window, width=50, textvariable=api)
role_label = tk.Label(
    window, text="Priveledged Server Role")
role_entry = tk.Entry(window, width=50, textvariable=role)
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
botcmd_label = tk.Label(
    window, text="Location of botcmd.txt")
botcmd_entry = tk.Entry(window, width=50, textvariable=role)
channel_label = tk.Label(
    window, text="Discord Channel ID for game chat output")
channel_entry = tk.Entry(window, width=50, textvariable=role)


save = tk.Button(window, text="Save Settings", command=save)
# file = filedialog.askopenfilename()

label.pack()
api_label.pack()
api_entry.pack()
role_label.pack()
role_entry.pack()
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
botcmd_label.pack()
botcmd_entry.pack()
channel_label.pack()
channel_entry.pack()
save.pack()

window.mainloop()
