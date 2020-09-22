#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 chat functions."""

import asyncio
import logging
import re
from datetime import datetime

import discord
from profanity_filter import ProfanityFilter
from discord.ext import commands

import libs.shared as shared
from config.config import *
from libs.pygtail import Pygtail

# Profanity filter settings
pf = ProfanityFilter()
pf.censor_char = '&'

# Chat repeat variable
repeat = False

# Info chat vars
server_embeds = {}
start_info = False  # Without this the info function can post an update before all messages are sent


# TODO: Add anti-spam
async def chat(self, channel):
    """Reads the BepInEx output log to send chat to Discord."""
    global stagenum
    global run_timer
    serverlogs = await shared.server_logs()
    for log_name in serverlogs:
        if str(channel) in log_name:
            bot_channel = self.bot.get_channel(int(channel))
            if os.path.exists(logpath / log_name):
                if os.path.exists(logpath / (log_name + '.offset')):
                    for line in Pygtail(str(logpath / log_name), read_from_end=True):
                        # Player chat
                        if "issued: say" in line:
                            line = line.replace(line[:58], '**')
                            line = re.sub(r" ?\([^)]+\)", "", line)
                            line = line.replace(' issued:', ':** ')
                            line = line.replace(' say ', '')
                            if len(line) < 2000:
                                await bot_channel.send(pf.censor(line))
                            else:
                                await bot_channel.send('Error showing message: Message too long')
                        # Run time
                        elif '[Info:Unity Log] Run time is ' in line:
                            line = str(line.replace(line[:70], ''))
                            run_timer = float(line)
                            run_timer = int(run_timer)
                        # Stages cleared
                        elif '[Info:Unity Log] Stages cleared: ' in line:
                            line = str(line.replace(line[:74], ''))
                            stagenum = int(line)
                        # Stage change
                        elif "Active scene changed from" in line:
                            devstage = '???'
                            stage = '???'
                            for key, value in shared.stages.items():
                                if key in line:
                                    devstage = key
                                    stage = value
                                    break
                            if devstage in (
                                    'bazaar', 'goldshores', 'mysteryspace', 'limbo', 'arena', 'artifactworld', 'outro'):
                                await bot_channel.send('**Entering Stage - ' + stage + '**')
                                await info_chat(self, channel, stage, run_timer)
                            # Won't output if the stage is title or splash, done on purpose
                            elif devstage in ('lobby', 'title', 'splash'):
                                if devstage == 'lobby':
                                    await bot_channel.send('**Entering ' + stage + '**')
                                    run_timer = 0
                                    stagenum = 0
                                    await info_chat(self, channel, stage, run_timer)
                            else:
                                if stagenum == 0:
                                    await bot_channel.send(
                                        '**Entering Stage ' + str(stagenum + 1) + ' - ' + stage + '**')
                                    await info_chat(self, channel, stage, run_timer)
                                else:
                                    formattedtime = await shared.format_time(run_timer)
                                    await bot_channel.send('**Entering Stage ' + str(
                                        stagenum + 1) + ' - ' + stage + ' [Time - ' + formattedtime + ']**')
                                    await info_chat(self, channel, stage, run_timer)
                        # Player joins
                        elif "[Info:R2DSE] New player :" in line:
                            line = line.replace(line[:67], '**Player Joined - ')
                            line = line.replace(' connected. ', '')
                            line = re.sub(r" ?\([^)]+\)", "", line)
                            await bot_channel.send(line + '**')
                        # Player leaves
                        elif "[Info:R2DSE] Ending AuthSession with" in line:
                            line = line.replace(line[:80], '**Player Left - ')
                            line = re.sub(r" ?\([^)]+\)", "", line)
                            await bot_channel.send(line + '**')
                else:
                    for _ in Pygtail(str(logpath / log_name), read_from_end=True):
                        pass


async def info_chat(self, server_channel, stage, time):
    """Gathers the current server information and returns an embed message.

    Parameters
    ----------
    self : bot
        Discord bot object
    server_channel : str
        Chat channel for the server
    stage : str
        The current stage the server is on
    time : int
        The current run time

    Returns
    -------
    Returns if the embed messages aren't created yet.
    """
    global server_embeds
    global start_info

    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] info_chat called. start_info: {str(start_info)}. server_channel: {server_channel}. stage: {stage}. time: {str(time)}')

    if start_info is False:
        return

    serverinfo = await shared.server(str(server_channel))
    try:
        update_channel = self.bot.get_channel(int(server_update_channel))
        formatted_time = await shared.format_time(time)

        # Creates the string of player names used in the embed
        player_names = []
        for player in serverinfo['server_players']:
            player_names.append(player.name)
        player_names = ("\n".join(map(str, player_names)))

        # Embed information
        embed = discord.Embed(
            title=str(serverinfo['server_info'].server_name),
            colour=discord.Colour.blue())
        embed.set_footer(text='Last Updated: ' + str(datetime.now(tz)))
        embed.add_field(name='Stage', value=f'{stage}', inline=True)
        embed.add_field(name='Run Time', value=f'{formatted_time}', inline=True)
        embed.add_field(
            name='Player Count',
            value=str(serverinfo['server_info'].player_count) + '/' + str(serverinfo['server_info'].max_players),
            inline=True)
        if serverinfo['server_info'].player_count == 0:
            pass
        else:
            embed.add_field(
                name='Players', value=player_names, inline=True)

        # Send or update the message
        if server_channel not in server_embeds.keys():
            message = await update_channel.send(embed=embed)
            server_embeds[server_channel] = message
        elif server_channel in server_embeds.keys():
            message = server_embeds[server_channel]
            await message.edit(embed=embed)
    except Exception as e:
        logging.error(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Failed to update server embded for '
                      f'{serverinfo["server_info"].server_name}: {e}')


async def info_chat_load(self):
    """Creates the empty embeds for the info_chat function.

    Parameters
    ----------
    self : bot
        Discord bot object
    """
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Starting info_chat_load.')
    global server_embeds
    global start_info

    update_channel = self.bot.get_channel(int(server_update_channel))  # Gets the server updates channel object
    # await update_channel.purge(limit=12)  # Removes previous messages from the channel

    # Create empty embed for all channels
    for channel in chat_channels:
        try:
            server_info = await shared.server(str(channel))
            server_name = server_info.server_name
        except:
            server_name = str(channel)

        # Embed information
        embed = discord.Embed(
            title=str(server_name),
            colour=discord.Colour.blue())
        embed.set_footer(text='Last Updated: ' + str(datetime.now(tz)))
        embed.add_field(name='Waiting for update...', value='Waiting for update...')

        # Send embed and store in dictionary for later use
        message = await update_channel.send(embed=embed)
        server_embeds[channel] = message

    # Allows the info_chat to function
    start_info = True
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Finished info_chat_load.')


async def chat_autostart_func(self):
    """Autostarts live chat output if it is enabled."""
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Starting chat_autostart_func.')
    do_autostart = chat_autostart
    if do_autostart:
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
            for configchannel in chat_channels:
                await chat(self, configchannel)
            await asyncio.sleep(0.5)


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.gather(chat_autostart_func(self), info_chat_load(self))


def setup(bot):
    """Loads the cog into bot.py."""
    try:
        bot.add_cog(Chat(bot))
        logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Loaded cog: chat.py')
    except Exception as e:
        logging.error(
            f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unable to load chat.py. Error: {e}')


def teardown(bot):
    """Prints to terminal when cog is unloaded."""
    global repeat
    repeat = False  # Stops the chat function
    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unloaded cog: chat.py')
