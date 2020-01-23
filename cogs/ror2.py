import os
import psutil
import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from configparser import ConfigParser
import re
from pygtail import Pygtail
import ast
import a2s

config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]

# Config variables
server_address = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')
steamcmd = Path(ror2["steamcmd"])
ror2ds = Path(ror2["ror2ds"])
BepInEx = Path(ror2["BepInEx"])
role = ror2["role"]
chat_autostart = ror2["auto-start-chat"]
hidden_mods = ast.literal_eval(config_object.get('RoR2', 'hidden_mods'))

# Global variables (yes, I know, not ideal but I'll fix them later)
yes, no = 0, 0
repeat = 0
stagenum = 0


# Function of chat
async def chat(self):
    """Reads the BepInEx output log to send chat to Discord."""
    file = (BepInEx / "LogOutput.log")
    channel = config_object.getint('RoR2', 'channel')
    channel = self.bot.get_channel(channel)
    global stagenum
    if os.path.exists(file):
        if os.path.exists(BepInEx / "LogOutput.log.offset"):
            for line in Pygtail(str(file)):
                # Player chat
                if "issued: say" in line:
                    line = line.replace('[Info   : Unity Log] ', '**')
                    line = re.sub(r" ?\([^)]+\)", "", line)
                    line = line.replace(' issued:', ':** ')
                    line = line.replace(' say ', '')
                    await channel.send(line)
                # Stage change
                elif "Active scene changed from" in line:
                    if "bazaar" in line:
                        stagenum = stagenum
                    elif "lobby" in line:
                        stagenum = 0
                    else:
                        stagenum = stagenum + 1
                    line = line.replace(
                        '[Info   : Unity Log] Active scene changed from  to ', '**ENTERING STAGE ' + str(stagenum) + ' - ')
                    await channel.send(line + '**')
                # Player joins
                elif "[Info   :     R2DSE] New player : " in line:
                    line = line.replace(
                        '[Info   :     R2DSE] New player : ', '**PLAYER JOINED - ')
                    line = line.replace(' connected. ', '')
                    line = re.sub(r" ?\([^)]+\)", "", line)
                    await channel.send(line + '**')
                # Player leaves
                elif "[Info   :     R2DSE] Ending AuthSession with : " in line:
                    line = line.replace(
                        '[Info   :     R2DSE] Ending AuthSession with : ', '**PLAYER LEFT - ')
                    line = re.sub(r" ?\([^)]+\)", "", line)
                    await channel.send(line + '**')
        else:
            for line in Pygtail(str(file)):
                pass


async def server():
    """
    Checks if the server is running or not.

    Returns:
        string: Used by functions calling this to check if running
    """
    if "Risk of Rain 2.exe" in (p.name() for p in psutil.process_iter()):
        return('true')
    else:
        return('false')


async def server_stop():
    """
    Stops the server.

    Returns:
        string: Indicates whether server stopped or not
    """
    for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
        process.kill()
        return('true')
    else:
        return('false')


class RoR2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if chat_autostart == 'true':
            global repeat
            repeat = 1
            if os.path.exists(BepInEx / "LogOutput.log.offset"):
                try:
                    os.remove(BepInEx / "LogOutput.log.offset")
                except Exception:
                    print('Unable to remove offset! Old messages may be displayed.')
            while repeat == 1:
                await chat(self)
                await asyncio.sleep(1)

    # Start the RoR2 server
    @commands.command(name='start', help='Starts the server if it is not running')
    @commands.has_role(role)
    async def start(self, ctx):
        # Checks to make sure the server is not running before starting it
        running = await server()
        if running == 'false':
            started = 1
            # Path of log file, removes before starting
            if os.path.exists(BepInEx / "LogOutput.log"):
                try:
                    os.remove(BepInEx / "LogOutput.log")
                except Exception:
                    print('Unable to remove log file')

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
        elif running == 'true':
            await ctx.send('Server is already running!')
    # Exits the server
    @commands.command(name='stop', help='Stops the server if currently running')
    @commands.has_role(role)
    async def stop(self, ctx):
        running = await server()
        if running == 'true':
            stopped = await server_stop()
            if stopped == 'true':
                await ctx.send('Risk of Rain 2 server shut down...')
            elif stopped == 'false':
                await ctx.send('Unable to stop server!')
        else:
            await ctx.send('Server is not running!')

    # Runs the update bat file, updates server via SteamCMD
    @commands.command(name='update', help='Updates the server, must be off before running this')
    @commands.has_role(role)
    async def update(self, ctx):
        # Checks to make sure the server is not running before updating it
        running = await server()
        if running == 'false':
            await ctx.send('Updating server, please wait...')
            updated = 1
            # Path of log file, removes before starting
            if os.path.exists(steamcmd / "logs/content_log.txt"):
                try:
                    os.remove(steamcmd / "logs/content_log.txt")
                except Exception:
                    print('Unable to remove log file')
                await asyncio.sleep(2)
            os.startfile(steamcmd / "RoR2DSUpdate.bat")
            await asyncio.sleep(15)

            # After 15 seconds checks logs to see if server updated
            while updated == 1:
                with open(steamcmd / "logs/content_log.txt") as f:
                    for line in f:
                        if "AppID 1180760 scheduler finished" in line:
                            await ctx.send('Server updated...')
                            updated = 2
                            break
        elif running == 'true':
            await ctx.send('You must stop the server prior to updating!')

    # Restart the server with votes
    @commands.command(name='restart', help='Initializes a vote to restart the RoR2 server')
    async def restart(self, ctx, time=60):
        running = await server()
        if running == 'true':
            global yes, no
            yes, no = 0, 0
            author = ctx.author
            message = await ctx.send('A restart vote has been initiated by {author.mention}, please react to this message!'.format(author=author))
            for emoji in ('✅', '❌'):
                await message.add_reaction(emoji)
            await asyncio.sleep(time)

            # Queries Steamworks to get total players
            info = a2s.info(server_address)
            player_count = info.player_count
            # Counts vote, if tie does nothing
            if yes == no:
                await ctx.send('It was a tie! There must be a majority to restart the server!')
            # If 75% of player count wants to restart it will
            elif (yes - 1) >= (player_count * 0.75):
                started = 1
                stopped = await server_stop()
                if stopped == 'true':
                    await ctx.send('Risk of Rain 2 server shut down...')
                elif stopped == 'false':
                    await ctx.send('Unable to stop server!')
                await asyncio.sleep(5)

                # Path of log file, removes before starting
                if os.path.exists(BepInEx / "LogOutput.log"):
                    try:
                        os.remove(BepInEx / "LogOutput.log")
                    except Exception:
                        print('Unable to remove log file')

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
        else:
            await ctx.send('Server is not running, unable to restart...')

    # Kick a player with a majority vote
    # TODO: Add the ability to call this command with in-game chat by adding a
    # conditional to the chat command, so players can do it while in-game too.
    # Would have to add functionality for votes to count with in-game chat
    # though. (or not, if I want to leave that to the discord).
    @commands.command(name='votekick', help='Begins a vote to kick a player from the game')
    async def votekick(self, ctx, kick_player='THEREISA32CHARACTERLIMITONSTEAMHAHA'):
        running = await server()
        if running == 'true':
            if(kick_player == 'THEREISA32CHARACTERLIMITONSTEAMHAHA'):
                await ctx.send('Insert a partial or complete player name. Put quotations around the name if it contains spaces.')
            else:
                global yes, no
                yes, no = 0, 0
                author = ctx.author
                time = 30

                players = a2s.players(server_address)
                info = a2s.info(server_address)
                player_names = []
                containskickplayer = 0
                for player in players:
                    player_names.append(player.name)
                    if(kick_player.upper() in player.name.upper()):
                        containskickplayer = 1
                        kick_player = player.name
                if(containskickplayer == 1):
                    message = await ctx.send('A vote to kick ' + kick_player + ' has been initiated by {author.mention}. Please react to this message with your vote!'.format(author=author))
                    for emoji in ('✅', '❌'):
                        await message.add_reaction(emoji)
                    player_count = info.player_count
                    await asyncio.sleep(time)
                    # Counts vote, if tie does nothing
                    if(yes == no):
                        await ctx.send('It was a tie! There must be a majority to kick ' + kick_player)
                    # If 75% of player count wants to kick it will
                    elif((yes - 1) >= (player_count * 0.75)):
                        append = open(BepInEx / "plugins/botcmd.txt", 'a')
                        append.write('kick "' + kick_player + '"\n')
                        append.close()
                        await ctx.send('Kicked player ' + kick_player)
                    # If vote fails
                    else:
                        await ctx.send('Vote failed. There must be a majority to kick ' + kick_player)
                else:
                    await ctx.send(kick_player + ' is not playing on the server')
        elif running == 'false':
            await ctx.send('Server is not running...')

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
        running = await server()
        if running == 'true':
            # Create embed
            embed = discord.Embed(
                title='Server Information',
                colour=discord.Colour.blue()
            )

            # Use Steamworks API to query server
            info = a2s.info(server_address)
            players = a2s.players(server_address)

            # Creates the string of player names used in the embed
            player_names = []
            for player in players:
                player_names.append(player.name)
            player_names = ("\n".join(map(str, player_names)))

            # Embed information
            embed.set_footer(text='Steam query is not always accurate')
            embed.set_thumbnail(
                url='http://icons.iconarchive.com/icons/ampeross/smooth/512/Steam-icon.png')
            embed.set_author(name=self.bot.guilds[0])
            embed.add_field(name='Server Name',
                            value="{}".format(info.server_name), inline=False)
            embed.add_field(
                name='Player Count', value='{}/{}'.format(info.player_count, info.max_players), inline=False)
            if info.player_count == 0:
                pass
            else:
                embed.add_field(
                    name='Players', value=player_names, inline=False)
            embed.add_field(name='Server Ping',
                            value=int(info.ping * 100), inline=False)

            # Send embed
            await ctx.send(embed=embed)
        elif running == 'false':
            await ctx.send('Server is currently offline.')

    # Send modlist to chat
    @commands.command(name='mods', help='Lists all the mods currently running on the server')
    async def mods(self, ctx):
        mods = []
        with open(BepInEx / "LogOutput.log") as f:
            for line in f:
                if "[Info   :   BepInEx] Loading" in line:
                    line = line[30:]
                    head, sep, tail = line.partition(' ')
                    if head in hidden_mods:
                        pass
                    else:
                        mods.append(head)
        mods = ("\n".join(map(str, mods)))
        mod_embed = discord.Embed(colour=discord.Colour.blue())
        mod_embed.add_field(name='Mods', value=mods, inline=False)
        await ctx.send(embed=mod_embed)

    # Output RoR server chat to Discord
    @commands.command(name='start_chat', help='Displays live chat from the server to the specified channel in Discord')
    @commands.has_role(role)
    async def start_chat(self, ctx):
        await ctx.send('Displaying chat messages from the server!')
        global repeat
        repeat = 1
        if os.path.exists(BepInEx / "LogOutput.log.offset"):
            try:
                os.remove(BepInEx / "LogOutput.log.offset")
            except Exception:
                print('Unable to remove offset! Old messages may be displayed.')
        while repeat == 1:
            await chat(self)
            await asyncio.sleep(1)

    # Stop outputting live server chat to Discord
    @commands.command(name='stop_chat', help='Stops outputting live chat from the server')
    @commands.has_role(role)
    async def stop_chat(self, ctx):
        global repeat
        if repeat == 0:
            await ctx.send('Not outputting chat to Discord!')
        else:
            repeat = 0
            await ctx.send('Stopping outputting live chat to the server...')

    # Print server configuration
    @commands.command(name='config', help='Prints the server configuration')
    @commands.has_role(role)
    async def config(self, ctx):
        await ctx.send('Coming soon!')


def setup(bot):
    """Loads the cog into bot.py."""
    bot.add_cog(RoR2(bot))
    print('Loaded cog: RoR2.py\n')


def teardown(bot):
    """Prints to termianl when cog is unloaded."""
    print('Unloaded cog: RoR2.py')
