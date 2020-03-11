#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 random functions."""

import datetime
import json
import logging
import random
import decimal
from configparser import ConfigParser
from pathlib import Path

import discord
import boto3
from botocore.exceptions import ClientError
from discord.ext import commands

config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]
general = config_object["General"]
role = general["role"]
linked_id = int(general["linked-id"])

colors = {
    'DEFAULT': 0x000000,
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'GREY': 0x95A5A6,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_GREY': 0x979C9F,
    'DARKER_GREY': 0x7F8C8D,
    'LIGHT_GREY': 0xBCC0C0,
    'DARK_NAVY': 0x2C3E50,
    'BLURPLE': 0x7289DA,
    'GREYPLE': 0x99AAB5,
    'DARK_BUT_NOT_BLACK': 0x2C2F33,
    'NOT_QUITE_BLACK': 0x23272A
}

channels = {
    'Server1': {'admin': 670373469845979136, 'commands': 665998238171660320},
    'Server2': {'admin': 671917010422333460, 'commands': 671921930873602099},
    'Server3': {'admin': 672682539390992384, 'commands': 672682345089859654},
    'Server4': {'admin': 672940159091867648, 'commands': 672939900600975362}
}

# Connects to Amazon DynamoDB and access the tables
dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="https://dynamodb.us-east-2.amazonaws.com")
players = dynamodb.Table('Players')
stats = dynamodb.Table('Stats')


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Displays this message', usage='cog')
    async def help(self, ctx, cog='all'):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        color_list = [c for c in colors.values()]
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

    @commands.command(name='help_admin', help='Displays this message', usage='cog')
    @commands.has_role(role)
    async def help_admin(self, ctx, cog='all'):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        color_list = [c for c in colors.values()]
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

    @commands.command(name='delete',
                      help='Deletes the given amount of messages in the channel',
                      usage='number')
    @commands.has_role(role)
    async def delete(self, ctx, number=5):
        logging.info(
            f'{ctx.message.author.name} used {ctx.command.name} on {number} messages.')
        number = number + 1
        await ctx.message.channel.purge(limit=number)

    @delete.error
    async def delete_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            logging.warning(
                f'{ctx.message.author.name} caused an error with '
                + f'{ctx.command.name} | Message: {ctx.message.content} | '
                + f'Error: {error}')
            await ctx.send('Please enter the number of messages to delete. '
                           + 'Example: ```delete 5```')

    @commands.command(name='link',
                      help='Links a user to their Steam ID',
                      usage='steamid')
    async def link(self, ctx, steamid):
        global table
        linked = False
        user = ctx.message.author  # Sender is a Member class object
        linkedrole = ctx.guild.get_role(linked_id)

        for role in user.roles:
            if role == linkedrole:
                linked = True
                break
        try:
            # Adds the items to the database or overwrites the current values
            await players.put_item(
                Item={
                    'steamid64': int(steamid),
                    'DiscordID': str(user.id),
                    'DiscordName': str(user.name)
                }
            )
        except:
            # For some reason the above is always throwing an Error
            # Temporary just pass so that it proceeds (everything works)
            # TODO: Figure out why it throws an error
            pass

        if linked is False:
            await user.add_roles(linkedrole)
            await ctx.send(f'Steam ID linked for {user.name}')
        else:
            await ctx.send(f'Steam ID updated for {user.name}')
        logging.info(
            f'{user.name} has linked to their Steam ID ({steamid}) using the {ctx.command.name} command.')

    @commands.command(name='stats',
                      help='Retrieves player stats for the Risk of Rain 2 server')
    async def stats(self, ctx):
        proceed = False
        user = ctx.message.author
        linkedrole = ctx.guild.get_role(linked_id)
        for role in user.roles:
            if role == linkedrole:
                proceed = True
                break
        if proceed:
            for key, value in channels.items():
                for k, v in channels[key].items():
                    if ctx.channel.id == v:
                        server = key
            try:
                # The key variable is used to find the entry in the table
                key = {'DiscordID': str(user.id)}
                steamid = players.get_item(Key=key)
                steamid = steamid['Item']['steamid64']
                key = {'SteamID64': str(steamid)}
                response = stats.get_item(Key=key)
                # If you don't do the below you also get the metadata
                response = response['Item'][server]

                # Create embed
                embed = discord.Embed(
                    title=f'Stats for {user.name}',
                    colour=discord.Colour.orange()
                    )
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_author(name=self.bot.guilds[0])
                for key, value in response.items():
                    if key == 'Time Played':
                        value = datetime.timedelta(seconds=int(value))
                    embed.add_field(
                        name=str(key), value=str(value), inline=False)
                await ctx.send(embed=embed)

            except KeyError:
                # Called if the SteamID isn't linked in the Players table
                await ctx.send('Your Steam ID does not have any stats associated with it. Play on the server at least once to create a stats profile')

        else:
            await ctx.send('You have not linked your Steam ID. To do so, use the command >link [your Steam ID]')
        logging.info(
            f'{user.name} used {ctx.command.name}')


def setup(bot):
    """Loads the cog into bot.py."""
    bot.add_cog(misc(bot))
    print('Loaded cog: misc.py')


def teardown(bot):
    """Prints to termianl when cog is unloaded."""
    print('Unloaded cog: misc.py')
