#!/usr/bin/env python3

"""Pyre Bot Risk of Rain 2 admin functions."""

import ast
import asyncio
import logging
import os
import re
from configparser import ConfigParser
from pathlib import Path

import a2s
import psutil
from discord.ext import commands
from pygtail import Pygtail

import cogs.player_stats as stats

config_object = ConfigParser()
config_file = Path.cwd().joinpath('config', 'config.ini')
config_object.read(config_file)
ror2 = config_object["RoR2"]
general = config_object["General"]

# Config variables
server_address = config_object.get(
    'RoR2', 'server_address'), config_object.getint('RoR2', 'server_port')
steamcmd = Path(ror2["steamcmd"])
ror2ds = Path(ror2["ror2ds"])
BepInEx = Path(ror2["BepInEx"])
role = general["role"]
c_autostart = ror2['auto-start-chat']
s_restart = ror2['auto-server-restart']
hidden_mods = ast.literal_eval(config_object.get('RoR2', 'hidden_mods'))
botcmd = Path.joinpath(BepInEx, 'plugins', 'BotCommands')
logfile = (BepInEx / "LogOutput.log")

# Global variables (yes, I know, not ideal but I'll fix them later)
yes, no = 0, 0
repeat = 0
stagenum = 0
run_timer = 0
# These get assigned / updated every time server() is called
server_info = ''
server_players = ''


# Dictionaries used for functions
equip = {
    'CommandMissile': 'Disposable Missile Launcher',
    'Saw': 'Saw',
    'Fruit': 'Foreign Fruit',
    'Meteor': 'Glowing Meteorite',
    'SoulJar': 'Jar of Souls',
    'AffixRed': "Ifrit's Distinction",
    'AffixBlue': 'Silence Between Two Strikes',
    'AffixYellow': '',
    'AffixGold': 'Coven of Gold',
    'AffixWhite': 'Her Biting Embrace',
    'AffixPoison': "N'kuhana's Retort",
    'Blackhole': 'Primordial Cube',
    'GhostGun': "Reaper's Remorse",
    'CritOnUse': 'Ocular HUD',
    'DroneBackup': 'The Back-up',
    'OrbitalLaser': 'EQUIPMENT_ORBITALLASER_NAME',
    'BFG': 'Preon Accumulator',
    'Enigma': 'EQUIPMENT_ENIGMA_NAME',
    'Jetpack': 'Milky Chrysalis',
    'Lightning': 'Royal Capacitor',
    'GoldGat': 'The CrowdFunder',
    'Passive Healing': 'Gnarled Woodsprite',
    'LunarPotion': 'EQUIPMENT_LUNARPOTION_NAME',
    'BurnNearby': 'Hellfire Tincture',
    'SoulCorruptor': 'EQUIPMENT_SOULCORRUPTOR_NAME',
    'Scanner': 'Radar Scanner',
    'CrippleWard': 'Effigy of Grief',
    'Gateway': 'Eccentric Vase',
    'Tonic': 'Spinel Tonic',
    'QuestVolatileBattery': 'Fuel Array',
    'Cleanse': 'Blast Shower',
    'FireBallDash': 'Volcanic Egg',
    'AffixHaunted': 'Spectral Circlet',
    'GainArmor': 'Jade Elephant'
}

item = {
    'Syringe': "Soldier's Syringe",
    'Bear': 'Tougher Times',
    'Behemoth': 'Brilliant Behemoth',
    'Missile': 'ATG Missile Mk. 1',
    'ExplodeOnDeath': "Will-o'-the-wisp",
    'Dagger': 'Ceremonial Dagger',
    'Tooth': 'Monster Tooth',
    'CritGlasses': "Lens-Maker's Glasses",
    'Hoof': "Paul's Goat Hoof",
    'Feather': 'Hopoo Feather',
    'AACannon': 'AA Cannon',
    'ChainLightning': 'Ukulele',
    'PlasmaCore': 'Plasma Core',
    'Seed': 'Leeching Seed',
    'Icicle': 'Frost Relic',
    'GhostOnKill': 'Happiest Mask',
    'Mushroom': 'Bustling Fungus',
    'Crowbar': 'Crowbar',
    'LevelBonus': 'ITEM_LEVELBONUS_NAME',
    'AttackSpeedOnCrit': 'Predatory Instincts',
    'BleedOnHit': 'Tri - Tip Dagger',
    'SprintOutOfCombat': 'Red Whip',
    'FallBoots': 'H3AD - 5T v2',
    'CooldownOnCrit': 'Wicked Ring',
    'WardOnLevel': 'Warbanner',
    'Phasing': 'Old War Stealthkit',
    'HealOnCrit': "Harvester's Scythe",
    'HealWhileSafe': 'Cautious Slug',
    'TempestOnKill': 'ITEM_TEMPESTONKILL_NAME',
    'PersonalShield': 'Personal Shield Generator',
    'EquipmentMagazine': 'Fuel Cell',
    'NovaOnHeal': "N'kuhana's Opinion",
    'ShockNearby': 'Unstable Tesla Coil',
    'Infusion': 'Infusion',
    'WarCryOnCombat': '',
    'Clover': '57 Leaf Clover',
    'Medkit': 'Medkit',
    'Bandolier': 'Bandolier',
    'BounceNearby': 'Sentient Meat Hook',
    'IgniteOnKill': 'Gasoline',
    'PlantOnHit': 'ITEM_PLANTONHIT_NAME',
    'StunChanceOnHit': 'Stun Grenade',
    'Firework': 'Bundle of Fireworks',
    'LunarDagger': 'Shaped Glass',
    'GoldOnHit': 'Brittle Crown',
    'MageAttunement': 'ITEM_MAGEATTUNEMENT_NAME',
    'WarCryOnMultiKill': "Berzerker's Pauldron",
    'BoostHp': 'ITEM_BOOSTHP_NAME',
    'BoostDamage': 'ITEM_BOOSTDAMAGE_NAME',
    'ShieldOnly': 'Transcendence',
    'AlienHead': 'Alien Head',
    'Talisman': 'Soulbound Catalyst',
    'Knurl': 'Titanic Knurl',
    'BeetleGland': "Queen's Gland",
    'BurnNearby': 'ITEM_BURNNEARBY_NAME',
    'CritHeal': 'ITEM_CRITHEAL_NAME',
    'CrippleWardOnLevel': 'ITEM_CRIPPLEWARDONLEVEL_NAME',
    'SprintBonus': 'Energy Drink',
    'SecondarySkillMagazine': 'Backup Magazine',
    'StickyBomb': 'Sticky Bomb',
    'TreasureCache': 'Rusted Key',
    'BossDamageBonus': 'Armor - Piercing Rounds',
    'SprintArmor': 'Rose Buckler',
    'IceRing': "Runald's Band",
    'FireRing': "Kjaro's Band",
    'SlowOnHit': 'Chronobauble',
    'ExtraLife': "Dio's Best Friend",
    'ExtraLifeConsumed': "Dio's Best Friend(Consumed)",
    'UtilitySkillMagazine': 'Hardlight Afterburner',
    'HeadHunter': 'Wake of Vultures',
    'KillEliteFrenzy': 'Brainstalks',
    'RepeatHeal': 'Corpsebloom',
    'Ghost': 'ITEM_GHOST_NAME',
    'HealthDecay': 'ITEM_HEALTHDECAY_NAME',
    'AutoCastEquipment': 'Gesture of the Drowned',
    'IncreaseHealing': 'Rejuvenation Rack',
    'JumpBoost': 'Wax Quail',
    'DrizzlePlayerHelper': 'ITEM_DRIZZLEPLAYERHELPER_NAME',
    'ExecuteLowHealthElite': 'Old Guillotine',
    'EnergizedOnEquipmentUse': 'War Horn',
    'BarrierOnOverHeal': 'Aegis',
    'TonicAffliction': 'Tonic Affliction',
    'TitanGoldDuringTP': 'Halcyon Seed',
    'SprintWisp': 'Little Disciple',
    'BarrierOnKill': 'Topaz Brooch',
    'ArmorReductionOnHit': 'Shattering Justice',
    'TPHealingNova': 'Lepton Daisy',
    'NearbyDamageBonus': 'Focus Crystal',
    'LunarUtilityReplacement': 'Strides of Heresy',
    'MonsoonPlayerHelper': 'ITEM_MONSOONPLAYERHELPER_NAME',
    'Thorns': 'Razorwire',
    'RegenOnKill': 'Fresh Meat',
    'Pearl': 'Pearl',
    'ShinyPearl': 'Irradiant Pearl',
    'BonusGoldPackOnKill': "Ghor's Tome",
    'LaserTurbine': 'Resonance Disc',
    'LunarPrimaryReplacement': 'Visions of Heresy',
    'NovaOnLowHealth': 'Genesis Loop',
    'LunarTrinket': 'Beads of Fealty'
}

stages = {
    # Time not started (keep stage at 0)
    'title': 'Title',
    'lobby': 'Game Lobby',
    # Time running normal
    'blackbeach': 'Distant Roost',
    'blackbeach2': 'Distant Roost',
    'golemplains': 'Titanic Plains',
    'golemplains2': 'Titanic Plains',
    'foggyswamp': 'Wetland Aspect',
    'goolake': 'Abandoned Aqueduct',
    'frozenwall': 'Rallypoint Delta',
    'wispgraveyard': 'Scorched Acres',
    'dampcave': 'Abyssal Depths',
    'shipgraveyard': "Siren's Call",
    # Time paused, no stage progression on following stages
    'bazaar': 'Hidden Realm: Bazaar Between Time',
    'goldshores': 'Hidden Realm: Glided Coast',
    'mysteryspace': 'Hidden Realm: A Moment, Fractured',
    'limbo': 'Hidden Realm: A Moment, Whole',
    'arena': 'Hidden Realm: Void Fields'
}

async def chat(self):
    """Reads the BepInEx output log to send chat to Discord."""
    channel = config_object.getint('RoR2', 'channel')
    channel = self.bot.get_channel(channel)
    global stagenum
    global run_timer
    global yes, no
    if os.path.exists(logfile):
        if os.path.exists(BepInEx / "LogOutput.log.offset"):
            for line in Pygtail(str(logfile)):
                updatestats = False  # Required to limit the updates to once per line
                # Player chat
                if "issued: say" in line:
                    line = line.replace('[Info   : Unity Log] ', '**')
                    line = re.sub(r" ?\([^)]+\)", "", line)
                    line = line.replace(' issued:', ':** ')
                    line = line.replace(' say ', '')
                    await channel.send(line)
                # Run time
                elif ('[Info   : Unity Log] Run time is ' in line):
                    line = str(line.replace('[Info   : Unity Log] Run time is ', ''))
                    run_timer = float(line)
                    run_timer = int(run_timer)
#                    print('run_timer: ' + str(run_timer))  # DEBUG
                    updatestats = True
                # Stages cleared
                elif ('[Info   : Unity Log] Stages cleared: ' in line):
                    line = str(line.replace(
                        '[Info   : Unity Log] Stages cleared: ', ''))
                    stagenum = int(line)
#                    print('stagenum: ' + str(stagenum))  # DEBUG
                    updatestats = True
                # Stage change
                elif "Active scene changed from" in line:
                    for key, value in stages.items():
                        if key in line:
                            devstage = key
                            stage = value
                            break
                    if devstage in ('bazaar', 'goldshores', 'mysteryspace', 'limbo', 'arena'):
                        await channel.send('**Entering Stage - ' + stage + '**')
                    # Won't output if the stage is title, done on purpose
                    elif devstage in ('lobby', 'title'):
                        if devstage == 'lobby':
                            await channel.send('**Entering ' + stage + '**')
                    else:
                        if stagenum == 0:
                            await channel.send('**Entering Stage ' + str(stagenum + 1) + ' - ' + stage + '**')
                        else:
                            if (run_timer - (int(run_timer / 60)) * 60) < 10:
                                formattedtime = str(
                                    int(run_timer / 60)) + ':0' + str(run_timer - (int(run_timer / 60)) * 60)
                            else:
                                formattedtime = str(
                                    int(run_timer / 60)) + ':' + str(run_timer - (int(run_timer / 60)) * 60)
                            await channel.send('**Entering Stage ' + str(stagenum + 1) + ' - ' + stage + ' [Time - ' + formattedtime + ']**')
                # Player joins
                elif "[Info   :     R2DSE] New player : " in line:
                    await stats.add_player(line, run_timer, stagenum)  # Still required for now
                    updatestats = False
                    line = line.replace(
                        '[Info   :     R2DSE] New player : ', '**Player Joined - ')
                    line = line.replace(' connected. ', '')
                    line = re.sub(r" ?\([^)]+\)", "", line)
                    await channel.send(line + '**')
                # Player leaves
                elif "[Info   :     R2DSE] Ending AuthSession with : " in line:
                    line = line.replace(
                        '[Info   :     R2DSE] Ending AuthSession with : ', '**Player Left - ')
                    line = re.sub(r" ?\([^)]+\)", "", line)
                    await channel.send(line + '**')
                elif "[Info   : Unity Log] Server(0) issued: run_end" in line:
                    await stats.update_stats(run_timer, stagenum, 1)
                    updatestats = False
                if updatestats:
                    await stats.update_stats(run_timer, stagenum)
        else:
            for line in Pygtail(str(logfile)):
                pass


async def server():
    """
    Checks if the server is running or not.
    Returns:
        Boolean: Used by functions calling this to check if running
    """
    global server_info
    global server_players
    try:
        server_info = a2s.info(server_address, 1.0)
        server_players = a2s.players(server_address)
        return True
    except:
        #        print("Server error:", sys.exc_info()[0], sys.exc_info()[1]) #  Used for debugging
        return False


async def server_restart():
    """Checks every 120 minutes if no players are active then restarts the server."""
    server_restart = s_restart
    if server_restart == "true":
        print('Auto server restarting enabled')
        while server_restart == "true":
            await asyncio.sleep(7200)
            if os.path.exists(BepInEx / "LogOutput.log"):
                try:
                    os.remove(BepInEx / "LogOutput.log")
                except Exception:
                    print('Unable to remove log file')
            if os.path.exists(BepInEx / "LogOutput.log.offset"):
                try:
                    os.remove(BepInEx / "LogOutput.log.offset")
                except Exception:
                    print('Unable to remove offset! Chat may not work!')
            await asyncio.sleep(5)
            await server()
            if server_info.player_count == 0:
                await server_stop()
                await asyncio.sleep(10)
                os.startfile(ror2ds / "Risk of Rain 2.exe")
                print('Server restarted')
            elif server_info.player_count > 0:
                print('Players currently in server')
    else:
        print('Not restarting server')


async def chat_autostart(self):
    """Autostarts live chat output if it is enabled."""
    chat_autostart = c_autostart
    if chat_autostart:
        print('Auto chat output enabled')
        global repeat
        repeat = 1
        if os.path.exists(BepInEx / "LogOutput.log.offset"):
            try:
                os.remove(BepInEx / "LogOutput.log.offset")
            except Exception:
                print('Unable to remove offset! Chat may not work!')
        while repeat == 1:
            await chat(self)
            await asyncio.sleep(1)
    else:
        print('Not outputting chat')


async def server_stop():
    """
    Stops the server.
    Returns:
        Boolean: Indicates whether server stopped or not
    """
    for proc in psutil.process_iter():
        exe = Path.cwd().joinpath(ror2ds, 'Risk of Rain 2.exe')
        try:
            processExe = proc.exe()
            if str(exe) == processExe:
                proc.kill()
                logging.info('Server stopped')
                return True
        except:
            pass
    return False


async def find_dll():
    """
    Checks to see if the BotCommands plugin is installed on server.
    Returns:
        Boolean: If true it is, otherwise it is not
    """
    plugin_dir = (BepInEx / 'plugins')
    files = [file.name for file in plugin_dir.glob('**/*') if file.is_file()]
    if 'BotCommands.dll' in files:
        return True
    logging.warning('Unable to find BotCommands.dll!')
    return False


class ror2_admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.gather(chat_autostart(self), server_restart())

    # Start the RoR2 server
    @commands.command(name='start', help='Starts the server if it is not running')
    @commands.has_role(role)
    async def start(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        # Checks to make sure the server is not running before starting it
        if await server():
            await ctx.send('Server is already running!')
        else:
            started = False
            # Path of log file, removes before starting
            if os.path.exists(BepInEx / "LogOutput.log"):
                try:
                    os.remove(BepInEx / "LogOutput.log")
                except Exception:
                    print('Unable to remove log file')
            # Path of log offset file, removes before starting
            if os.path.exists(BepInEx / "LogOutput.log.offset"):
                try:
                    os.remove(BepInEx / "LogOutput.log.offset")
                except Exception:
                    print('Unable to remove log offset file')

            # Starts the server
            try:
                os.startfile(ror2ds / "Risk of Rain 2.exe")
                started = True
                await ctx.send('Starting Risk of Rain 2 Server, please wait...')
                await asyncio.sleep(15)
            except Exception:
                logging.warning('Error starting the server!')
                await ctx.send('Unable to start the server, please check the logs')

            # After 15 seconds checks logs to see if server started
            while started is True:
                with open(BepInEx / "LogOutput.log") as f:
                    for line in f:
                        if "Loaded scene lobby" in line:
                            await ctx.send('Server started successfully...')
                            started = False
                            break

    # Exits the server
    @commands.command(name='stop', help='Stops the server if currently running')
    @commands.has_role(role)
    async def stop(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        if await server():
            stopped = await server_stop()
            if stopped is True:
                await ctx.send('Risk of Rain 2 server shut down...')
            else:
                await ctx.send('Unable to stop server!')
        else:
            await ctx.send('Server is not running!')

    # Runs the update bat file, updates server via SteamCMD
    @commands.command(
        name='update',
        help='Updates the server, must be off before running this'
    )
    @commands.has_role(role)
    async def update(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        # Checks to make sure the server is not running before updating it
        if await server() is False:
            await ctx.send('Updating server, please wait...')
            updated = 1
            # Path of log file, removes before starting
            if os.path.exists(steamcmd / "logs/content_log.txt"):
                try:
                    os.remove(steamcmd / "logs/content_log.txt")
                except Exception:
                    print('Unable to remove log file')
                await asyncio.sleep(2)
            os.startfile(steamcmd / "RoR2DSUpdate.bat")
            await asyncio.sleep(15)

            # After 15 seconds checks logs to see if server updated
            while updated == 1:
                with open(steamcmd / "logs/content_log.txt") as f:
                    for line in f:
                        if "AppID 1180760 scheduler finished" in line:
                            await ctx.send('Server updated...')
                            updated = 2
                            break
        else:
            await ctx.send('You must stop the server prior to updating!')

    # Executes say on the server

    @commands.command(
        name='say',
        help='Sends a message from the server',
        usage='message'
    )
    @commands.has_role(role)
    async def serversay(self, ctx, *, message):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        if await server() and await find_dll() is True:
            append = open(botcmd / "botcmd.txt", 'a')
            append.write('say "' + message + '"\n')
            append.close()
        elif await server() is False:
            await ctx.send('Server is not running...')
        elif await find_dll() is False:
            await ctx.send('BotCommands plugin is not loaded on the server!')

    # EXPERIMENTAL - Use with caution
    # Passes on a command to be interpreted directly by the console
    # TODO: Test this when there's a lot of output, i.e. many players at once
    @commands.command(
        name='cmd',
        help='Passes on a command to be interpreted directly by the console',
        usage='command'
    )
    @commands.has_role(role)
    async def customcmd(self, ctx, *, cmd_with_args):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        if await server() and await find_dll() is True:
            global server_info
            if server_info.map_name in ('lobby', 'title'):
                await ctx.send('No run in progress. Use >say if you want to send a message to the lobby.')
            else:
                append = open(botcmd / "botcmd.txt", 'a')
                append.write(cmd_with_args + '\n')
                append.close()
                findline = True
                consoleout = ''
                tempreader = Pygtail(str(logfile))
                while findline:
                    for line in tempreader:
                        #                    print('line -' + str(line))  # DEBUG
                        if ('Server(0) issued' in line):
                            continue
                        elif ('is not a recognized ConCommand or ConVar.' in line):
                            await ctx.send(cmd_with_args + ' is not a valid command')
                            findline = False
                            break
                        elif ('[Info   : Unity Log]' in line):  # There's an \n in every line
                            consoleout = str(line.replace('[Info   : Unity Log] ', ''))
                            findline = False
                            continue
                        elif ('[Error  : Unity Log]' in line):  # There's an \n in every line
                            consoleout = str(line.replace(
                                '[Error  : Unity Log] ', 'Error - '))
                            findline = False
                            continue
                        elif str(line) != '\n':
                            #                        print('not newline')  # Debug
                            consoleout += str(line)
                            findline = False  # This was the trick, keep going through the lines until there are none left, and then the encompassing while loop will break
                            continue
                        else:
                            #                        print('newline')  # Debug
                            findline = False
                            continue
                await ctx.send('**Server: **' + consoleout)
        elif await server() is False:
            await ctx.send('Server is not running...')
        elif await find_dll() is False:
            await ctx.send('BotCommands plugin is not loaded on the server!')

    # Executes give_item on the server
    @commands.command(
        name='giveitem',
        help='Gives a player a specified quantity of an item',
        usage='playername itemname qty'
    )
    @commands.has_role(role)
    async def giveitem(self, ctx, playername, itemname, qty="1"):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        if await server() and await find_dll() is True:
            global server_info
            if server_info.map_name in ('lobby', 'title'):
                await ctx.send('No run in progress')
            else:
                containsplayer = False
                for player in server_players:
                    if playername.upper() in player.name.upper():
                        playername = player.name
                        containsplayer = True
                        break
                if containsplayer is True:
                    append = open(botcmd / "botcmd.txt", 'a')
                    append.write('give_item "' + itemname + '" '
                                 + qty + ' "' + playername + '"\n')
                    append.close()
                    findline = True
                    tempreader = Pygtail(str(logfile))
                    while findline:
                        for line in tempreader:
                            if ('[Info   : Unity Log] The requested object could not be '
                                    + 'found' in line):
                                await ctx.send(itemname + ' is not a valid item name')
                                findline = False
                                break
                            elif "[Info   : Unity Log] Gave" in line:
                                if "None" in line:
                                    pass
                                else:
                                    for key, value in item.items():
                                        if key in line:
                                            itemname = value
                                            break
                                    await ctx.send('Gave ' + qty + ' ' + itemname + ' to '
                                                   + playername)
                                    findline = False
                                    break
                elif containsplayer is False:
                    await ctx.send(playername + ' is not playing on the server')
        elif await server() is False:
            await ctx.send('Server is not running...')
        elif await find_dll() is False:
            await ctx.send('BotCommands plugin is not loaded on the server!')

    @giveitem.error
    async def giveitem_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'playername':
                logging.warning(
                    f'{ctx.message.author.name} caused an error with '
                    + f'{ctx.command.name} | Message: {ctx.message.content} | '
                    + f'Error: {error}')
                await ctx.send('Please enter a partial or complete player name')
            if error.param.name == 'itemname':
                logging.warning(
                    f'{ctx.message.author.name} caused an error with '
                    + f'{ctx.command.name} | Message: {ctx.message.content} | '
                    + f'Error: {error}')
                await ctx.send('Please enter a valid item name')

    # Executes give_equip on the server
    @commands.command(
        name='giveequip',
        help='Gives a player a specified equipment',
        usage='playername equipname'
    )
    @commands.has_role(role)
    async def giveequip(self, ctx, playername, equipname):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        if await server() and await find_dll() is True:
            global server_info
            if server_info.map_name in ('lobby', 'title'):
                await ctx.send('No run in progress')
            else:
                containsplayer = False
                for player in server_players:
                    if playername.upper() in player.name.upper():
                        playername = player.name
                        containsplayer = True
                        break
                if containsplayer is True:
                    append = open(botcmd / "botcmd.txt", 'a')
                    append.write('give_equip "' + equipname + '" "'
                                 + playername + '"\n')
                    append.close()
                    findline = True
                    tempreader = Pygtail(str(logfile))
                    while findline:
                        for line in tempreader:
                            if ('[Info   : Unity Log] The requested object could not be '
                                    + 'found' in line):
                                await ctx.send(equipname + ' is not a valid equipment name')
                                findline = False
                                break
                            elif "[Info   : Unity Log] Gave" in line:
                                if "None" in line:
                                    pass
                                else:
                                    for key, value in equip.items():
                                        if key in line:
                                            equipname = value
                                            break
                                    await ctx.send('Gave ' + equipname + ' to '
                                                   + playername)
                                    findline = False
                                    break
                elif containsplayer is False:
                    await ctx.send(playername + ' is not playing on the server')
        elif await server() is False:
            await ctx.send('Server is not running...')
        elif await find_dll() is False:
            await ctx.send('BotCommands plugin is not loaded on the server!')

    @giveequip.error
    async def giveequip_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'playername':
                logging.warning(
                    f'{ctx.message.author.name} caused an error with '
                    + f'{ctx.command.name} | Message: {ctx.message.content} | '
                    + f'Error: {error}')
                await ctx.send('Please enter a partial or complete player name')
            if error.param.name == 'equipname':
                logging.warning(
                    f'{ctx.message.author.name} caused an error with '
                    + f'{ctx.command.name} | Message: {ctx.message.content} | '
                    + f'Error: {error}')
                await ctx.send('Please enter a valid equipment name')

    # Output RoR server chat to Discord
    @commands.command(
        name='start_chat',
        help='Displays live chat from the server to the specified channel in Discord'
    )
    @commands.has_role(role)
    async def start_chat(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        await ctx.send('Displaying chat messages from the server!')
        global repeat
        repeat = 1
        if os.path.exists(BepInEx / "LogOutput.log.offset"):
            try:
                os.remove(BepInEx / "LogOutput.log.offset")
            except Exception:
                print('Unable to remove offset! Old messages may be displayed.')
        while repeat == 1:
            await chat(self)
            await asyncio.sleep(1)

    # Stop outputting live server chat to Discord
    @commands.command(
        name='stop_chat',
        help='Stops outputting live chat from the server'
    )
    @commands.has_role(role)
    async def stop_chat(self, ctx):
        logging.info(f'{ctx.message.author.name} used {ctx.command.name}')
        global repeat
        if repeat == 0:
            await ctx.send('Not outputting chat to Discord!')
        else:
            repeat = 0
            await ctx.send('Stopping outputting live chat to the server...')

    # Print server configuration
    @commands.command(name='config', help='Prints the server configuration')
    @commands.has_role(role)
    async def config(self, ctx):
        await ctx.send('Coming soon!')


def setup(bot):
    """Loads the cog into bot.py."""
    bot.add_cog(ror2_admin(bot))
    print('Loaded cog: ror2_admin.py')


def teardown(bot):
    """Prints to termianl when cog is unloaded."""
    global repeat
    print('Unloaded cog: ror2_admin.py')
    repeat = 0
