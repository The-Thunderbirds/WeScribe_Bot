#discord
from datetime import datetime
from discord.ext import commands,tasks
import discord
from discord.utils import get
import os,asyncio,random
from secret import BOT_ANNOUNCEMENTS, CR_NAME, GUILD
from __constants import YEAR,LIKE_EMOJI,COLORS,CONVERT,DISLIKE_EMOJI
from settings import TIMETABLES_PATH
from Cogs.Embeds import Embeds
from Utils.TimetableUtil import TimetableUtil
from Utils.MessageUtil import MessageUtil


class Notifier(commands.Cog,name="Notifier Cog"):
    def __init__(self,bot):
        self.bot=bot
        self.ClassNotifier.start()
        self.EventsNotifier.start()

    def validYear(self,year:str):
        return (year in YEAR)
    

    @commands.command("timetable-get",help="Returns timetable of the specified year.")
    @commands.cooldown(3,30,commands.BucketType.user)
    async def TimetableGet(self,ctx,year:str):
        if(not self.validYear(year)):
            await ctx.send(f"<@{ctx.author.id}> Enter a valid year.(Case-sensitive)")
            return
        year+=".csv"
        PATH=os.path.join(TIMETABLES_PATH,str(ctx.guild.id),year)
        if(os.path.isfile(PATH)):
            await ctx.send(file=discord.File(PATH))
        else:
            await ctx.send(f"<@{ctx.author.id}> Couldn't find the requested year's timetable. Request the batch CR to put up one.")

    @commands.command("timetable-put",help="Helps to put up a timetable.")
    @commands.cooldown(3,30,commands.BucketType.user)
    @commands.has_role(CR_NAME)
    async def TimetablePut(self,ctx,year:str):
        if(not self.validYear(year)):
            await ctx.send(f"<@{ctx.author.id}> Enter a valid year.(Case-sensitive)")
            return
        
        def check(msg):
            if(msg.author==ctx.author and msg.channel==ctx.channel):
                if (msg.content.lower()=="n" or len(msg.attachments)>0):
                    return True
                return False
            else:
                return False
        
        def checkBool(msg):
            if(msg.author==ctx.author and msg.channel==ctx.channel):
                if(msg.content.lower()=='y' or msg.content.lower()=='n'):
                    return True
            return False

        if(os.path.isfile(os.path.join(TIMETABLES_PATH,str(ctx.guild.id),f"{year}.csv"))):
            try:
                await ctx.send("Timetable already exists. Enter 'y' to overwrite or 'n' to cancel.")
                confirm=await self.bot.wait_for('message',check=checkBool,timeout=30)
                if(confirm.content.lower()=='n'):
                    await confirm.add_reaction(LIKE_EMOJI)
                    await ctx.send("<@{ctx.member.id}> Cool.")
                    return
                
            except asyncio.exceptions.TimeoutError:
                await ctx.send(f"<@{ctx.author.id}> Sorry, you didn't reply within 30sec. Aborted.")
                return

        try:
            await ctx.send("Upload the file within 60 sec. Enter 'n' (without quotes) to cancel.")
            msg=await self.bot.wait_for('message',check=check,timeout=60)
            if(msg.content.lower()=="n"):
                await msg.add_reaction(LIKE_EMOJI)
                await ctx.send("<@{ctx.author.id}> Cool.")
                return
            
            attachment=msg.attachments[0]
            link=attachment.url
            TimetableUtil.StoreCSV(ctx.guild.id,year,link)
            await msg.add_reaction(LIKE_EMOJI)

        except asyncio.exceptions.TimeoutError:
            await ctx.send(f"<@{ctx.author.id}> Sorry, you didn't upload any file within 60sec. Aborted.")


    @commands.command("live",help="Notifies the specified year students about the session.")
    @commands.cooldown(1,30,commands.BucketType.user)
    async def Live(self,ctx,year:str,*tags):
        if(not self.validYear(year)):
            await ctx.send("Enter a valid year.")
            return
        
        embed=Embeds.Live(ctx.author,get(ctx.guild.roles,name=year),random.choice(COLORS),tags)
        msg=await get(ctx.guild.channels,id=int(BOT_ANNOUNCEMENTS)).send(embed=embed)
        MessageUtil.LinkMessage(ctx.guild.id,msg.id,ctx.author.id)
        await ctx.message.add_reaction(LIKE_EMOJI)
        await msg.add_reaction(LIKE_EMOJI)
        await msg.add_reaction(DISLIKE_EMOJI)

    #every 15 min
    @tasks.loop(minutes=15)
    async def ClassNotifier(self):
        guild=get(self.bot.guilds,id=int(GUILD))
        announcements=get(guild.channels,id=int(BOT_ANNOUNCEMENTS))
        for i in range(1,6):
            specific_year=TimetableUtil.GetJSON(guild.id,f"{CONVERT[i]}Year")
            role=get(guild.roles,name=f"{CONVERT[i]}Year")
            if specific_year is not None:
                for start_time in specific_year:
                    delta=TimetableUtil.TimeCompare(start_time)
                    print(delta)
                    if(delta>=15*60 and delta<30*60):
                        await announcements.send(f"<@&{role.id}> You have an upcoming {specific_year[start_time]['subject']} lecture at {start_time}.")


    @ClassNotifier.before_loop
    async def ClassNotifierBefore(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=15)
    async def EventsNotifier(self):
        pass

    @EventsNotifier.before_loop
    async def EventsNotifierBefore(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Notifier(bot))