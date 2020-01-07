# lol.py
import os
import psutil
import time
from dotenv import load_dotenv
import random
import cassiopeia as cass
from cassiopeia import Summoner

cass.set_riot_api_key("RGAPI-1eb42454-70d3-42d2-a0a7-63261fbff325")  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")

kalturi = Summoner(name="Kalturi")
good_with = kalturi.champion_masteries.filter(lambda cm: cm.level >= 6)
print([cm.champion.name for cm in good_with])
