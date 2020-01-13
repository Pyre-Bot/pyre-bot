import os
import psutil
import asyncio
from pathlib import Path
import discord
from discord.ext import commands
import valve.source.a2s

# Server information
SERVER_ADDRESS = ('ror2.infernal.wtf', 27016)
steamcmd = Path("C:/steamcmd")
ror2ds = Path("C:/steamcmd/ror2ds")
BepInEx = Path("C:/steamcmd/ror2ds/BepInEx")
role = "RoR2 Admin"

# Global variables for restart vote
yes, no = 0, 0


class RoR2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    # Start the RoR2 server
    @commands.command(name='start', help='Starts the server if it is not running')
    @commands.has_role(role)
    async def start(self, ctx):
        # Checks to make sure the server is not running before starting it
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            await ctx.send('Server is already running!')
            break
        else:
            started = 1
        # Path of log file, removes before starting
        if os.path.exists(BepInEx / "LogOutput.log"):
            os.remove(BepInEx / "LogOutput.log")

        # Starts the server
        os.startfile(ror2ds / "Risk of Rain 2.exe")
        await ctx.send('Starting Risk of Rain 2 Server, please wait...')
        await asyncio.sleep(15)

        # After 15 seconds checks logs to see if server started
        while started == 1:
            with open(BepInEx / "LogOutput.log") as f:
                for line in f:
                    if "Loaded scene lobby" in line:
                        await ctx.send('Server started successfully...')
                        started = 2
                        break
    # Exits the server
    @commands.command(name='stop', help='Stops the server if currently running')
    @commands.has_role(role)
    async def stop(self, ctx):
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            process.kill()
            await ctx.send('Risk of Rain 2 server shut down...')
            break
        else:
            await ctx.send('Server is not running!')

    # Runs the update bat file, updates server via SteamCMD
    @commands.command(name='update', help='Updates the server, must be off before running this')
    @commands.has_role(role)
    async def update(self, ctx):
        # Checks to make sure the server is not running before updating it
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            await ctx.send('Stop the server before running this (r!stop)')
            break
        else:
            os.startfile(steamcmd / "RoR2DSUpdate.bat")
            await ctx.send('Updating server, please wait...')
            updated = 1
            # Path of log file, removes before starting
            if os.path.exists(steamcmd / "logs/content_log.txt"):
                os.remove(steamcmd / "logs/content_log.txt")
                await asyncio.sleep(15)

            # After 15 seconds checks logs to see if server updated
            while updated == 1:
                with open(steamcmd / "logs/content_log.txt") as f:
                    for line in f:
                        if "AppID 1180760 scheduler finished" in line:
                            await ctx.send('Server updated...')
                            updated = 2
                            break

    # Restart the server with votes
    @commands.command(name='restart', help='Initializes a vote to restart the RoR2 server')
    async def restart(self, ctx, time=60):
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            global yes, no
            yes, no = 0, 0
            author = ctx.author
            message = await ctx.send('A restart vote has been initiated by {author.mention}, please react to this message!'.format(author=author))
            for emoji in ('✅', '❌'):
                await message.add_reaction(emoji)
            await asyncio.sleep(time)

            # Queries Steamworks to get total players
            with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as query:
                players = []
                for player in query.players()["players"]:
                    if player["name"]:
                        players.append(player)
                player_count = len(players)
                # Counts vote, if tie does nothing
                if(yes == no):
                    await ctx.send('It was a tie! There must be a majority to restart the server!')
                # If 75% of player count wants to restart it will
                elif((yes-1) >= (player_count*0.75)):
                    started = 1
                    for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
                        process.kill()
                        await asyncio.sleep(5)

                    # Path of log file, removes before starting
                    if os.path.exists(BepInEx / "LogOutput.log"):
                        os.remove(BepInEx / "LogOutput.log")

                    # Starts the server
                    os.startfile(ror2ds / "Risk of Rain 2.exe")
                    await ctx.send('Starting Risk of Rain 2 Server, please wait...')
                    await asyncio.sleep(15)

                    # After 15 seconds checks logs to see if server started
                    while started == 1:
                        with open(BepInEx / "LogOutput.log") as f:
                            for line in f:
                                if "Loaded scene lobby" in line:
                                    await ctx.send('Server started successfully...')
                                    started = 2
                                    break
                # All other options
                else:
                    await ctx.send('Restart vote failed!')
                break
        else:
            await ctx.send('Server is not running, unable to restart...')

    # Used for restart command
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global yes, no
        if payload.emoji.name == "✅":
            yes = yes + 1
        elif payload.emoji.name == "❌":
            no = no + 1
        else:
            pass

    # Displays the status of the Server
    @commands.command(name='status', help='Displays the status of current session')
    async def status(self, ctx):
        for process in (process for process in psutil.process_iter() if process.name() == "Risk of Rain 2.exe"):
            # Create embed
            embed = discord.Embed(
                title='Risk of Rain 2 Server Information',
                colour=discord.Colour.blue()
            )
            # Use Steamworks API to query server
            with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
                info = server.info()
                players = server.players()
                ping = server.ping()

            # Embed information
            embed.set_footer(text='Steam query is not always accurate')
            embed.set_thumbnail(
                url='http://files.softicons.com/download/application-icons/variations-icons-3-by-guillen-design/png/256x256/steam.png')
            embed.set_author(name=self.bot.guilds[0])
            embed.add_field(name='Player Count and Server Name',
                            value="{player_count}/{max_players} {server_name}".format(**info), inline=False)
            for player in sorted(players["players"],
                                 key=lambda p: p["score"], reverse=True):
                first = 1
                if(first == 1):
                    embed.add_field(name='Players', value="{name}".format(
                        **player), inline=False)
                    first = 2
                else:
                    embed.add_field(name=' ', value="{name}".format(
                        **player), inline=False)
            embed.add_field(name='Server Ping',
                            value="{:n}".format(ping), inline=False)

            # Send embed
            await ctx.send(embed=embed)
            break
        else:
            await ctx.send('Server is currently stopped...')

    # Sends the Steam connection link
    # @commands.command(name='link', help='Get the Steam connection link')
    # async def link(self, ctx):
    #     await ctx.send('steam://connect/ror2.infernal.wtf:27015')

    # Print server configuration
    @commands.command(name='config', help='Prints the server configuration')
    @commands.has_role(role)
    async def config(self, ctx):
        await ctx.send('Coming soon!')


def setup(bot):
    bot.add_cog(RoR2(bot))
