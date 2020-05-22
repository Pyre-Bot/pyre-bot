#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 user functions."""
import asyncio
import logging

import discord
from discord.ext import commands

import libs.shared as shared
from config.config import *

# Global variables (yes, I know, not ideal but I'll fix them later)
yes, no = 0, 0


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
        if await shared.server():
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
            elif (yes - 1) >= (shared.server_info.player_count * 0.75):
                await ctx.send('Vote passed! Restarting the server, please wait...')
                if await shared.restart():
                    await ctx.send('Server restarted!')
                else:
                    await ctx.send('Unable to restart the server, please contact server admins. @Admin')
            else:
                logging.info('There were not enough votes to restart the server')
                await ctx.send('Restart vote failed!')
        else:
            await ctx.send('Server is not running, unable to restart...')

    # Kick a player with a majority vote
    # TODO: Add the ability to call this command with in-game chat
    @commands.command(
        name='votekick',
        help='Begins a vote to kick a player from the game',
        usage='playername'
    )
    async def votekick(self, ctx, *, kick_player):
        if await shared.server() and await shared.find_dll() is True:
            global yes, no
            yes, no = 0, 0
            author = ctx.author
            time = 30
            containskickplayer = 0
            for player in shared.server_players:
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
                elif (yes - 1) >= (shared.server_info.player_count * 0.75):
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
        elif await shared.server() is False:
            await ctx.send('Server is not running...')
        elif await shared.find_dll() is False:
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
        if await shared.server() and await shared.find_dll() is True:
            logging.info(f'{ctx.message.author.name} started an end run vote')
            if shared.server_info.map_name in ('lobby', 'title'):
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
                if (yes - 1) >= (shared.server_info.player_count * 0.75):
                    logging.info('Vote passed to end the current run')
                    append = open(botcmd / "botcmd.txt", 'a')
                    append.write('run_end' + '\n')
                    append.close()
                    await ctx.send('Run ended, all players have been returned to the lobby')
                # If vote fails
                else:
                    logging.info('End run vote failed')
                    await ctx.send('Vote failed. There must be a majority to end the run')
        elif await shared.server() is False:
            await ctx.send('Server is not running...')
        elif await shared.find_dll() is False:
            await ctx.send('BotCommands plugin is not loaded on the server!')

    # Displays the status of the server
    @commands.command(
        name='info',
        help='Displays Risk of Rain 2 server information'
    )
    async def status(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        if await shared.server():
            stage = '???'
            # Create embed
            embed = discord.Embed(
                title='Server Information',
                colour=discord.Colour.blue()
            )

            # Creates the string of player names used in the embed
            player_names = []
            for player in shared.server_players:
                player_names.append(player.name)
            player_names = ("\n".join(map(str, player_names)))

            # Convert Steam map name to game name
            for key, value in shared.stages.items():
                if key in shared.server_info.map_name:
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
                            value=f'{shared.server_info.server_name}', inline=False)
            embed.add_field(name='Current Stage', value=f'{stage}', inline=False)
            embed.add_field(
                name='Player Count',
                value=f'{shared.server_info.player_count}/{shared.server_info.max_players}', inline=False)
            if shared.server_info.player_count == 0:
                pass
            else:
                embed.add_field(
                    name='Players', value=player_names, inline=False)
            embed.add_field(name='Server Ping',
                            value=int(shared.server_info.ping * 1000), inline=False)

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
