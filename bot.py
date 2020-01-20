# bot.py
import os
import discord
from discord.ext import commands
from configparser import ConfigParser
from pathlib import Path

# Configuration settings
config_file = Path("config/config.ini")
config_path = Path.cwd().joinpath('config')

# Checks if the config file exists, otherwise makes it
if config_file.exists():
    pass
else:
    if config_path.exists():
        pass
    else:
        os.makedirs(config_path)

    config_object = ConfigParser()
    config_object["API"] = {
                            "DISCORD_TOKEN": "token"
    }
    config_object["RoR2"] = {
                            "SERVER_ADDRESS": "your-server-address",
                            "SERVER_PORT": "your-server-port",
                            "steamcmd": "path-to-steamcmd",
                            "ror2ds": "path-to-ror2ds",
                            "BepInEx": "path-to-bepinex",
                            "role": "privilledged-server-role",
                            "channel": "enter-channel-id"
    }
    with open('config/config.ini', 'w') as conf:
        config_object.write(conf)

# Loads the configuartion file
config_object = ConfigParser()
config_object.read("config/config.ini")
api = config_object["API"]

# Load Discord API token from config file
token = api["DISCORD_TOKEN"]

bot = commands.Bot(command_prefix=('r!', 'ig!', '>'), case_insensitive=True)


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command doesn't exist, please view help for more information.")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send('Too many arguments, plase try again.')
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have permissions to do this.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("You don't have permissions to do this.")

# Do this when the bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Waiting for something to do!'))
    print(
          f'Connected to Discord as: \n'
          f'{bot.user.name}(id: {bot.user.id})\n'
          f'Using {config_file}\n'
          f'----------'
    )

# Load and Unload cogs stuff
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Discord bot token
try:
    bot.run(token)
except discord.errors.LoginFailure:
    print("Login unsuccessful.")
