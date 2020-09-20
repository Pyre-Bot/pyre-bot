#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 admin functions."""

import logging
import random
from datetime import datetime

import discord
from discord.ext import commands

import libs.shared as shared
from config.config import *

# Globals
yes, no = 0, 0
stagenum = 0
run_timer = 0


class Ror2_admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='start', help='Starts the server if it is not running')
    @commands.check(shared.is_host)
    async def start(self, ctx):
        """Issues a host command to the server.

        :param ctx: Discord context
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        # Checks to make sure the server is not running before starting it
        if await shared.server(str(ctx.message.channel.id)) is False:
            await ctx.send('Starting Risk of Rain 2 server, please wait')
            if await shared.start(str(ctx.message.channel.id)):
                await ctx.send('Risk of Rain 2 server started!')
            else:
                await ctx.send('Unable to start server! Please check logs for error.')
                logging.error(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Failed to start the server')
        else:
            await ctx.send('Server is already running!')

    @commands.command(name='stop', help='Stops the server if currently running')
    @commands.check(shared.is_host)
    async def stop(self, ctx):
        """Issues a disconnect command to the server.

        :param ctx: Discord context
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        if await shared.server(str(ctx.message.channel.id)):
            if await shared.server_stop(str(ctx.message.channel.id)):
                await ctx.send('Risk of Rain 2 server shut down...')
            else:
                await ctx.send('Unable to stop server!')
                logging.error("[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Failed to stop the server")
        else:
            await ctx.send('Server is not running!')

    @commands.command(
        name='say',
        help='Sends a message from the server',
        usage='message',
        aliases=['s']
    )
    @commands.check(shared.is_host)
    async def serversay(self, ctx, *, message):
        """Sends a chat message to the server

        :param ctx: Discord context
        :param message: Message to send to the server
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        if await shared.server(str(ctx.message.channel.id)):
            await shared.execute_cmd(str(ctx.message.channel.id), "say '" + message + "'")
        else:
            await ctx.send('Server is not running...')

    @commands.command(
        name='cmd',
        help='Passes on a command to be interpreted directly by the console',
        usage='command'
    )
    @commands.check(shared.is_host)
    async def customcmd(self, ctx, *, cmd_with_args):
        """Issues a custom command to the server.

        :param ctx: Discord context
        :param cmd_with_args: Command to be sent to the server
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            await shared.execute_cmd(str(ctx.message.channel.id), cmd_with_args)
            """ Commented out for now, will get to later
            findline = True
            consoleout = ''
            tempreader = Pygtail(str(logfile), read_from_end=True)
            while findline:
                for line in tempreader:
                    if 'Server(0) issued' in line:
                        continue
                    elif 'is not a recognized ConCommand or ConVar.' in line:
                        await ctx.send(cmd_with_args + ' is not a valid command')
                        findline = False
                        break
                    elif '[Info   : Unity Log]' in line:  # There's an \n in every line
                        consoleout = str(line.replace('[Info   : Unity Log] ', ''))
                        findline = False
                        continue
                    elif '[Error  : Unity Log]' in line:  # There's an \n in every line
                        consoleout = str(line.replace(
                            '[Error  : Unity Log] ', 'Error - '))
                        findline = False
                        continue
                    elif str(line) != '\n':
                        consoleout += str(line)
                        findline = False
                        continue
                    else:
                        findline = False
                        continue
            await ctx.send('**Server: **' + consoleout)
            """
        else:
            await ctx.send('Server is not running...')

    @commands.command(
        name='giveitem',
        help='Gives a player a specified quantity of an item',
        usage='playername itemname qty'
    )
    @commands.check(shared.is_host)
    async def giveitem(self, ctx, playername, itemname, qty="1"):
        """Issues a command on the server to get the player specified equipment.

        :param ctx: Discord context
        :param playername: Full or partial player name
        :param itemname: Full or partial item name
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            if serverinfo['server_info'].map_name in ('lobby', 'title', 'splash'):
                await ctx.send('No run in progress')
            else:
                containsplayer = False
                for player in serverinfo['server_players']:
                    if playername.upper() in player.name.upper():
                        playername = player.name
                        containsplayer = True
                        break
                if containsplayer is True:
                    await shared.execute_cmd(str(ctx.message.channel.id), "give_item '" + itemname + "' "
                                             + qty + " '" + playername + "'")
                    """ Commented out for now
                    findline = True
                    tempreader = Pygtail(str(logfile), read_from_end=True)
                    while findline:
                        for line in tempreader:
                            if ('[Info   : Unity Log] The requested object could not be '
                                    + 'found' in line):
                                await ctx.send(itemname + ' is not a valid item name')
                                findline = False
                                break
                            elif "[Info   : Unity Log] Gave" in line:
                                if "None" in line:
                                    pass
                                else:
                                    for key, value in shared.item.items():
                                        if key in line:
                                            itemname = value
                                            break
                                    await ctx.send('Gave ' + qty + ' ' + itemname + ' to '
                                                   + playername)
                                    findline = False
                                    break
                    """
                else:
                    await ctx.send(playername + ' is not playing on the server')
        else:
            await ctx.send('Server is not running...')

    @giveitem.error
    async def giveitem_handler(self, ctx, error):
        """Handles errors related to the giveitem command.

        :param ctx: Discord context
        :param error: Error raised by the command
        """
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'playername':
                logging.warning(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
                                f'{ctx.message.author.name} caused an error with '
                                + f'{ctx.command.name} | Message: {ctx.message.content} | '
                                + f'Error: {error}')
                await ctx.send('Please enter a partial or complete player name')
            if error.param.name == 'itemname':
                logging.warning(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
                                f'{ctx.message.author.name} caused an error with '
                                + f'{ctx.command.name} | Message: {ctx.message.content} | '
                                + f'Error: {error}')
                await ctx.send('Please enter a valid item name')

    @commands.command(
        name='giveequip',
        help='Gives a player a specified equipment',
        usage='playername equipname'
    )
    @commands.check(shared.is_host)
    async def giveequip(self, ctx, playername, equipname):
        """Issues a command on the server to get the player specified equipment.

        :param ctx: Discord context
        :param playername: Full or partial player name
        :param equipname: Full or partial equipment name
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            if serverinfo['server_info'].map_name in ('lobby', 'title', 'splash'):
                await ctx.send('No run in progress')
            else:
                containsplayer = False
                for player in serverinfo['server_players']:
                    if playername.upper() in player.name.upper():
                        playername = player.name
                        containsplayer = True
                        break
                if containsplayer is True:
                    await shared.execute_cmd(str(ctx.message.channel.id), "give_equip '" + equipname + "' '"
                                             + playername + "'")
                    """ Will come back to it
                    findline = True
                    tempreader = Pygtail(str(logfile), read_from_end=True)
                    while findline:
                        for line in tempreader:
                            if ('[Info   : Unity Log] The requested object could not be '
                                    + 'found' in line):
                                await ctx.send(equipname + ' is not a valid equipment name')
                                findline = False
                                break
                            elif "[Info   : Unity Log] Gave" in line:
                                if "None" in line:
                                    pass
                                else:
                                    for key, value in shared.equip.items():
                                        if key in line:
                                            equipname = value
                                            break
                                    await ctx.send('Gave ' + equipname + ' to '
                                                   + playername)
                                    findline = False
                                    break
                    """
                else:
                    await ctx.send(playername + ' is not playing on the server')
        else:
            await ctx.send('Server is not running...')

    @giveequip.error
    async def giveequip_handler(self, ctx, error):
        """Handles errors related to the giveequip command.

        :param ctx: Discord context
        :param error: Error raised by the command
        """
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'playername':
                logging.warning(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
                                f'{ctx.message.author.name} caused an error with '
                                + f'{ctx.command.name} | Message: {ctx.message.content} | '
                                + f'Error: {error}')
                await ctx.send('Please enter a partial or complete player name')
            if error.param.name == 'equipname':
                logging.warning(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
                                f'{ctx.message.author.name} caused an error with '
                                + f'{ctx.command.name} | Message: {ctx.message.content} | '
                                + f'Error: {error}')
                await ctx.send('Please enter a valid equipment name')

    # noinspection DuplicatedCode
    @commands.command(name='help_admin', help='Displays this message', usage='cog')
    @commands.check(shared.is_host)
    async def help_admin(self, ctx, cog='ror2_admin'):
        """Displays the help options including admin commands.

        :param ctx: Discord context
        :param cog: (Optional) Cog name for more in depth information.
        :return: Returns if invalid cog name is specified
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        color_list = [c for c in shared.colors.values()]
        help_embed = discord.Embed(
            title='Help',
            color=random.choice(color_list)
        )
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=self.bot.user.avatar_url
        )
        cogs = [c for c in self.bot.cogs.keys()]
        if cog == 'all':
            for cog in cogs:
                cog_commands = self.bot.get_cog(cog).get_commands()
                commands_list = ''
                for comm in cog_commands:
                    commands_list += f'**{comm.name}** - *{comm.help}*\n'
                help_embed.add_field(
                    name=cog,
                    value=commands_list,
                    inline=False
                )
        else:
            lower_cogs = [c.lower() for c in cogs]
            if cog.lower() in lower_cogs:
                commands_list = self.bot.get_cog(
                    cogs[lower_cogs.index(cog.lower())]).get_commands()
                help_text = ''
                for command in commands_list:
                    help_text += f'```{command.name}```\n' \
                                 f'**{command.help}**\n\n'
                    if command.usage is not None:
                        help_text += f'Format: `{command.name} {command.usage}`\n\n'
                help_embed.description = help_text
            else:
                await ctx.send('Invalid cog specified.\n'
                               + 'Use `help` command to list all cogs.')
                return
        await ctx.send(embed=help_embed)

    @commands.command(name='restart_admin', help='Restarts the RoR2 server', usage='time')
    @commands.check(shared.is_host)
    async def restart_admin(self, ctx):
        """Admin server restart command.

        :param ctx: Discord context
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            await ctx.send('Restarting server... please wait....')
            if await shared.restart(str(ctx.message.channel.id)):
                await ctx.send('Server restarted!')
            else:
                await ctx.send('Server could not be restarted')
        else:
            await ctx.send('Server is not running, unable to restart...')

    @commands.command(name='kick', help='kick a player from the game', usage='playername')
    @commands.check(shared.is_host)
    async def kick(self, ctx, *, kick_player):
        """Admin kick/ban of a player from the server.

        :param ctx: Discord context
        :param kick_player: Full or partial steam name of a player
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            author = ctx.author
            containskickplayer = False
            for player in serverinfo['server_players']:
                if kick_player.upper() in player.name.upper():
                    containskickplayer = True
                    kick_player = player.name
                    break
            if containskickplayer:
                logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
                             f'{ctx.message.author.name} kicked {kick_player}')
                await ctx.send(f'{kick_player} has been kicked by {author.mention}')
                await shared.execute_cmd(str(ctx.message.channel.id), "ban '" + kick_player + "'")
            else:
                await ctx.send(kick_player + ' is not playing on the server')
        else:
            await ctx.send('Server is not running...')

    @kick.error
    async def kick_handler(self, ctx, error):
        """Handles errors related to an incomplete player name with kick.

        :param ctx: Discord context
        :param error: The error created by the command.
        """
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'kick_player':
                await ctx.send('Please insert a partial or complete player name')

    @commands.command(name='endrun_admin', help='Begins a vote to end the current run')
    @commands.check(shared.is_host)
    async def endrun_admin(self, ctx):
        """Admin command to end the current run.

        :param ctx: Discord context
        """
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            if serverinfo['server_info'].map_name in ('lobby', 'title', 'splash'):
                await ctx.send('No run in progress.')
            else:
                await shared.execute_cmd(str(ctx.message.channel.id), 'run_end')
                await ctx.send('Run ended, all players have been returned to the lobby')
        else:
            await ctx.send('Server is not running...')

    @commands.command(name='delete',
                      help='Deletes the given amount of messages in the channel',
                      usage='number')
    @commands.check(shared.is_host)
    async def delete(self, ctx, number=5):
        """Deletes messages/embeds/images from the channel.

        :param ctx: Discord context
        :param number: Amount of messages to delete
        """
        logging.info(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
                     f'{ctx.message.author.name} used {ctx.command.name} on {number} messages.')
        number = number + 1
        await ctx.message.channel.purge(limit=number)

    @delete.error
    async def delete_handler(self, ctx, error):
        """Handles error caused by the delete command.

        :param ctx: Discord context
        :param error: Error raised by the command
        """
        if isinstance(error, commands.MissingRequiredArgument):
            logging.warning(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] '
                            f'{ctx.message.author.name} caused an error with '
                            + f'{ctx.command.name} | Message: {ctx.message.content} | '
                            + f'Error: {error}')
            await ctx.send('Please enter the number of messages to delete. '
                           + 'Example: ```delete 5```')

    @commands.command(name='addban')
    @commands.check(shared.is_host)
    async def ban(self, ctx, *, player_name):
        logging.info(
            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} used {ctx.command.name}')
        serverinfo = await shared.server(str(ctx.message.channel.id))
        if serverinfo:
            for player in serverinfo['server_players']:
                if player_name.upper() in player.name.upper():
                    try:
                        # Add the player to the ban database
                        ban_table.put_item(
                            Item={
                                'SteamName': player.name,
                                'BanDate': str(datetime.today().strftime('%d-%b-%Y')),
                                'BannedBy': ctx.message.author.name
                            }
                        )
                        # Issue the ban in-game command
                        await shared.execute_cmd(str(ctx.message.channel.id), "ban '" + player.name + "'")
                        await ctx.send(f'{player.name} has been banned.')
                        logging.info(
                            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] {ctx.message.author.name} banned {player.name}')
                    except Exception:
                        await ctx.send(f'Failed banning {player.name}')
                        logging.error(
                            f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Failed banning {player.name}')


def setup(bot):
    """Loads the cog into bot.py."""
    try:
        bot.add_cog(Ror2_admin(bot))
        logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Loaded cog: ror2_admin.py')
    except Exception as e:
        logging.warning(
            f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unable to load ror2_admin.py. Error: {e}')


def teardown(bot):
    """Prints to terminal when cog is unloaded."""
    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unloaded cog: ror2_admin.py')
