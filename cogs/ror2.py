#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 user functions."""
import asyncio
import logging
import os

import a2s
import discord
import psutil
from discord.ext import commands

from config.config import *

# Global variables (yes, I know, not ideal but I'll fix them later)
yes, no = 0, 0

# These get assigned / updated every time server() is called
# Only using string type as a placeholder to avoid exceptions if the server is not online when the bot initializes
server_info = ''
server_players = ''

# Dictionaries used for functions
stages = {
    'title': 'Title',
    'lobby': 'Game Lobby',
    'blackbeach': 'Distant Roost',
    'blackbeach2': 'Distant Roost',
    'golemplains': 'Titanic Plains',
    'golemplains2': 'Titanic Plains',
    'foggyswamp': 'Wetland Aspect',
    'goolake': 'Abandoned Aqueduct',
    'frozenwall': 'Rallypoint Delta',
    'wispgraveyard': 'Scorched Acres',
    'dampcave': 'Abyssal Depths',
    'shipgraveyard': "Siren's Call",
    'arena': 'Hidden Realm: Void Fields',
    'bazaar': 'Hidden Realm: Bazaar Between Time',
    'goldshores': 'Hidden Realm: Glided Coast',
    'mysteryspace': 'Hidden Realm: A Moment, Fractured',
    'limbo': 'Hidden Realm: A Moment, Whole',
    'artifactworld': 'Hidden Realm: Artifact World',
    'skymeadow': 'Sky Meadow'
}


async def server():
    """
    Checks if the server is running or not.
    Returns:
        Boolean: Used by functions calling this to check if running
    """
    global server_info
    global server_players
    try:
        server_info = a2s.info(server_address, 1.0)
        server_players = a2s.players(server_address)
        return True
    except:
        #        print("Server error:", sys.exc_info()[0], sys.exc_info()[1]) #  Used for debugging
        return False


async def server_stop():
    """
    Stops the server.
    Returns:
        Boolean: Indicates whether server stopped or not
    """
    for proc in psutil.process_iter():
        exe = Path.cwd().joinpath(ror2ds, 'Risk of Rain 2.exe')
        try:
            processExe = proc.exe()
            if str(exe) == processExe:
                proc.kill()
                logging.info('Server stopped')
                return True
        except:
            pass
    return False


async def find_dll():
    """
    Checks to see if the BotCommands plugin is installed on server.
    Returns:
        Boolean: If true it is, otherwise it is not
    """
    plugin_dir = (bepinex / 'plugins')
    files = [file.name for file in plugin_dir.glob('**/*') if file.is_file()]
    if 'BotCommands.dll' in files:
        return True
    logging.warning('Unable to find BotCommands.dll!')
    return False


class RoR2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Counts reactions of commands with votes
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global yes, no
        if payload.emoji.name == "✅":
            yes = yes + 1
        elif payload.emoji.name == "❌":
            no = no + 1
        else:
            pass

    # Restart the server with votes
    @commands.command(
        name='restart',
        help='Initializes a vote to restart the RoR2 server',
        usage='time'
    )
    async def restart(self, ctx, time=15):
        if await server():
            logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
            global yes, no
            yes, no = 0, 0
            author = ctx.author
            message = await ctx.send('A restart vote has been initiated by '
                                     + f'{author.mention}. Please react to this message'
                                     + ' with your vote!')
            for emoji in ('✅', '❌'):
                await message.add_reaction(emoji)
            await asyncio.sleep(time)
            # Counts vote, if tie does nothing
            if yes == no:
                logging.info('There were not enoough votes to restart the server')
                await ctx.send('It was a tie! There must be a majority to restart the '
                               + 'server!')
            # If 75% of player count wants to restart it will
            elif (yes - 1) >= (server_info.player_count * 0.75):
                started = 1
                stopped = await server_stop()
                if stopped is True:
                    await ctx.send('Risk of Rain 2 server shut down...')
                elif stopped is False:
                    await ctx.send('Unable to stop server!')
                await asyncio.sleep(5)

                # Path of log file, removes before starting
                if os.path.exists(bepinex / "LogOutput.log"):
                    try:
                        os.remove(bepinex / "LogOutput.log")
                    except Exception:
                        print('Unable to remove log file')

                # Starts the server
                os.startfile(ror2ds / "Risk of Rain 2.exe")
                await ctx.send('Starting Risk of Rain 2 Server, please wait...')
                await asyncio.sleep(15)

                # After 15 seconds checks logs to see if server started
                while started == 1:
                    with open(bepinex / "LogOutput.log") as f:
                        for line in f:
                            if "Loaded scene lobby" in line:
                                await ctx.send('Server started successfully...')
                                started = 2
                                break
                # All other options
            else:
                logging.info('There were not enough votes to restart the server')
                await ctx.send('Restart vote failed!')
        else:
            await ctx.send('Server is not running, unable to restart...')

    # Kick a player with a majority vote
    # TODO: Add the ability to call this command with in-game chat by adding a
    # conditional to the chat command, so players can do it while in-game too.
    # Would have to add functionality for votes to count with in-game chat
    # though. (or not, if I want to leave that to the discord).
    @commands.command(
        name='votekick',
        help='Begins a vote to kick a player from the game',
        usage='playername'
    )
    async def votekick(self, ctx, *, kick_player):
        if await server() and await find_dll() is True:
            global yes, no
            yes, no = 0, 0
            author = ctx.author
            time = 30
            containskickplayer = 0
            for player in server_players:
                if kick_player.upper() in player.name.upper():
                    containskickplayer = 1
                    kick_player = player.name
                    break
            if containskickplayer == 1:
                logging.info(
                    f'{ctx.message.author.name} started a vote to kick {kick_player}')
                message = await ctx.send('A vote to kick ' + kick_player
                                         + f' has been initiated by {author.mention}. '
                                         + 'Please react to this message with your '
                                         + 'vote!')
                for emoji in ('✅', '❌'):
                    await message.add_reaction(emoji)
                await asyncio.sleep(time)
                # Counts vote, if tie does nothing
                if yes == no:
                    await ctx.send(
                        'It was a tie! There must be a majority to kick '
                        + kick_player
                    )
                # If 75% of player count wants to kick it will
                elif (yes - 1) >= (server_info.player_count * 0.75):
                    logging.info(f'{kick_player} was kicked from the game.')
                    append = open(botcmd / "botcmd.txt", 'a')
                    append.write('ban "' + kick_player + '"\n')
                    append.close()
                    await ctx.send('Kicked player ' + kick_player)
                # If vote fails
                else:
                    logging.info('Not enough votes to pass')
                    await ctx.send('Vote failed. There must be a majority to kick '
                                   + kick_player
                                   )
            else:
                await ctx.send(kick_player + ' is not playing on the server')
        elif await server() is False:
            await ctx.send('Server is not running...')
        elif await find_dll() is False:
            await ctx.send('BotCommands plugin is not loaded on the server!')

    @votekick.error
    async def votekick_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'kick_player':
                await ctx.send('Please insert a partial or complete player name')

    # Ends the run with a majority vote
    # TODO: Add the ability to call this command with in-game chat by adding a
    # conditional to the chat command, so players can do it while in-game too.
    # Would have to add functionality for votes to count with in-game chat
    # though. (or not, if I want to leave that to the discord).
    @commands.command(
        name='endrun',
        help='Begins a vote to end the current run',
    )
    async def endrun(self, ctx):
        if await server() and await find_dll() is True:
            logging.info(f'{ctx.message.author.name} started an end run vote')
            global server_info
            if server_info.map_name in ('lobby', 'title'):
                await ctx.send('No run in progress.')
            else:
                global yes, no
                yes, no = 0, 0
                author = ctx.author
                time = 30
                message = await ctx.send('A vote to end the run has been initiated by '
                                         + f'{author.mention}. Please react to this message'
                                         + ' with your vote!')
                for emoji in ('✅', '❌'):
                    await message.add_reaction(emoji)
                await asyncio.sleep(time)
                # If 75% of player count wants to end the run it will
                if (yes - 1) >= (server_info.player_count * 0.75):
                    logging.info('Vote passed to end the current run')
                    append = open(botcmd / "botcmd.txt", 'a')
                    append.write('run_end' + '\n')
                    append.close()
                    await ctx.send('Run ended, all players have been returned to the lobby')
                # If vote fails
                else:
                    logging.info('End run vote failed')
                    await ctx.send('Vote failed. There must be a majority to end the run')
        elif await server() is False:
            await ctx.send('Server is not running...')
        elif await find_dll() is False:
            await ctx.send('BotCommands plugin is not loaded on the server!')

    # Displays the status of the server
    @commands.command(
        name='info',
        help='Displays Risk of Rain 2 server information'
    )
    async def status(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        if await server():
            stage = '???'
            # Create embed
            embed = discord.Embed(
                title='Server Information',
                colour=discord.Colour.blue()
            )

            # Creates the string of player names used in the embed
            player_names = []
            for player in server_players:
                player_names.append(player.name)
            player_names = ("\n".join(map(str, player_names)))

            # Convert Steam map name to game name
            for key, value in stages.items():
                if key in server_info.map_name:
                    stage = value
                    break

            # Embed information
            embed.set_footer(
                text=f'Requested by {ctx.message.author.name}',
                icon_url=self.bot.user.avatar_url
            )
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_author(name=self.bot.guilds[0])
            embed.add_field(name='Server Name',
                            value=f'{server_info.server_name}', inline=False)
            embed.add_field(name='Current Stage', value=f'{stage}', inline=False)
            embed.add_field(
                name='Player Count',
                value=f'{server_info.player_count}/{server_info.max_players}', inline=False)
            if server_info.player_count == 0:
                pass
            else:
                embed.add_field(
                    name='Players', value=player_names, inline=False)
            embed.add_field(name='Server Ping',
                            value=int(server_info.ping * 1000), inline=False)

            # Send embed
            await ctx.send(embed=embed)
        else:
            await ctx.send('Server is currently offline.')

    # Send modlist to chat
    @commands.command(
        name='mods',
        help='Lists all the mods currently running on the server'
    )
    async def mods(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        mods = []
        with open(bepinex / "LogOutput.log") as f:
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
        mod_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=self.bot.user.avatar_url
        )
        mod_embed.add_field(name='Mods', value=mods, inline=False)
        await ctx.send(embed=mod_embed)


def setup(bot):
    """Loads the cog into bot.py."""
    bot.add_cog(RoR2(bot))
    print('Loaded cog: ror2.py')


def teardown(bot):
    """Prints to terminal when cog is unloaded."""
    print('Unloaded cog: ror2.py')
