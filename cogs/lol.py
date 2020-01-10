import os
import psutil
import asyncio
import discord
from discord.ext import commands
import cassiopeia as cass
from cassiopeia import Summoner


class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    # Get Summoner information
    @commands.command(name='summoner')
    async def summoner(self, ctx, arg):
        summoner = Summoner(name=arg)
        mastered = summoner.champion_masteries.filter(lambda cm: cm.level >= 6)
        await ctx.send([cm.champion.name for cm in mastered])


def setup(bot):
    bot.add_cog(Lol(bot))
