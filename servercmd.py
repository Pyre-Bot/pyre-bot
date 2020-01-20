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

class RoR2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick a player with a majority vote
    # TODO: Add the ability to call this command with in-game chat by adding a conditional to the chat command, so players can do it while in-game too. Would have to add functionality for votes to count with in-game chat though. (or not, if I want to leave that to the discord).
    # TODO: Give a message if server is offline (this should be done globally)
    @commands.command(name='votekick', help='Begins a vote to kick a player from the game')
    async def votekick(self, ctx, kick_player='THEREISA32CHARACTERLIMITONSTEAMHAHA'):
        if(kick_player=='THEREISA32CHARACTERLIMITONSTEAMHAHA'):
            await ctx.send('Insert a partial or complete player name. Put quotations around the name if it contains spaces.')
        else:
            for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
                global yes, no # Keep this one or keep the other one?
                yes, no = 0, 0
                author = ctx.author # Would have to change this if I added the functionality to call from in-game. Would assign to player name, which I could get as easily as I do from regular chat operation
                time = 15 # Changed time to 15 seconds for tests
                server = subprocess.Popen(executable="Risk of Rain 2.exe")
                server.run(player_list)

                # Queries Steamworks to get total players
                with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as query:
                    players = []
                    containskickplayer = 0
                    for player in query.players()["players"]:
                        players.append(player)
                        if(kick_player.upper() in player["name"].upper()): # Need to make sure that it won't match to more than 1 user if there are common features in the name (theoretically it could match by one letter so)
                            containskickplayer = 1
                            kick_player = player["name"]
                    if(containskickplayer == 1):
                        message = await ctx.send('A vote to kick ' + kick_player + ' has been initiated by {author.mention}. Please react to this message with your vote!'.format(author=author))
                        for emoji in ('✅', '❌'):
                            await message.add_reaction(emoji)
                        player_count = len(players)
                        await asyncio.sleep(time)
                        # Counts vote, if tie does nothing
                        if(yes == no):
                            await ctx.send('It was a tie! There must be a majority to kick ' + kick_player)
                            break
                        # If 75% of player count wants to kick it will
                        #elif((yes - 1) >= (player_count * 0.75)): # Would this react properly with fractions? I.e. having there be 3 players, should require 2 players to vote.
                        elif((yes - 1) >= 1): # Changed to needing only one vote for tests, use commented-out code after testing is complete
                            await ctx.send('Kicked player ' + kick_player)
                        # If vote fails
                        else:
                            await ctx.send('Vote failed. There must be a majority to kick ' + kick_player)
                    else:
                        await ctx.send(kick_player + ' is not playing on the server')
                        #break

    # Used for restart and votekick commands. Could be risking interference if multiple votes were going on at once? Need to test. Could also add a condition where multiple votes can't be occurring at once.
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global yes, no # Keep this one or keep the other one?
        if payload.emoji.name == "✅":
            yes = yes + 1
        elif payload.emoji.name == "❌":
            no = no + 1
        else:
            pass

def setup(bot):
    bot.add_cog(RoR2(bot))
    print('Loaded cog: servercmd.py\n')
