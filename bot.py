#!/usr/bin/env python3

"""The main Python program to run and control Pyre Bot.
Pyre Bot lets you manage game servers from a Discord server and is continually improving.

Usage:
    bot.py
"""

import logging

import discord
from discord.ext import commands

from pyre.config.config import *

# Log settings
logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='/data/discord/bot.log',
                    level=logging.INFO
                    )
logging.getLogger('discord').setLevel(logging.WARNING)
logging.info('Bot started')

bot = commands.Bot(command_prefix='>', case_insensitive=True)
cogs = [
    'cogs.ror2',
    'cogs.ror2_admin',
    'cogs.misc'
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
    print(
        f'Connected to Discord as: \n'
        f'{bot.user.name}(id: {bot.user.id})\n'
        f'----------'
    )
    logging.info(f'Bot connected as {bot.user.name}(id: {bot.user.id})')
    for cog in cogs:
        try:
            bot.load_extension(cog)
            logging.info(f'Loaded {cog}')
        except Exception:
            logging.warning(f'Error loading {cog}, trying second method.')
            try:
                bot.unload_extension(cog)
                bot.load_extension(cog)
                logging.info(f'Loaded {cog}')
            except Exception:
                logging.warning(f'Unable to load cog: {cog}')
                print(f'Unable to load {cog}')

    # TESTING -- Posts a message to admin channel
    admin_channel = bot.get_channel(737812925414244442)
    await admin_channel.send('👀 Bot is online.')


# Load and Unload cogs stuff
@bot.command()
@commands.has_role(role)
async def load(ctx, extension):
    """Loads the specified cog into the bot.

    :param ctx: Discord context
    :param extension: Name of the cog to load
    """
    bot.load_extension(f'cogs.{extension}')
    logging.info(f'Loaded {extension}')


@bot.command()
@commands.has_role(role)
async def unload(ctx, extension):
    """Unloads the specified cog from the bot.

    :param ctx: Discord context
    :param extension: Name of the cog to unload
    """
    bot.unload_extension(f'cogs.{extension}')
    logging.info(f'Unloaded {extension}')


@bot.command()
@commands.has_role(role)
async def reload(ctx, cog='all'):
    """Reloads the specified cog, if there is no cog specified reloads all of them.

    :param ctx: Discord context
    :param cog: Name of the cog to reload
    """
    if cog == 'all':
        for item in cogs:
            bot.unload_extension(item)
            bot.load_extension(item)
            logging.info(f'Reload {item}')
    else:
        bot.unload_extension(cog)
        bot.load_extension(cog)
        logging.info(f'Reloaded {cog}')


# Pyre Bot uses a custom help command so we must remove the built-in one
bot.remove_command('help')

# Tells discord.py to run the bot
try:
    bot.run(discord_token)
except discord.errors.LoginFailure:
    logging.warning("Login unsuccessful.")
