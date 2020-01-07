# bot.py
import os
import psutil
import asyncio
# Discord Imports
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import has_role
# Cassiopeia / LoL imports
import cassiopeia as cass
from cassiopeia import Summoner
# Steam imports
import valve.source.a2s

# Get token info from .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
rtoken = os.getenv('RIOT_TOKEN')
bot = commands.Bot(command_prefix=('r!', 'ig!', '>'))

# Riot API and Cassiopeia info
# This overrides the value set in your configuration/settings.
cass.set_riot_api_key(rtoken)
cass.set_default_region("NA")

# Steam server information
SERVER_ADDRESS = ('ror2.infernal.wtf', 27016)

# Do this when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# RoR2 stuff
# Start the RoR2 server
@bot.command(name='start', help='Starts the server if it is not running')
@commands.has_role('RoR2 Admin')
async def start(ctx):
    # Checks to make sure the server is not running before starting it
    for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
        await ctx.send('Server is already running!')
        break
    else:
        started = 1
        # Path of log file, removes before starting
        if os.path.exists(r"C:\steamcmd\ror2ds\BepInEx\LogOutput.log"):
            os.remove(r"C:\steamcmd\ror2ds\BepInEx\LogOutput.log")

        # Starts the server
        os.startfile(r"C:\steamcmd\ror2ds\Risk of Rain 2.exe")
        await ctx.send('Starting Risk of Rain 2 Server, please wait...')
        await asyncio.sleep(30)

        # After 30 seconds checks logs to see if server started
        while started == 1:
            with open(r"C:\steamcmd\ror2ds\BepInEx\LogOutput.log") as f:
                for line in f:
                    if "Loaded scene lobby" in line:
                        await ctx.send('Server started successfully...')
                        started = 2
                        break

# Runs the update bat file, updates server via SteamCMD
@bot.command(name='update', help='Updates the server, must be off before running this')
@commands.has_role('RoR2 Admin')
async def update(ctx):
    # Checks to make sure the server is not running before updating it
    for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
        await ctx.send('Stop the server before running this (r!stop)')
        break
    else:
        os.startfile(r"C:\steamcmd\RoR2DSUpdate.bat")
        await ctx.send('Updating server, please wait...')
        updated = 1
        # Path of log file, removes before starting
        if os.path.exists(r"C:\steamcmd\logs\content_log.txt"):
            os.remove(r"C:\steamcmd\logs\content_log.txt")
            await asyncio.sleep(30)

        # After 30 seconds checks logs to see if server updated
        while updated == 1:
            with open(r"C:\steamcmd\logs\content_log.txt") as f:
                for line in f:
                    if "AppID 1180760 scheduler finished" in line:
                        await ctx.send('Server updated...')
                        updated = 2
                        break

# Exits the server
@bot.command(name='stop', help='Stops the server if currently running')
@commands.has_role('RoR2 Admin')
async def stop(ctx):
    for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
        process.kill()
        await ctx.send('Shutting down the server...')
        break
    else:
        await ctx.send('Server is not running!')

# Lists the mods used on the Server
@bot.command(name='mods', help='Displays the list of current mods')
async def mods(ctx):
    await ctx.send('Coming soon!')

# Displays the status of the Server
@bot.command(name='status', help='Displays the status of current session')
async def status(ctx):
    for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
        with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
            info = server.info()
            players = server.players()
            ping = server.ping()

        await ctx.send("{player_count}/{max_players} {server_name}".format(**info))
        for player in sorted(players["players"],
                             key=lambda p: p["score"], reverse=True):
            await ctx.send("{name}".format(**player))
        await ctx.send("\nServer ping is {:n}.".format(ping))
        break
    else:
        await ctx.send('Server is currently running...')

# Sends the Steam connection link
@bot.command(name='link', help='Get the Steam connection link')
async def link(ctx):
    await ctx.send('steam://connect/76.25.137.127:27015')

# Print server configuration
@bot.command(name='config', help='Prints the server configuration')
@commands.has_role('RoR2 Admin')
async def config(ctx):
    await ctx.send('Coming soon!')

# LoL stuff
# Get Summoner information
@bot.command(name='summoner')
async def summoner(ctx, arg):
    summoner = Summoner(name=arg)
    mastered = summoner.champion_masteries.filter(lambda cm: cm.level >= 6)
    print([cm.champion.name for cm in mastered])

# Discord bot token
try:
    bot.run(token)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
