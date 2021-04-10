#discord
from discord.ext import commands
from Cogs.Embeds import Embeds
import random
from __constants import COLORS
from Utils.XPutils import XPUtil
from Utils.XPCard import XPCard
import aiohttp
from io import BytesIO
import discord

class XP(commands.Cog,name="XP Cog"):
    def __init__(self,bot):
        self.bot=bot

    def GetLvlXP(self,currentLvl:int):
        if(currentLvl<0):
            return 0
        return (5*currentLvl*currentLvl)+(50*currentLvl)+100

    @commands.command("xp",help="Returns your xp details.")
    @commands.cooldown(3,30,commands.BucketType.user)
    async def XPGet(self,ctx):
        level,xp=XPUtil.GetXP(ctx.guild.id,ctx.message.author.id)
        embed=Embeds.XPEmbed(ctx,level,xp,self.GetLvlXP(level+1),random.choice(COLORS))
        await ctx.send(embed=embed)

    @commands.command("xp-card",help="Returns your xp details as a card.")
    @commands.cooldown(3,30,commands.BucketType.user)
    async def XPCard(self,ctx):
        if ctx.author.avatar_url == ctx.author.default_avatar_url:
            await ctx.send(f"<@{ctx.author.id}> Please put up a DP to get an XP card.")
            return
        level,xp=XPUtil.GetXP(ctx.guild.id,ctx.message.author.id)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{ctx.author.avatar_url_as(size=128)}') as response:
                profile_bytes=await response.read()
        buff=XPCard.BuildCard(str(ctx.author),level,xp,self.GetLvlXP(level+1),BytesIO(profile_bytes))
        await ctx.send(file=discord.File(fp=buff,filename=f"{ctx.author.name}.png"))
        

def setup(bot):
    bot.add_cog(XP(bot))