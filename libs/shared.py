#!/usr/bin/env python3

"""Shared functions used throughout multiple cogs within Pyre Bot."""

import a2s

import asyncio
import json
import requests
from datetime import datetime, date, timedelta


from config.config import *


# Used for help command
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

# Available equipment to give players
equip = {
    'CommandMissile': 'Disposable Missile Launcher',
    'Saw': 'Saw',
    'Fruit': 'Foreign Fruit',
    'Meteor': 'Glowing Meteorite',
    'SoulJar': 'Jar of Souls',
    'AffixRed': "Ifrit's Distinction",
    'AffixBlue': 'Silence Between Two Strikes',
    'AffixYellow': 'AffixYellow',
    'AffixGold': 'Coven of Gold',
    'AffixWhite': 'Her Biting Embrace',
    'AffixPoison': "N'kuhana's Retort",
    'Blackhole': 'Primordial Cube',
    'GhostGun': "Reaper's Remorse",
    'CritOnUse': 'Ocular HUD',
    'DroneBackup': 'The Back-up',
    'OrbitalLaser': 'OrbitalLaser',
    'BFG': 'Preon Accumulator',
    'Enigma': 'Enigma',
    'Jetpack': 'Milky Chrysalis',
    'Lightning': 'Royal Capacitor',
    'GoldGat': 'The CrowdFunder',
    'Passive Healing': 'Gnarled Woodsprite',
    'LunarPotion': 'LunarPotion',
    'BurnNearby': 'Hellfire Tincture',
    'SoulCorruptor': 'SoulCorruptor',
    'Scanner': 'Radar Scanner',
    'CrippleWard': 'Effigy of Grief',
    'Gateway': 'Eccentric Vase',
    'Tonic': 'Spinel Tonic',
    'QuestVolatileBattery': 'Fuel Array',
    'Cleanse': 'Blast Shower',
    'FireBallDash': 'Volcanic Egg',
    'AffixHaunted': 'Spectral Circlet',
    'GainArmor': 'Jade Elephant',
    'Sawmerang': 'Sawmerang',
    'Recycle': 'Recycler',
    'LifestealOnHit': 'Super Massive Leech',
    'TeamWarCry': "Gorag's Opus",
    'DeathProjectile': 'Forgive Me Please'
}

# Available items to give players
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
    'LunarTrinket': 'Beads of Fealty',
    'FocusedConvergence': 'Focused Convergence',
    'ArtifactKey': 'Artifact Key',
    'RepulsionArmorPlate': 'Repulsion Armor Plate',
    'SquidTurret': 'Squid Polyp',
    'DeathMark': 'Death Mark',
    'InterstellarDeskPlant': 'Interstellar Desk Plant',
    'Incubator': 'Ancestral Incubator',
    'FocusConvergence': 'Focused Convergence',
    'CaptainDefenseMatrix': 'Defensive Microbots',
    'FireballsOnHit': 'Molten Perforator',
    'BleedOnHitAndExplode': 'Shatterspleen',
    'SiphonOnLowHealth': 'Mired Urn',
    'MonstersOnShrineUse': 'Defiant Gouge',
    'RandomDamageZone': 'Mercurial Rachis',
    'ScrapWhite': 'Item Scrap, White',
    'ScrapGreen': 'Item Scrap, Green',
    'ScrapRed': 'Item Scrap, Red',
    'ScrapYellow': 'Item Scrap, Yellow',
    'LunarBadLuck': 'Purity'
}

# Possible stage names
stages = {
    'title': 'Title',
    'lobby': 'Game Lobby',
    'blackbeach': 'Distant Roost',
    'blackbeach2': 'Distant Roost',
    'golemplains': 'Titanic Plains',
    'golemplains2': 'Titanic Plains',
    'foggyswamp': 'Wetland Aspect',
    'goolake': 'Abandoned Aqueduct',
    'frozenwall': 'Rallypoint Delta',
    'wispgraveyard': 'Scorched Acres',
    'dampcave': 'Abyssal Depths',  # May be unused now, changed to dampcavesimple.. but just in case
    'shipgraveyard': "Siren's Call",
    'arena': 'Hidden Realm: Void Fields',
    'bazaar': 'Hidden Realm: Bazaar Between Time',
    'goldshores': 'Hidden Realm: Glided Coast',
    'mysteryspace': 'Hidden Realm: A Moment, Fractured',
    'limbo': 'Hidden Realm: A Moment, Whole',
    'artifactworld': 'Hidden Realm: Artifact World',
    'skymeadow': 'Sky Meadow',
    'splash': 'Splash Screen',
    'moon': 'Moon',
    'outro': 'Outro',
    'dampcavesimple': 'Abyssal Depths',
    'rootjungle': 'Sundered Grove'
}

# These get assigned / updated every time server() is called
server_info = None
server_players = None


async def execute_cmd(channel, command):
    """Sends a custom command to be executed on the server.

    A custom command can be sent to the server that will be executed as if typed into the console. Be careful,
    this command can cause weird side effects and break your entire server!

    :param channel: Channel the command is executed in, used to determine which server.
    :param command: The command to be executed.
    """
    postdict = {
        "@t": datetime.now().isoformat(),
        "@mt": "{Command}",
        "Command": command,
        "Channel": channel
    }
    jsondata = json.dumps(postdict)
    result = requests.post(url=f"http://seq.pyre-bot.com/api/events/raw?clef&apiKey={seq_api}",
                           data=jsondata, headers={"ContentType": "application/vnd.serilog.clef"})


async def server(channel):
    """Checks if the server is running or not.

    Parameters
    ----------
    channel : str
        Chat channel of the server

    Returns
    -------
        Server info if server is online otherwise False.
    """
    for serverdict in server_list:
        if serverdict["commands_channel"] == str(channel) or serverdict["admin_channel"] == str(channel)\
                or serverdict["chat_channel"] == str(channel):
            address = serverdict["server_address"]
            break
    try:
        svr_info = a2s.info(address, 1.0)
        svr_players = a2s.players(address)
        return {"server_info": svr_info, "server_players": svr_players}
    except Exception as e:
        logging.warning(f'[Pyre-Bot:Commands][{datetime.now(tz).strftime(t_fmt)}] Error checking server status: {e}')
        return False


async def server_stop(channel):
    """Issues the disconnect command to stop the server.

    :param channel: Channel the command is executed in, used to determine which server.
    :return: True if the server was stopped, otherwise false.
    """
    if await server(channel):
        await execute_cmd(channel, "disconnect")
        return True
    else:
        return False


async def restart(channel):
    """Issues the commands to restart the server.

    Calls the server_stop() function and then calls the start() function.

    :param channel: Channel the command is executed in, used to determine which server.
    :return: Returns false if unable to restart the server.
    """
    if not await server_stop(channel):
        return False
    await asyncio.sleep(5)
    return await start(channel)


async def start(channel):
    """Issues the host command to start the server.

    :param channel: Channel the command is executed in, used to determine which server.
    :return: Returns false if the server is already running, otherwise true.
    """
    # Starts the server
    if await server(channel):
        return False
    else:
        await execute_cmd(channel, "host 1")
        return True


async def server_logs():
    """Parses over all logs cached and creates the list used to determine which ones to use, removes old logs.

    :return: List of logs that are to be used
    """
    serverlogs_ = os.listdir(logpath)
    serverlogs = []
    today_date = date.today().strftime("%Y%m%d")
    yesterday_date = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
    for log in serverlogs_:
        if len(serverlogs) >= len(server_addresses):  # Stop counting logs after they are all accounted for, save time
            break
        elif log.endswith('-' + today_date + '.log'):
            serverlogs.append(log)
        elif not log.endswith('-' + today_date + '.log.offset')\
                and not log.endswith('-' + yesterday_date + '.log')\
                and not log.endswith('-' + yesterday_date + '.log.offset'):
            try:
                os.remove(log)
            except OSError as e:
                pass
    return serverlogs


async def is_host(ctx):
    """Makes sure the command is ran in an admin Discord channel

    :param ctx: Discord context
    :return: List of admin channels
    """
    return str(ctx.message.channel.id) in admin_channels


async def format_time(time):
    value = timedelta(seconds=int(float(time)))
    total_hours = int(value.total_seconds() // 3600)
    if total_hours < 10:
        total_hours = "0" + str(total_hours)
    total_minutes = int((value.total_seconds() // 60) % 60)
    if total_minutes < 10:
        total_minutes = "0" + str(total_minutes)
    total_seconds = int(value.total_seconds() % 60)
    if total_seconds < 10:
        total_seconds = "0" + str(total_seconds)
    return str(total_hours) + ":" + str(total_minutes) + ":" + str(total_seconds)

# async def server_logs_comprehension_test():
#     serverlogs = []
#     serverlogs = [f for f in os.listdir(logpath)
#                   if f.endswith('-' + datetime.date.today().strftime("%Y%m%d") + '.log')
#                   and len(serverlogs) < len(server_addresses)]
#     return serverlogs
