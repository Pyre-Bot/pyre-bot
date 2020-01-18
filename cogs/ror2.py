import os
import psutil
import asyncio
from pathlib import Path
import discord
from discord.ext import commands
import valve.source.a2s
from configparser import ConfigParser
import re
from pygtail import Pygtail

config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]

# Config variables
SERVER_ADDRESS = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')
steamcmd = Path(ror2["steamcmd"])
ror2ds = Path(ror2["ror2ds"])
BepInEx = Path(ror2["BepInEx"])
role = ror2["role"]

# Global variables (yes, I know, not ideal but I'll fix them later)
yes, no = 0, 0
repeat = 0


# Function of chat
async def chat(self):
    file = (BepInEx / "LogOutput.log")
    channel = config_object.getint('RoR2', 'channel')
    channel = self.bot.get_channel(channel)
    if os.path.exists(file):
        if os.path.exists(BepInEx / "LogOutput.log.offset"):
            for line in Pygtail(str(file)):
                if "say" in line:
                    line = line[21:]
                    line = re.sub(r" ?\([^)]+\)", "", line)
                    line = line.replace(' issued', '')
                    line = line.replace(' say ', '')
                    await channel.send(line)
        else:
            for line in Pygtail(str(file)):
                pass


class RoR2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Start the RoR2 server
    @commands.command(name='start', help='Starts the server if it is not running')
    @commands.has_role(role)
    async def start(self, ctx):
        # Checks to make sure the server is not running before starting it
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            await ctx.send('Server is already running!')
            break
        else:
            started = 1
        # Path of log file, removes before starting
        if os.path.exists(BepInEx / "LogOutput.log"):
            os.remove(BepInEx / "LogOutput.log")

        # Starts the server
        os.startfile(ror2ds / "Risk of Rain 2.exe")
        await ctx.send('Starting Risk of Rain 2 Server, please wait...')
        await asyncio.sleep(15)

        # After 15 seconds checks logs to see if server started
        while started == 1:
            with open(BepInEx / "LogOutput.log") as f:
                for line in f:
                    if "Loaded scene lobby" in line:
                        await ctx.send('Server started successfully...')
                        started = 2
                        break
    # Exits the server
    @commands.command(name='stop', help='Stops the server if currently running')
    @commands.has_role(role)
    async def stop(self, ctx):
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            process.kill()
            await ctx.send('Risk of Rain 2 server shut down...')
            break
        else:
            await ctx.send('Server is not running!')

    # Runs the update bat file, updates server via SteamCMD
    @commands.command(name='update', help='Updates the server, must be off before running this')
    @commands.has_role(role)
    async def update(self, ctx):
        # Checks to make sure the server is not running before updating it
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            await ctx.send('Stop the server before running this (r!stop)')
            break
        else:
            os.startfile(steamcmd / "RoR2DSUpdate.bat")
            await ctx.send('Updating server, please wait...')
            updated = 1
            # Path of log file, removes before starting
            if os.path.exists(steamcmd / "logs/content_log.txt"):
                os.remove(steamcmd / "logs/content_log.txt")
                await asyncio.sleep(15)

            # After 15 seconds checks logs to see if server updated
            while updated == 1:
                with open(steamcmd / "logs/content_log.txt") as f:
                    for line in f:
                        if "AppID 1180760 scheduler finished" in line:
                            await ctx.send('Server updated...')
                            updated = 2
                            break

    # Restart the server with votes
    @commands.command(name='restart', help='Initializes a vote to restart the RoR2 server')
    async def restart(self, ctx, time=60):
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            global yes, no
            yes, no = 0, 0
            author = ctx.author
            message = await ctx.send('A restart vote has been initiated by {author.mention}, please react to this message!'.format(author=author))
            for emoji in ('✅', '❌'):
                await message.add_reaction(emoji)
            await asyncio.sleep(time)

            # Queries Steamworks to get total players
            with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as query:
                players = []
                for player in query.players()["players"]:
                    if player["name"]:
                        players.append(player)
                player_count = len(players)
                # Counts vote, if tie does nothing
                if(yes == no):
                    await ctx.send('It was a tie! There must be a majority to restart the server!')
                # If 75% of player count wants to restart it will
                elif((yes - 1) >= (player_count * 0.75)):
                    started = 1
                    for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
                        process.kill()
                        await asyncio.sleep(5)

                    # Path of log file, removes before starting
                    if os.path.exists(BepInEx / "LogOutput.log"):
                        os.remove(BepInEx / "LogOutput.log")

                    # Starts the server
                    os.startfile(ror2ds / "Risk of Rain 2.exe")
                    await ctx.send('Starting Risk of Rain 2 Server, please wait...')
                    await asyncio.sleep(15)

                    # After 15 seconds checks logs to see if server started
                    while started == 1:
                        with open(BepInEx / "LogOutput.log") as f:
                            for line in f:
                                if "Loaded scene lobby" in line:
                                    await ctx.send('Server started successfully...')
                                    started = 2
                                    break
                # All other options
                else:
                    await ctx.send('Restart vote failed!')
                break
        else:
            await ctx.send('Server is not running, unable to restart...')

    # Used for restart command
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global yes, no
        if payload.emoji.name == "✅":
            yes = yes + 1
        elif payload.emoji.name == "❌":
            no = no + 1
        else:
            pass

    # Displays the status of the Server
    @commands.command(name='status', help='Displays the status of current session')
    async def status(self, ctx):
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            # Create embed
            embed = discord.Embed(
                title='Server Information',
                colour=discord.Colour.blue()
            )

            # Use Steamworks API to query server
            with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
                info = server.info()
                ping = server.ping()
                players = []

                # Creates the string of player names used in the embed
                for player in server.players()["players"]:
                    if player["name"]:
                        players.append(player["name"])
                player_count = len(players)
                players = ('\n'.join(map(str, players)))

            # Embed information
            embed.set_footer(text='Steam query is not always accurate')
            embed.set_thumbnail(
                url='http://icons.iconarchive.com/icons/ampeross/smooth/512/Steam-icon.png')
            embed.set_author(name=self.bot.guilds[0])
            embed.add_field(name='Server Name',
                            value="{server_name}".format(**info), inline=False)
            embed.add_field(
                name='Player Count', value='{player_count}/{max_players}'.format(**info), inline=False)
            if player_count == 0:
                pass
            else:
                embed.add_field(name='Players', value=players, inline=False)
            embed.add_field(name='Server Ping',
                            value="{:n}".format(ping), inline=False)

            # Send embed
            await ctx.send(embed=embed)
            break
        else:
            await ctx.send('Server is currently offline.')

        # Output RoR server chat to Discord
        @commands.command(name='Start Live Chat', help='Displays live chat from the server to the specified channel in Discord')
        async def start_chat(self, ctx):
            await ctx.send('Displaying chat messages from the server!')
            global repeat
            repeat = 1
            if os.path.exists(BepInEx / "LogOutput.log.offset"):
                os.remove(BepInEx / "LogOutput.log.offset")
            while repeat == 1:
                await chat(self)
                await asyncio.sleep(1)

        # Stop outputting live server chat to Discord
        @commands.command(name='Stop Live Chat', help='Stops outputting live chat from the server')
        async def stop_chat(self, ctx):
            global repeat
            if repeat == 0:
                await ctx.send('Not outputting chat to Discord!')
            else:
                repeat = 0
                await ctx.send('Stopping outputting live chat to the server...')

    # Sends the Steam connection link
    # @commands.command(name='link', help='Get the Steam connection link')
    # async def link(self, ctx):
    #     await ctx.send('steam://connect/ror2.infernal.wtf:27015')

    # Print server configuration
    @commands.command(name='config', help='Prints the server configuration')
    @commands.has_role(role)
    async def config(self, ctx):
        await ctx.send('Coming soon!')


def setup(bot):
    bot.add_cog(RoR2(bot))
    print('Loaded cog: RoR2.py\n')
