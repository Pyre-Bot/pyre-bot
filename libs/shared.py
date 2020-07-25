import asyncio  # NEEDED?
import logging  # NEEDED?
import os  # NEEDED?

import a2s
import psutil  # NEEDED?

from config.config import *

import json
import requests
import datetime

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

# Used to determine which server stats need updating
channels = {
    'Server1': {'admin': 670373469845979136,
                'commands': 665998238171660320,
                'chat': 667473663343198220},
    'Server2': {'admin': 671917010422333460,
                'commands': 671921930873602099,
                'chat': 671918498531770378},
    'Server3': {'admin': 672682539390992384,
                'commands': 672682345089859654,
                'chat': 672682313003565057},
    'Server4': {'admin': 672940159091867648,
                'commands': 672939900600975362,
                'chat': 672939927507435533}
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
    'GainArmor': 'Jade Elephant',
    'Sawmerang': 'Sawmerang',
    'Recycler': 'Recycler'
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
    'RepulsionArmorPlate': 'Repulsion Armor Plate',
    'SquidTurret': 'Squid Polyp',
    'DeathMark': 'Death Mark',
    'InterstellarDeskPlant': 'Interstellar Desk Plant',
    'AncestralIncubator': 'Ancestral Incubator'
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
    'dampcave': 'Abyssal Depths',
    'shipgraveyard': "Siren's Call",
    'arena': 'Hidden Realm: Void Fields',
    'bazaar': 'Hidden Realm: Bazaar Between Time',
    'goldshores': 'Hidden Realm: Glided Coast',
    'mysteryspace': 'Hidden Realm: A Moment, Fractured',
    'limbo': 'Hidden Realm: A Moment, Whole',
    'artifactworld': 'Hidden Realm: Artifact World',
    'skymeadow': 'Sky Meadow'
}

# These get assigned / updated every time server() is called
server_info = ''
server_players = ''


async def execute_cmd(channel, command):
    postdict = {
        "@t": datetime.datetime.now().isoformat(),
        "@mt": "{Command}",
        "Command": command,
        "Channel": channel
    }
    jsondata = json.dumps(postdict)
    # print(jsondata)  # DEBUG
    result = requests.post(url=f"http://seq.pyre-bot.com/api/events/raw?clef&apiKey={seq_api}",
                           data=jsondata, headers={"ContentType": "application/vnd.serilog.clef"})
    # print(result.text)  # DEBUG


async def server(channel):
    """Checks if the server is running or not.

    This check is used by many of the commands and functions within the bot. It checks the steam server list to
    determine if the server is running.

    Returns:
        Boolean: True if the server is running, otherwise false.


    """
    for serverdict in server_list:
        if serverdict["commands_channel"] == str(channel) or serverdict["admin_channel"] == str(channel):
            address = serverdict["server_address"]
            break
    try:
        server_info = a2s.info(address, 1.0)
        server_players = a2s.players(address)
        return {"server_info": server_info, "server_players": server_players}
    except Exception as e:
        print(str(e))  # DEBUG
        return False


# TODO: Change to pass command disconnect
async def server_stop(channel):
    """Stops the server.

    Returns:
        Boolean: True if the server was stopped, otherwise false.


    """
    # Stops the server
    if await server(channel):
        await execute_cmd(channel, "disconnect")
        return True
    else:
        return False


async def restart(channel):
    """Used to restart the server.

    Calls the server_stop() function and then calls the start() function.

    Returns:
        Boolean: True if started successfully, otherwise false.


    """
    if not await server_stop(channel):
        return False
    return await start(channel)


async def start(channel):
    """Starts the server

    Checks for the existence of log files and removes them prior to server restart. Once the files are removed
    it starts the server.

    Returns:
        Boolean: True if started successfully, otherwise false.


    """
    # Starts the server
    if await server(channel):
        return False
    else:
        await execute_cmd(channel, "host 1")
        return True


async def server_logs():
    serverlogs_ = os.listdir(logpath)
    serverlogs = []
    today_date = datetime.date.today().strftime("%Y%m%d")
    for log in serverlogs_:
        if log.endswith('-' + today_date + '.log'):
            serverlogs.append(log)

    return serverlogs
