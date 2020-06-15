import asyncio
import logging
import os

import a2s
import psutil

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
        return False


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
    plugin_dir = (bepinex / 'plugins')
    files = [file.name for file in plugin_dir.glob('**/*') if file.is_file()]
    if 'BotCommands.dll' in files:
        return True
    logging.warning('Unable to find BotCommands.dll!')
    return False


async def restart(ctx):
    if await server_stop():
        await asyncio.sleep(5)
        if await start(ctx):
            return True
    else:
        return False


async def start(ctx):
    # Path of log file, removes before starting
    if os.path.exists(bepinex / "LogOutput.log"):
        try:
            os.remove(bepinex / "LogOutput.log")
        except Exception:
            print('Unable to remove log file')
            return False
    # Path of log offset file, removes before starting
    if os.path.exists(bepinex / "LogOutput.log.offset"):
        try:
            os.remove(bepinex / "LogOutput.log.offset")
        except Exception:
            print('Unable to remove log offset file')
            return False

    # Starts the server
    try:
        os.startfile(ror2ds / "Risk of Rain 2.exe")
        started = True
        await asyncio.sleep(15)
    except Exception:
        logging.error('Error starting the server!' + Exception)
        return False

    # After 15 seconds checks logs to see if server started
    while started is True:
        with open(bepinex / "LogOutput.log") as f:
            for line in f:
                if "Loaded scene lobby" in line:
                    return True
