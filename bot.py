#!/usr/bin/env python3

"""The main Python program to run and control Pyre Bot.
Pyre Bot lets you manage game servers from a Discord server and is continually improving.

Usage:
    bot.py
"""

import sys
from datetime import datetime

import discord
#import seqlog
from discord.ext import commands

from config.config import *
from libs.server import servers, Server
from libs.leaderboard import leaderboards, Leaderboard, lb_stats

# Seq configuration
#seqlog.log_to_seq(
#    server_url=f"{seq_url}:80",
#    api_key=seq_api,
#    level=log_level,
#    batch_size=5,
#    auto_flush_timeout=5,  # seconds
#    override_root_logger=True
#)

logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Bot started')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=('>', '$'), case_insensitive=True, intents=intents)
cogs = [
    'cogs.ror2',
    'cogs.ror2_admin',
    'cogs.misc',
    'cogs.chat'
]


# # Error handling
# @bot.event
# async def on_command_error(ctx, error):
#     """Used to catch discord.py errors."""
#     if isinstance(error, commands.MissingRequiredArgument):
#         if check_channel(ctx) is True:
#             await ctx.send('Please pass in all required arguments.')
#             logging.warning(f'Argument error detected on command {ctx.command.name}')
#     elif isinstance(error, commands.CommandNotFound):
#         if check_channel(ctx) is True:
#             await ctx.send("Command doesn't exist, please view help for more information.")
#             logging.warning(
#                 f'Command not found on command {ctx.message.content}')
#     elif isinstance(error, commands.TooManyArguments):
#         if check_channel(ctx) is True:
#             await ctx.send('Too many arguments, please try again.')
#             logging.warning(f'Argument error detected on command: {ctx.command.name}')
#     elif isinstance(error, commands.MissingAnyRole):
#         if check_channel(ctx) is True:
#             await ctx.send("You don't have permission to do this.")
#             logging.warning(
#                 f'Permission error from {ctx.message.author.name} '
#                 + f'on command: {ctx.command.name}')
#     elif isinstance(error, commands.NotOwner):
#         if check_channel(ctx) is True:
#             await ctx.send("You don't have permissions to do this.")
#             logging.warning(
#                 f'Permission error from {ctx.message.author.name} '
#                 + f'on command: {ctx.command.name}')
#     elif isinstance(error, commands.CheckFailure):
#         # We don't need this output since we are expecting it
#         pass


# Do this when the bot is ready
@bot.event
async def on_ready():
    """Outputs to terminal when bot is ready."""

    await bot.change_presence(
        status=discord.Status.online
    )

    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Bot connected as {bot.user.name}(id: {bot.user.id})')

    # Load cogs into the bot
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception:
            logging.warning(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Error loading {cog}.')

    # Create server class objects
    for server in server_list:
        servers[server['server_name']] = Server(server['server_name'],  # Change to use steam info fetch?
                                                server['server_address'],
                                                'Lobby',  # Stage
                                                '0:00',  # Run time
                                                server['admin_channel'],
                                                server['commands_channel'],
                                                None,  # Players
                                                0,  # Number of current players
                                                0)  # Max players

    # Create leaderboard class objects
    for stat in lb_stats:
        leaderboards[stat] = Leaderboard(stat)
        await leaderboards[stat].only10()

    # Posts a message to admin channel
    admin_channel = bot.get_channel(admin_update_channel)
    await admin_channel.send(f'👀 {len(server_list)} server class objects created, bot online.')


# Load and Unload cogs stuff
@bot.command()
@commands.has_role(role)
async def load(ctx, extension):
    """
    Loads the specified cog.
    Args:
        ctx: Required argument to be passed by discord.py
        extension (str): The file name, with .py, to load
    """
    bot.load_extension(f'cogs.{extension}')
    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Loaded {extension}')


@bot.command()
@commands.has_role(role)
async def unload(ctx, extension):
    """
    Unloads the specified cog.
    Args:
        ctx: Required argument to be passed by discord.py
        extension (str): The file name, with .py, to unload
    """
    bot.unload_extension(f'cogs.{extension}')
    logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unloaded {extension}')


@bot.command()
@commands.has_role(role)
async def reload(ctx, cog='all'):
    """
    Reloads the specified cog.
    Args:
        ctx: Required argument to be passed by discord.py
        cog (str): The file name, with .py, to reload
    """
    if cog == 'all':
        for item in cogs:
            bot.unload_extension(item)
            bot.load_extension(item)
            logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Reloaded {item}')
    else:
        bot.unload_extension(cog)
        bot.load_extension(cog)
        logging.info(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Reloaded {cog}')


# Pyre Bot uses a custom help command so we must remove the built-in one
bot.remove_command('help')

# Tells discord.py to run the bot
try:
    bot.run(discord_token)
except discord.errors.LoginFailure as e:
    logging.error(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Unable to log in to Discord: {e}')
    sys.exit(1)
except discord.errors.HTTPException as e:
    logging.error(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Error connection to Discord: {e}.')
    sys.exit(1)
finally:
    logging.warning(f'[Pyre-Bot:Admin][{datetime.now(tz).strftime(t_fmt)}] Exiting the bot.')
    sys.exit(1)
