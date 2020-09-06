#!/usr/bin/env python3

"""Collection of functions and commands that don't fit into other cogs."""

import datetime
import logging
import random

import discord
import requests
from discord.ext import commands

import pyre.libs.shared as shared
from pyre.config.config import *


async def stat_tracking(ctx):
    """Custom check to determine is stats are being checked.

    Parameters
    ----------
    ctx : Any
        Current Discord context

    Returns
    -------
    bool
        Status if stats are being tracked.
    """
    if track_stats == "yes":  # TODO: Change this to be nicer
        return True
    else:
        return False


class Misc(commands.Cog):
    """Commands that are not fitting into other cogs.

    Parameters
    ----------
    commands.Cog : Cog
        The base cog class used for all discord.py cogs.

    Methods
    -------
    help(ctx, cog='all')
        Outputs the help options when called upon.
    link(ctx, steamid)
        Links the members SteamID to their DiscordID
    stats(ctx)
        Posts the member's stats

    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member, ctx):
        """Adds Discord member to database when they join the server.

        This is used to track member retention in the server.

        Parameters
        ----------
        member : discord.Member
            Discord member information
        ctx : Any
            Current Discord context
        """
        logging.info(f'{member.name} joined the server! Discord ID: {member.id}')
        if await stat_tracking(ctx):
            try:
                await discord_table.put_item(
                    Item={
                        'DiscordID': str(member.id),
                        'DiscordName': str(member.name),
                        'JoinDate': str(datetime.datetime.utcnow())
                    }
                )
            except TypeError:
                # put_item doesn't like async so we pass the error because we know it happens.
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member, ctx):
        """Updates the database with the user leave date.

        Parameters
        ----------
        member : discord.Member
            Discord member information
        ctx : Any
            Current Discord context
        """
        if await stat_tracking(ctx):
            try:
                r_key = {'DiscordID': str(member.id)}
                try:
                    response = discord_table.get_item(Key=r_key)
                except TypeError:
                    # get_item doesn't like async so we pass the error because we know it happens.
                    pass
                response = response['Item']
                response['LeaveDate'] = str(datetime.datetime.utcnow())
                try:
                    discord_table.put_item(
                        Item={
                            'DiscordID': str(response['DiscordID']),
                            'DiscordName': str(response['DiscordName']),
                            'JoinDate': str(response['JoinDate']),
                            'LeaveDate': str(response['LeaveDate'])
                        }
                    )
                except TypeError:
                    # put_item doesn't like async so we pass the error because we know it happens.
                    pass
            except TypeError:
                # boto3 doesn't like async so we pass teh error because we know it happens.
                pass

    # noinspection DuplicatedCode
    @commands.command(name='help', help='Displays this message', usage='cog')
    async def help(self, ctx, cog='all'):
        """Creates and sends a custom help output to the channel.

        Parameters
        ----------
        ctx : Any
            Current Discord context
        cog : str
            Name of the cog to get help information about

        """
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
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
                if 'admin' in cog:
                    pass
                else:
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

    @commands.command(name='link',
                      help='Links a user to their Steam ID',
                      usage='steamid')
    @commands.check(stat_tracking)
    async def link(self, ctx, steamid):
        """Link command used to tie Discord names and IDs to SteamIDs.

        Parameters
        ----------
        ctx : Any
            Current Discord context
        steamid : str
            Member's SteamID to be linked to the DiscordID
        """
        linked = False
        user = ctx.message.author  # Sender is a Member class object
        linkedrole = ctx.guild.get_role(linked_id)
        r = requests.get(request_url + str(steamid))
        r_list = r.text.splitlines()

        for line in r_list:
            if '"keywords":' in line:
                keyword_line = line.replace(
                    '                "keywords": "steamid, ', '')
                keyword_line = keyword_line.replace('",', '')
                keyword_line = keyword_line.replace(', ', ';')
                keyword_line = keyword_line.split(';')
                if len(keyword_line) == 3:
                    keyword_line.append('None')

        for user_role in user.roles:
            if user_role == linkedrole:
                linked = True
                break
        try:
            # Adds the items to the database or overwrites the current values
            await stats_players.put_item(
                Item={
                    'DiscordID': str(user.id),
                    'DiscordName': str(user.name),
                    'steamid64': int(keyword_line[2]),
                    'SteamID': str(keyword_line[0]),
                    'SteamID3': str(keyword_line[1]),
                    'Steam CustomURL': str(keyword_line[3])
                }
            )
        except TypeError:
            # boto3 doesn't like async so we pass the error because we are expecting it
            pass

        if linked is False:
            await user.add_roles(linkedrole)
            await ctx.send(f'Steam ID linked for {user.name}')
            logging.info(
                f'{user.name} has linked to their Steam ID ({steamid}) using the {ctx.command.name} command.')
        else:
            await ctx.send(f'Steam ID updated for {user.name}')
            logging.info(
                f'{user.name} has updated their Steam ID ({steamid}) using the {ctx.command.name} command.')

    # TODO: Change to using single server
    @commands.command(name='stats', help='Retrieves player stats for the Risk of Rain 2 server')
    @commands.check(stat_tracking)
    async def stats(self, ctx):
        """Retrieves stats from the database and posts an embed.

        Parameters
        ----------
        ctx : Any
            Current Discord context
        """
        server = None
        user = ctx.message.author
        try:
            stat_names = {
                'totalStagesCompleted': 'Stages Completed',
                'totalKills': 'Kills',
                'totalTimeAlive': 'Time Alive',
                'totalPurchases': 'Purchases',
                'totalDeaths': 'Deaths',
                'totalItemsCollected': 'Items Collected',
                'totalGoldCollected': 'Gold Collected',
                'highestLevel': 'Highest Level'
            }
            proceed = False
            user = ctx.message.author
            linkedrole = ctx.guild.get_role(linked_id)
            for this_role in user.roles:
                if this_role == linkedrole:
                    proceed = True
                    break
            if proceed:
                for serverdict in server_list:
                    if serverdict["commands_channel"] == str(ctx.message.channel.id) or serverdict["admin_channel"] == str(ctx.message.channel.id):
                        server = serverdict["server_name"]
                        break
                try:
                    key = {'DiscordID': str(user.id)}
                    steamid = stats_players.get_item(Key=key)
                    steamid = steamid['Item']['steamid64']
                    key = {'SteamID64': int(steamid)}
                    response = stats_table.get_item(Key=key)
                    response = response['Item'][server]

                    embed = discord.Embed(title=f'Stats for {user.name}', colour=discord.Colour.orange())
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_author(name=self.bot.guilds[0])
                    for key, value in response.items():
                        if key == 'totalTimeAlive':
                            value = datetime.timedelta(seconds=int(float(value)))
                        for k, v in stat_names.items():
                            if k == key:
                                name = v
                                embed.add_field(name=str(name), value=str(value), inline=True)
                    await ctx.send(embed=embed)
                except KeyError:
                    # Sent if the SteamID isn't linked in the Players table
                    await ctx.send(
                        'Your Steam ID does not have any stats associated with it. Play on the server at least once to '
                        'create a stats profile')
            else:
                await ctx.send('You have not linked your Steam ID. To do so, use the command >link [your Steam ID]')
        except Exception as e:
            logging.warning(e)
        logging.info(f'{user.name} used {ctx.command.name}')


def setup(bot):
    """Loads the cog into the bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        Discord bot object
    """
    bot.add_cog(Misc(bot))
    logging.info('Loaded cog: misc.py')


def teardown(bot):
    """Removes the cog from the bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        Discord bot object
    """
    logging.info('Unloaded cog: misc.py')
