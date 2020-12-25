#!/usr/bin/env python3

"""Functions and methods related to the chat capabilities of the bot."""

import asyncio
import random
import re
import sys
from datetime import datetime

import discord
from profanity_filter import ProfanityFilter
from discord.ext import commands

import libs.shared as shared
from config.config import *
from libs.pygtail import Pygtail
from libs.server import servers
from libs.leaderboard import leaderboards

# Profanity filter settings
pf = ProfanityFilter()
pf.censor_char = '&'

# Chat repeat variable
repeat = False

# Info chat vars
server_embeds = {}
start_info = False  # Without this the info function can post an update before all messages are sent

# Leaderboard vars
leaderboards_embeds = None
start_leaderboards = False


# TODO: Add anti-spam
async def chat(self, channel):
    """Reads the Seq output logs for events and posts to chat channels or calls info_chat.

    Parameters
    ----------
    self : bot
        Discord bot object
    channel : int
        Specified Discord chat channel
    """
    # Determines which object to use
    for key, value in servers.items():
        if channel == value.chat_channel:
            server = value
            break

    serverlogs = await shared.server_logs()
    for log_name in serverlogs:
        if str(channel) in log_name:
            bot_channel = self.bot.get_channel(int(channel))
            if os.path.exists(logpath / log_name):
                if os.path.exists(logpath / (log_name + '.offset')):
                    for line in Pygtail(str(logpath / log_name), read_from_end=True):
                        # Player chat
                        # if "issued: say" in line:
                        #     await chat_say(line, bot_channel)

                        # Run time
                        if '[Info:Unity Log] Run time is ' in line:
                            await chat_runtime(line, server)

                        # Stages cleared
                        elif '[Info:Unity Log] Stages cleared: ' in line:
                            await chat_stage_number(line, server)

                        # Stage change
                        elif "Active scene changed from" in line:
                            # await chat_stage_change(line, server, bot_channel)
                            await info_chat(self, server)

                        # Player updates
                        elif "[Info:R2DSE] New player :" in line or "[Info:R2DSE] Ending AuthSession with" in line:
                            # await chat_players(line, bot_channel)
                            await info_chat(self, server)
                else:
                    for _ in Pygtail(str(logpath / log_name), read_from_end=True):
                        pass


async def chat_say(line, channel):
    """Sends a chat message from the game to a channel.

    Parameters
    ----------
    line : str
        Message sent in game.
    channel : Channel
        Discord channel object to end the message.
    """
    line = line.replace(line[:58], '**')
    line = re.sub(r" ?\([^)]+\)", "", line)
    line = line.replace(' issued:', ':** ')
    line = line.replace(' say ', '')

    if len(line) < 2000:
        await channel.send(pf.censor(line))
    else:
        await channel.send('Error showing message: Message too long')


async def chat_runtime(line, server):
    """Updates the server's object when a run time update is sent from the server.

    Parameters
    ----------
    line : str
        Run time message sent from the server.
    server: Server
        Server class object
    """
    line = str(line.replace(line[:70], ''))
    run_timer = float(line)
    run_timer = int(run_timer)

    server.runtime = run_timer  # Updates saved run time


async def chat_stage_number(line, server):
    """Updates the server's object when a new stage number is available.

    Parameters
    ----------
    line : str
        Stage num message sent from the server.
    server : Server
        Server class object
    """
    line = str(line.replace(line[:74], ''))
    stage_number = int(line)

    server.stage_number = stage_number


async def chat_stage_change(line, server, channel):
    """Updates the stored stage for the server and sends a message to the chat channel with the new stage information.

    Parameters
    ----------
    line : str
        Stage update message sent from the server.
    server : Server
        Server class object
    channel : Channel
        Discord channel object to end the message.
    """
    devstage = '???'
    stage = '???'

    for key, value in shared.stages.items():
        if key in line:
            devstage = key
            stage = value
            break

    if devstage in ('bazaar', 'goldshores', 'mysteryspace', 'limbo', 'arena', 'artifactworld', 'outro'):
        await channel.send('**Entering Stage - ' + stage + '**')
        server.stage = stage  # Updates saved stage
    # Won't output if the stage is title or splash, done on purpose
    elif devstage in ('lobby', 'title', 'splash'):
        if devstage == 'lobby':
            await channel.send('**Entering ' + stage + '**')
            server.stage = stage  # Updates saved stage
            server.stage_number = 0  # Updates saved stage number
            server.runtime = 0  # Updates saved run time
    else:
        if server.stage_number == 0:
            server.stage_number += 1
            server.stage = stage  # Updates saved stage
            await channel.send('**Entering Stage ' + str(server.stage_number) + ' - ' + stage + '**')
        else:
            server.stage_number += 1
            server.stage = stage  # Updates saved stage
            formatted_time = await shared.format_time(server.runtime)
            await channel.send('**Entering Stage ' + str(server.stage_number) + ' - ' + stage + ' [Time - '
                               + formatted_time + ']**')


async def chat_players(line, channel):
    """Updates the stored players for the server and sends a message to Discord.

    Parameters
    ----------
    line : str
        Player update sent from the server.
    channel : Channel
        Discord channel object to end the message.
    """
    # Player joins
    if "[Info:R2DSE] New player :" in line:
        line = line.replace(line[:67], '**Player Joined - ')
        line = line.replace(' connected. ', '')
        line = re.sub(r" ?\([^)]+\)", "", line)

    # Player leaves
    elif "[Info:R2DSE] Ending AuthSession with" in line:
        line = line.replace(line[:80], '**Player Left - ')
        line = re.sub(r" ?\([^)]+\)", "", line)

    await channel.send(line + '**')


async def info_chat(self, server):
    """Gathers the current server information and returns an embed message.

    Parameters
    ----------
    self : bot
        Discord bot object
    server: Server
        Class object of the server

    Returns
    -------
    Returns if the embed messages aren't created yet.
    """
    global server_embeds
    global start_info

    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] info_chat called. '
                  f'start_info: {str(start_info)}. server_channel: {server.chat_channel}. stage: {server.stage}. '
                  f'time: {str(server.runtime)}')

    # Does nothing if the embeds aren't fully created
    if start_info is False:
        return

    try:
        await server.info()  # Updates object information

        update_channel = self.bot.get_channel(int(server_update_channel))
        formatted_time = await shared.format_time(server.runtime)

        # Embed information
        embed = discord.Embed(
            title=str(server.name),
            colour=discord.Colour.blue())
        embed.set_footer(text='Last Updated: ' + str(datetime.now(tz).strftime(i_fmt)))
        embed.add_field(name='Stage', value=f'{server.stage}', inline=True)
        embed.add_field(name='Run Time', value=f'{formatted_time}', inline=True)
        embed.add_field(
            name='Player Count',
            value=str(server.player_num) + '/' + str(server.max_players),
            inline=True)
        if server.player_num == 0:
            pass
        else:
            embed.add_field(
                name='Players', value=server.players, inline=True)

        # Send or update the message
        if server.chat_channel not in server_embeds.keys():
            message = await update_channel.send(embed=embed)
            server_embeds[server.chat_channel] = message
        elif server.chat_channel in server_embeds.keys():
            message = server_embeds[server.chat_channel]
            await message.edit(embed=embed)
    except Exception as e:
        logging.error(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Failed to update server embed for '
                      f'{server.name}: {e}')


async def info_chat_load(self):
    """Creates the empty embeds for the info_chat function.

    Parameters
    ----------
    self : Chat
        Discord bot object
    """
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Starting info_chat_load.')
    global server_embeds
    global start_info

    update_channel = self.bot.get_channel(int(server_update_channel))  # Gets the server updates channel object
    await update_channel.purge(limit=50)  # Removes previous messages from the channel

    # Create empty embed for all channels
    for server in servers:
        try:
            server_info = await shared.server(str(servers[server].chat_channel))
            server_name = str(server_info['server_info'].server_name)
        except Exception as e:
            print(e)
            server_name = str(servers[server].chat_channel)

        # Embed information
        embed = discord.Embed(
            title=str(server_name),
            colour=discord.Colour.blue())
        embed.set_footer(text='Last Updated: ' + str(datetime.now(tz).strftime(i_fmt)))
        embed.add_field(name='Waiting for update...', value='Waiting for update...')

        # Send embed and store in dictionary for later use
        message = await update_channel.send(embed=embed)
        server_embeds[servers[server].chat_channel] = message

    start_info = True  # Allows info_chat
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Finished info_chat_load.')


async def leaderboards_load(self):
    """Creates the embeds for the leaderboards.

    Parameters
    ----------
    self : Chat
        Discord bot object
    """
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Starting leaderboards_load.')
    global leaderboards_embeds
    global start_leaderboards

    leaderboard_channel = self.bot.get_channel(int(leaderboard_update_channel))  # Gets Discord channel
    await leaderboard_channel.purge(limit=50)

    embed = await create_leaderboards(self, 'Stages Completed')  # Create and send embed
    leaderboards_embeds = await leaderboard_channel.send(embed=embed)  # Store message ID

    # Add reactions for changing the leaderboard
    emojis = ['🗺', '☠', '⌛', '💰', '💀', '📦', '💹']
    for emoji in emojis:
        await leaderboards_embeds.add_reaction(emoji)
    start_leaderboards = True

    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Finished leaderboards_load.')


async def create_leaderboards(self, category):
    color_list = [c for c in shared.colors.values()]  # Gets random colors for embed
    ranks = await leaderboards[category].results()  # Gets results from Leaderboard class

    # Create embed
    embed = discord.Embed(
        title=f'{category} Leaderboard',
        color=random.choice(color_list)
    )
    embed.set_footer(text='Last Updated: ' + str(datetime.now(tz).strftime(i_fmt)))
    place = 0
    for rank, amount in ranks.items():
        place += 1
        player = self.bot.get_user(int(rank))
        if str(player) == 'None':
            player = rank  # If player no longer in Discord
        else:
            player = str(player)[:-5]  # Removed numbers from DiscordID
        if place == 1:
            embed.add_field(name=f'🥇 {player}', value=amount, inline=False)
        elif place == 2:
            embed.add_field(name=f'🥈 {player}', value=amount, inline=False)
        elif place == 3:
            embed.add_field(name=f'🥉 {player}', value=amount, inline=False)
        else:
            embed.add_field(name=player, value=amount, inline=False)

    return embed


async def chat_autostart_func(self):
    """Starts and runs the chat function.

    Parameters
    ----------
    self : bot.py
        Discord bot object
    """
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Starting chat_autostart_func.')
    global repeat
    repeat = True
    serverlogs = await shared.server_logs()
    for log_name in serverlogs:
        if os.path.exists(logpath / (log_name + '.offset')):
            try:
                os.remove(logpath / (log_name + '.offset'))
            except OSError as e:
                logging.error(f'Unable to start chat! Failed removing {e.filename}: {e.strerror}')
    while repeat:
        for config_channel in chat_channels:
            try:
                await chat(self, config_channel)
            except Exception as e:
                logging.error(f'[Pyre-Bot:Error][{datetime.now(tz).strftime(t_fmt)}] Chat error: {e}')
        await asyncio.sleep(0.5)


class Chat(commands.Cog):
    """Cog used to load and manage chat capabilities"""
    def __init__(self, bot):
        self.bot = bot
        try:
            asyncio.gather(chat_autostart_func(self), info_chat_load(self), leaderboards_load(self))
        except Exception as e:
            logging.error(f'[Pyre-Bot:Error][{datetime.now(tz).strftime(t_fmt)}] Chat Module error: {e}')
            sys.exit(2)  # Restarts bot on chat error

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Determines which leaderboard to change to.

        Parameters
        ----------
        payload : discord.Message
            The object containing the message reaction information.
        """
        if start_info and payload.message_id == leaderboards_embeds.id:
            embed = False
            if payload.emoji.name == '🗺':
                embed = await create_leaderboards(self, 'Stages Completed')
            elif payload.emoji.name == '☠':
                embed = await create_leaderboards(self, 'Kills')
            elif payload.emoji.name == '⌛':
                embed = await create_leaderboards(self, 'Time Alive')
            elif payload.emoji.name == '💰':
                embed = await create_leaderboards(self, 'Purchases')
            elif payload.emoji.name == '💀':
                embed = await create_leaderboards(self, 'Deaths')
            elif payload.emoji.name == '📦':
                embed = await create_leaderboards(self, 'Items Collected')
            elif payload.emoji.name == '💹':
                embed = await create_leaderboards(self, 'Gold Collected')

            if embed:
                await leaderboards_embeds.edit(embed=embed)
                await leaderboards_embeds.remove_reaction(payload.emoji.name, self.bot.get_user(payload.user_id))



def setup(bot):
    """Loads the cog into bot.py."""
    try:
        bot.add_cog(Chat(bot))
        logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Loaded cog: chat.py')
    except Exception as e:
        logging.error(
            f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unable to load chat.py. Error: {e}')


def teardown(bot):
    """Disable chat and then updates logs when unloading the cog."""
    global repeat
    repeat = False  # Stops the chat function
    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unloaded cog: chat.py')
