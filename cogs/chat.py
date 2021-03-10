#!/usr/bin/env python3

"""Functions and methods related to the chat capabilities of the bot."""

import asyncio
import random
import sys
from datetime import datetime

import discord
from discord.ext import commands

import libs.shared as shared
from config.config import *
from libs.server import servers
from libs.leaderboard import leaderboards

# Info chat vars
server_embeds = {}
start_info = False  # Without this the info function can post an update before all messages are sent

# Leaderboard vars
leaderboards_embeds = None
start_leaderboards = False


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
                  f'start_info: {str(start_info)}. server_channel: {server.command_channel}. stage: {server.stage}. '
                  f'time: {str(server.runtime)}')

    # Does nothing if the embeds aren't fully created
    if start_info is False:
        return

    try:
        await server.info()  # Updates object information
        update_channel = self.bot.get_channel(int(server_update_channel))
        # Embed information
        embed = discord.Embed(
            title=str(server.name),
            colour=discord.Colour.blue())
        embed.set_footer(text='Last Updated: ' + str(datetime.now(tz).strftime(i_fmt)))
        embed.add_field(name='Run Time', value=f'{server.runtime}', inline=True)
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
        if server.command_channel not in server_embeds.keys():
            message = await update_channel.send(embed=embed)
            server_embeds[server.command_channel] = message
        elif server.command_channel in server_embeds.keys():
            message = server_embeds[server.command_channel]
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
            server_info = await shared.server(str(servers[server].command_channel))
            server_name = str(server_info['server_info'].server_name)
        except Exception as e:
            print(e)
            server_name = str(servers[server].command_channel)

        # Embed information
        embed = discord.Embed(
            title=str(server_name),
            colour=discord.Colour.blue())
        embed.set_footer(text='Last Updated: ' + str(datetime.now(tz).strftime(i_fmt)))
        embed.add_field(name='Waiting for update...', value='Waiting for update...')

        # Send embed and store in dictionary for later use
        message = await update_channel.send(embed=embed)
        server_embeds[servers[server].command_channel] = message  # I think this just prints the channel name if nothing else is given, seen this with servers that don't get made

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
        player = self.bot.get_user(int(rank))
        if str(player) == 'None':
            continue  # Don't list users who have left the discord
        else:
            place += 1
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


# Should update server info every x seconds
async def autoupdate_info(self):
    """Starts and runs the autoupdate function.

    Parameters
    ----------
    self : bot.py
        Discord bot object
    """
    logging.debug(f'[Pyre-Bot:Debug][{datetime.now(tz).strftime(t_fmt)}] Starting autoupdate_info_func.')
    while True:
        await asyncio.sleep(5)  # Setting to 5 for debugging, real time will be 60
        for server in servers:
            await info_chat(self, server)

class Chat(commands.Cog):
    """Cog used to load and manage chat capabilities"""
    def __init__(self, bot):
        self.bot = bot
        try:
            asyncio.gather(autoupdate_info(self), info_chat_load(self), leaderboards_load(self))
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
