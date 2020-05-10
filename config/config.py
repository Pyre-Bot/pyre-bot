from configparser import ConfigParser
from pathlib import Path

config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)

api = config_object["API"]
aws = config_object["AWS"]
general = config_object["General"]
ror2 = config_object["RoR2"]

discord_token = api["discord_token"]
stats_region = aws["stats_region"]
stats_endpoint = aws["stats_endpoint"]
stats_table = aws["stats_table"]
discord_table = aws["discord_table"]
role = general["role"]
linked_id = int(general["linked-id"])
admin_channel = general["admin-channel"]
commands_channel = general["commands-channel"]
server_address = ror2["server_address"]
server_port = ror2["server_port"]
steamcmd = ror2["steamcmd"]
ror2ds = ror2["ror2ds"]
bepinex = ror2["bepinex"]
chat_channel = ror2["channel"]
chat_autostart = ror2["auto-start-chat"]
server_restart = ror2["auto-server-restart"]
server_restart_interval = ror2["server_restart_time"]
hidden_mods = ror2["hidden_mods"]

botcmd = Path.joinpath(bepinex, 'plugins', 'BotCommands')
logfile = (bepinex / "LogOutput.log")
