# bot.py
import os
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path

import discord
from discord.ext import commands

# Configuration settings
config_file = Path("config/config.ini")
config_path = Path.cwd().joinpath('config')

# Checks if the config file exists, otherwise runs setup
if config_file.exists():
    pass
else:
    setup = subprocess.Popen(['python', (Path.cwd() / 'setup' / 'setup.py')])
    setup.wait()
    os.startfile(__file__)
    sys.exit()

# Loads the configuartion file
config_object = ConfigParser()
config_object.read("config/config.ini")
api = config_object["API"]
token = api["discord_token"]

bot = commands.Bot(command_prefix=('r!', 'ig!', '>'), case_insensitive=True)
cogs = [
    'cogs.ror2',
    'cogs.admin'
]

# Error handling
# @bot.event
# async def on_command_error(ctx, error):
#     """Used to catch discord.py errors."""
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please pass in all required arguments.')
#     elif isinstance(error, commands.CommandNotFound):
#         await ctx.send("Command doesn't exist, please view help for more information.")
#     elif isinstance(error, commands.TooManyArguments):
#         await ctx.send('Too many arguments, plase try again.')
#     elif isinstance(error, commands.MissingAnyRole):
#         await ctx.send("You don't have permissions to do this.")
#     elif isinstance(error, commands.NotOwner):
#         await ctx.send("You don't have permissions to do this.")


# Do this when the bot is ready
@bot.event
async def on_ready():
    """Outputs to terminal when bot is ready."""
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game('Waiting for something to do!')
    )
    print(
        f'Connected to Discord as: \n'
        f'{bot.user.name}(id: {bot.user.id})\n'
        f'Using {config_file}\n'
        f'----------'
    )
    for cog in cogs:
        bot.load_extension(cog)


# Load and Unload cogs stuff
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """
    Loads the specified cog.

    Args:
        extension (str): The file name, with .py, to load
    """
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    """
    Unloads the specified cog.

    Args:
        extension (str): The file name, with .py, to unload
    """
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def reload(ctx, cog='all'):
    """
    Reloads the specified cog.

    Args:
        cog (str): The file name, with .py, to reload
    """
    if cog == 'all':
        for cog in cogs:
            bot.unload_extension(cog)
            bot.load_extension(cog)
    else:
        bot.unload_extension(cog)
        bot.load_extension(cog)

bot.remove_command('help')

# Discord bot token
try:
    bot.run(token)
except discord.errors.LoginFailure:
    print("Login unsuccessful.")
