#!/usr/bin/env python3

"""Functions that are primarily used by Discord members for Risk of Rain 2."""

import asyncio
import logging

import discord
from discord.ext import commands

import pyre.libs.shared as shared

# Global variables (yes, I know, not ideal but I'll fix them later)
yes, no = 0, 0


class RoR2(commands.Cog):
    """Member-specific Risk of Rain 2 Discord commands and functions.

    Parameters
    ----------
    commands.Cog : Cog
        The base cog class used for all discord.py cogs.

    Methods
    -------
    restart(ctx, time=15)
        Creates a restart vote for the server.
    votekick(ctx, kick_player)
        Creates a vote to kick a player from the server.
    endrun(ctx)
        Creates a vote to end the current run.
    status(ctx)
        Returns the current server information.

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
        """Creates a restart vote.

        Parameters
        ----------
        ctx : Any
            Current Discord context
        time : int
            Number of seconds to let the vote run
        """
        serverinfo = await shared.server(ctx.message.channel.id)
        if serverinfo:
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
                logging.info('There were not enough votes to restart the server')
                await ctx.send('It was a tie! There must be a majority to restart the '
                               + 'server!')
            # If 75% of player count wants to restart it will
            elif (yes - 1) >= (serverinfo['server_info'].player_count * 0.75):
                await ctx.send('Vote passed! Restarting the server, please wait...')
                if await shared.restart(ctx.message.channel.id):
                    await ctx.send('Server restarted!')
                else:
                    await ctx.send('Server could not be restarted')
            else:
                logging.info('There were not enough votes to restart the server')
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
        """Creates a votekick.

        Parameters
        ----------
        ctx : Any
            Current Discord context
        kick_player : str
            Full or partial name of the player

        See Also
        --------
        votekick_handler : Error handling for this method
        """
        serverinfo = await shared.server(ctx.message.channel.id)
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
                elif (yes - 1) >= (serverinfo['server_info'].player_count * 0.75):
                    logging.info(f'{kick_player} was kicked from the game.')
                    await shared.execute_cmd(ctx.message.channel.id, "ban '" + kick_player + "'")
                    await ctx.send('Kicked player ' + kick_player)
                # If vote fails
                else:
                    logging.info('Not enough votes to pass')
                    await ctx.send('Vote failed. There must be a majority to kick '
                                   + kick_player
                                   )
            else:
                await ctx.send(kick_player + ' is not playing on the server')
        else:
            await ctx.send('Server is not running...')

    @votekick.error
    async def votekick_handler(self, ctx, error):
        """Handles errors related to a missing player name for `votekick`.

        Parameters
        ----------
        ctx : Any
            Current Discord context
        error : Any
            Error object raised by `votekick`
        """
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'kick_player':
                await ctx.send('Please insert a partial or complete player name')

    # TODO: Add the ability to call this command with in-game chat
    @commands.command(
        name='endrun',
        help='Begins a vote to end the current run',
    )
    async def endrun(self, ctx):
        """Creates a vote to end the current run.

        Parameters
        ----------
        ctx : Any
            Current Discord object
        """
        serverinfo = await shared.server(ctx.message.channel.id)
        if serverinfo:
            logging.info(f'{ctx.message.author.name} started an end run vote')
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
                    logging.info('Vote passed to end the current run')
                    await shared.execute_cmd(ctx.message.channel.id, 'run_end')
                    await ctx.send('Run ended, all players have been returned to the lobby')
                # If vote fails
                else:
                    logging.info('End run vote failed')
                    await ctx.send('Vote failed. There must be a majority to end the run')
        else:
            await ctx.send('Server is not running...')

    @commands.command(
        name='info',
        help='Displays Risk of Rain 2 server information'
    )
    async def status(self, ctx):
        """Queries Steam for the current information about the server.

        Parameters
        ----------
        ctx : Any
            Current Discord context.
        """
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(ctx.message.channel.id)
        if serverinfo:
            stage = '???'  # Sets a standard stage name to be used if the stage name is no recognized.
            # Create embed
            embed = discord.Embed(
                title='Server Information',
                colour=discord.Colour.blue()
            )

            # Creates the string of player names used in the embed
            player_names = []
            for player in serverinfo['server_players']:
                player_names.append(player.name)
            player_names = ("\n".join(map(str, player_names)))

            # Convert Steam map name to game name
            for key, value in shared.stages.items():
                if key in serverinfo['server_info'].map_name:
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
                            value=str(serverinfo['server_info'].server_name), inline=False)
            embed.add_field(name='Current Stage', value=f'{stage}', inline=False)
            embed.add_field(
                name='Player Count',
                value=str(serverinfo['server_info'].player_count)+'/'+str(serverinfo['server_info'].max_players), inline=False)
            if serverinfo['server_info'].player_count == 0:
                pass
            else:
                embed.add_field(
                    name='Players', value=player_names, inline=False)
            embed.add_field(name='Server Ping',
                            value=int(serverinfo['server_info'].ping * 1000), inline=False)

            # Send embed
            await ctx.send(embed=embed)
        else:
            await ctx.send('Server is currently offline.')


def setup(bot):
    """Loads the cog into the bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        Discord bot object
    """
    bot.add_cog(RoR2(bot))
    logging.info('Loaded cog: ror2.py')


def teardown(bot):
    """Removes the cog from the bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        Discord bot object
    """
    logging.info('Unloaded cog: ror2.py')
