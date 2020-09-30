#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 user functions."""
import asyncio
from datetime import datetime

import discord
from discord.ext import commands
from config.config import *

import libs.shared as shared
from libs.server import servers

# Global variables
yes, no = 0, 0


class RoR2(commands.Cog):
    """Handles all of the functions for the RoR2 cog.

    This cog handles user functions and features. Anything in here can be used without requiring special roles.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Counts the number of votes added to messages. Used solely for vote kick.

        Args:
            payload: The object containing the message reaction information.
        """
        global yes, no
        if payload.emoji.name == "✅":
            yes = yes + 1
        elif payload.emoji.name == "❌":
            no = no + 1
        else:
            pass

    @commands.command(
        name='restart',
        help='Initializes a vote to restart the RoR2 server',
        usage='time'
    )
    async def restart(self, ctx, time=15):
        """Used to start a vote to restart the game server.

        Args:
            ctx: Current Discord context.
            time: How long to let the vote run, by default 15 seconds.
        """
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            logging.info(
                f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
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
                logging.info(
                    f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] There were not enough votes to restart the server')
                await ctx.send('It was a tie! There must be a majority to restart the '
                               + 'server!')
            # If 75% of player count wants to restart it will
            elif (yes - 1) >= (serverinfo['server_info'].player_count * 0.75):
                await ctx.send('Vote passed! Restarting the server, please wait...')
                if await shared.restart(str(ctx.message.channel.id)):
                    await ctx.send('Server restarted!')
                    logging.info(
                        f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Restart vote passed.')
                else:
                    await ctx.send('Server could not be restarted')
                    logging.error(
                        f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Unable to restart the server')
            else:
                logging.info(
                    f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] There were not enough votes to restart the server')
                await ctx.send('Restart vote failed!')
        else:
            await ctx.send('Server is not running, unable to restart...')

    # TODO: Add the ability to call this command with in-game chat
    @commands.command(
        name='votekick',
        help='Begins a vote to kick a player from the game',
        usage='playername'
    )
    async def votekick(self, ctx, *, kick_player):
        """Player initiated function that creates a vote to remove a player from the game.

        Args:
            ctx: Current Discord context.
            kick_player: Full or partial steam name of the player.
        """
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            global yes, no
            yes, no = 0, 0
            author = ctx.author
            time = 30
            containskickplayer = 0
            for player in serverinfo['server_players']:
                if kick_player.upper() in player.name.upper():
                    containskickplayer = 1
                    kick_player = player.name
                    break
            if containskickplayer == 1:
                logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
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
                elif (yes - 1) >= (serverinfo['server_info'].player_count * 0.75):
                    logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {kick_player} was kicked from the game.')
                    await shared.execute_cmd(str(ctx.message.channel.id), "ban '" + kick_player + "'")
                    await ctx.send('Kicked player ' + kick_player)
                # If vote fails
                else:
                    logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Not enough votes to pass')
                    await ctx.send('Vote failed. There must be a majority to kick '
                                   + kick_player
                                   )
            else:
                await ctx.send(kick_player + ' is not playing on the server')
        else:
            await ctx.send('Server is not running...')

    @votekick.error
    async def votekick_handler(self, ctx, error):
        """Handles errors related to an incomplete player name with votekick.

        Args:
            ctx: Current Discord context.
            error: The error raised by the votekick command.
        """
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'kick_player':
                await ctx.send('Please insert a partial or complete player name')
                logging.warning(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Player name not specified')

    # TODO: Add the ability to call this command with in-game chat by adding a
    # conditional to the chat command, so players can do it while in-game too.
    # Would have to add functionality for votes to count with in-game chat
    # though. (or not, if I want to leave that to the discord).
    @commands.command(
        name='endrun',
        help='Begins a vote to end the current run',
    )
    async def endrun(self, ctx):
        """Begins a vote to end the run if enough players agree.

        Args:
            ctx: Current Discord context.
        """
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} started an end run vote')
            if serverinfo['server_info'].map_name in ('lobby', 'title', 'splash'):
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
                if (yes - 1) >= (serverinfo['server_info'].player_count * 0.75):
                    logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Vote passed to end the current run')
                    await shared.execute_cmd(str(ctx.message.channel.id), 'run_end')
                    await ctx.send('Run ended, all players have been returned to the lobby')
                # If vote fails
                else:
                    logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] End run vote failed')
                    await ctx.send('Vote failed. There must be a majority to end the run')
        else:
            await ctx.send('Server is not running...')

    @commands.command(
        name='info',
        help='Displays Risk of Rain 2 server information'
    )
    async def info(self, ctx):
        """Gathers the current server information and returns an embed message.

        Args:
            ctx: Current Discord context.
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')

        # Determines which object to use
        channel = str(ctx.message.channel.id)
        for key, value in servers.items():
            if channel == value.command_channel or channel == value.admin_channel:
                server = value
                break

        server_info = await server.info()
        if server_info:
            stage = '???'  # Handles stages not listed in the dictionary
            # Create embed
            embed = discord.Embed(
                title='Server Information',
                colour=discord.Colour.blue()
            )

            # Convert Steam map name to game name
            for key, value in shared.stages.items():
                if key in server_info['server_info'].map_name:
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
                            value=str(server.name), inline=False)
            embed.add_field(name='Current Stage', value=f'{stage}', inline=False)
            embed.add_field(
                name='Player Count',
                value=str(server.player_num) + '/' + str(server.max_players),
                inline=False)
            if server.player_num != 0:
                embed.add_field(
                    name='Players', value=server.players, inline=False)

            # Send embed
            await ctx.send(embed=embed)
        else:
            await ctx.send('Server is currently offline.')


def setup(bot):
    """Loads the cog into bot.py."""
    bot.add_cog(RoR2(bot))
    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Loaded cog: ror2.py')


def teardown(bot):
    """Prints to terminal when cog is unloaded."""
    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unloaded cog: ror2.py')
