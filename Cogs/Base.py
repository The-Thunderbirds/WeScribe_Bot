#discord
from discord.ext import commands
from discord.utils import get
from discord import Activity,ActivityType
#secret
from secret import GUILD,STUDENT
from __constants import LEVEL_COLORS

from Utils.MainUtil import MainUtil
from Utils.XPutils import XPUtil

class Base(commands.Cog,name="Base Cog"):
    def __init__(self,bot):
        self.bot=bot
    
    async def CreateLevels(self):
        existing_roles=await get(self.bot.guilds,id=int(GUILD)).fetch_roles()
        existing_roles=[role.name for role in existing_roles]
        levels=len(LEVEL_COLORS)
        for level in range(0,levels):
            if(f"Level {level}" not in existing_roles):
                await get(self.bot.guilds,id=int(GUILD)).create_role(name=f"Level {level}",colour=LEVEL_COLORS[level])
                print(f"Created Level {level} role")


    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            await member.add_roles(get(get(self.bot.guilds,id=int(GUILD)).roles,id=int(STUDENT)))        
            level0=get(get(self.bot.guilds,id=int(GUILD)).roles,name="Level 0")
            await member.add_roles(level0)
            XPUtil.AddNewUser(member.guild.id,member.id)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name="!help"))
        for guild in self.bot.guilds:
            MainUtil.init(guild.id)
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.CreateLevels()

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        MainUtil.init(guild.id)

def setup(bot):
    bot.add_cog(Base(bot))