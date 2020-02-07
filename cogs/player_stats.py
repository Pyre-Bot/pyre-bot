import ast
import asyncio
import logging
import os
import re
import sqlite3
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

import a2s
import discord
import psutil
from discord.ext import commands
from pygtail import Pygtail

players = []


class Player:
    def __init__(self, id, start_time):
        self.id = id
        self.start = start_time


config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]
general = config_object["General"]
server_address = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')

db = Path.cwd().joinpath('stats.db')


async def add_player(line):
    global players
    now = datetime.utcnow()
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    players.append(Player(player_id, now))


async def commit_player(line):
    global players
    now = datetime.utcnow()
    player_id = re.search(r'\((.*?)\)', line).group(1)
    player_id = re.sub("[^0-9]", "", player_id)
    for player in players:
        if player_id == player.id:
            gametime = now - player.start
            player = (player.id, gametime)
            try:
                await sql_insert(player)
            except:
                print('Error adding to DB')


async def sql_insert(player):
    con = sqlite3.connect(db)
    c = con.cursor()
    c.execute(
        'CREATE TABLE if not exists players(id integer PRIMARY KEY, gametime real)')
    try:
        c.execute('''INSERT INTO players(id, gametime) VALUES(?, ?)''', player)
    except sqlite3.IntegrityError:
        c.execute(f'UPDATE players SET gametime = {player[2]} WHERE id = {player[0]}')
    con.commit()
