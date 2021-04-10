from discord.ext import commands
from discord.utils import get
from __constants import YEAR,LIKE_EMOJI,COLORS
from Cogs.Embeds import Embeds
import random


class General(commands.Cog,name="General Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    def validYear(self,year):
        return (year in YEAR)

    @commands.command("years",help="Returns list of years (batches) available for usage.")
    async def Years(self,ctx):
        tags=YEAR
        tags.remove('no-tag')
        embed=Embeds.ListEmbed("Available year tags",tags,random.choice(COLORS))
        await ctx.send(embed=embed)

    @commands.command("assign",help="Allows you to assign to a particular year.")
    async def assign(self,ctx,year):
        if not self.validYear(year):
            await ctx.send(f"<@{ctx.author.id}> Enter a valid Year. (Case sensitive)")
            return
        await ctx.author.add_roles(get(ctx.guild.roles,name=year))
        await ctx.message.add_reaction(LIKE_EMOJI)


def setup(bot):
    bot.add_cog(General(bot))