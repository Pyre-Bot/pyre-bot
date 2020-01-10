# bot.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import cassiopeia as cass

# Get token info from .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
rtoken = os.getenv('RIOT_TOKEN')

bot = commands.Bot(command_prefix=('r!', 'ig!', '>'))

# Riot API and Cassiopeia info
# This overrides the value set in your configuration/settings.
cass.set_riot_api_key(rtoken)
cass.set_default_region("NA")


# Do this when the bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Waiting for something to do!'))
    print(f'{bot.user.name} has connected to Discord!')

# Load and Unload cogs stuff
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
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
