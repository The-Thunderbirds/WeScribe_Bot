#discord
from discord.ext import commands,tasks
from discord.utils import get
from __constants import XP,CONTENT_TYPES,COLORS,LIKE_EMOJI,YEAR,DISLIKE_EMOJI
from Cogs.Embeds import Embeds
import random
from Utils.XPutils import XPUtil
from secret import BOT_ANNOUNCEMENTS
import asyncio
from Utils.RegexUtil import Regex
from Utils.XPutils import XPUtil
from Utils.MessageUtil import MessageUtil

class Share(commands.Cog,name="XP Cog"):
    def __init__(self,bot):
        self.bot=bot

    def validYear(self,year:str):
        return (year in YEAR)

    def validContent(self,content_type:str):
        return (content_type in CONTENT_TYPES)
    
    def extract_tags(self,sem:str):
        pass


    async def IncreaseXP(self,guild_id:int,associated_user:int,xp):
        associated_user_level,_=XPUtil.GetXP(guild_id,associated_user)
        ok=XPUtil.IncreaseXP(guild_id,associated_user,xp,associated_user_level)
        if ok:
            oldLevel=get(get(self.bot.guilds,id=guild_id).roles,name=f"Level {associated_user_level}")
            newLevel=get(get(self.bot.guilds,id=guild_id).roles,name=f"Level {associated_user_level+1}")
            user=get(get(self.bot.guilds,id=guild_id).members,id=int(associated_user))
            await user.add_roles(newLevel)
            await user.remove_roles(oldLevel)
            embed=Embeds.LevelUp(user,associated_user_level+1,XPUtil.GetXP(user.guild.id,associated_user)[1],random.choice(COLORS))
            await get(user.guild.channels,id=int(BOT_ANNOUNCEMENTS)).send(embed=embed)

    async def DecreaseXP(self,guild_id:int,associated_user:int,xp):
        associated_user_level,_=XPUtil.GetXP(guild_id,associated_user)
        ok=XPUtil.DecreaseXP(guild_id,associated_user,xp,associated_user_level)
        if ok:
            oldLevel=get(get(self.bot.guilds,id=guild_id).roles,name=f"Level {associated_user_level}")
            newLevel=get(get(self.bot.guilds,id=guild_id).roles,name=f"Level {associated_user_level-1}")
            user=get(get(self.bot.guilds,id=guild_id).members,id=int(associated_user))
            await user.add_roles(newLevel)
            await user.remove_roles(oldLevel)
            embed=Embeds.LevelDown(user,max(associated_user_level-1,0),XPUtil.GetXP(user.guild.id,associated_user)[1],random.choice(COLORS))
            await get(user.guild.channels,id=int(BOT_ANNOUNCEMENTS)).send(embed=embed)


    @commands.command("share",help="Allows you to share any useful material (file/link/wescribe).")
    @commands.cooldown(3,30,commands.BucketType.user)
    async def Share(self,ctx,content_type:str,year:str,*extratags):

        content_type=content_type.lower()
        xp_addup=0
        
        if(not self.validContent(content_type)):
            await ctx.send(f"<@{ctx.author.id}> Enter a valid content type. Only file/link/wescribe are allowed.")
            return

        if(not self.validYear(year)):
            await ctx.send(f"<@{ctx.author.id}> Enter a valid year. (Case-Sensitive)")
            return

        if(content_type=='file'):
            await ctx.send(f"<@{ctx.author.id}> Upload the file within 60 sec. Enter 'n' (without quotes) to cancel.")

            def check(msg):
                if(msg.author==ctx.author and msg.channel==ctx.channel):
                    if (msg.content.lower()=="n" or len(msg.attachments)>0):
                        return True
                return False 
            
            try:
                msg=await self.bot.wait_for('message',check=check,timeout=60)
                if(msg.content=="n"):
                    await msg.add_reaction(LIKE_EMOJI)
                    return
                attachment=msg.attachments[0]
                await msg.add_reaction(LIKE_EMOJI)
                embed=Embeds.NewFile(ctx,get(ctx.guild.roles,name=year).id,str(attachment.filename),str(attachment.url),extratags)
            except asyncio.exceptions.TimeoutError:
                await ctx.send(f"<@{ctx.author.id}> Sorry, you didn't upload any file within 60sec. Aborted.")
                return

        elif(content_type=='link'):
            await ctx.send(f"<@{ctx.author.id}> Send URL within 60 sec. Enter 'n' (without quotes) to cancel.")

            def check(msg):
                if(msg.author==ctx.author and msg.channel==ctx.channel):
                    if (msg.content.lower()=="n" or Regex.ValidURL(msg.content)):
                        return True
                return False 
            
            try:
                msg=await self.bot.wait_for('message',check=check,timeout=60)
                if(msg.content=="n"):
                    await msg.add_reaction(LIKE_EMOJI)
                    return
                await msg.add_reaction(LIKE_EMOJI)
                url=msg.content
                embed=Embeds.NewLink(ctx,get(ctx.guild.roles,name=year).id,url,extratags)
            except asyncio.exceptions.TimeoutError:
                await ctx.send(f"<@{ctx.author.id}> Sorry, you didn't send any valid url within 60 sec. Aborted.")
                return

        elif(content_type=='wescribe'):
            await ctx.send(f"<@{ctx.author.id}> Send your WeScribe note URL within 60 sec. Enter 'n' (without quotes) to cancel.")

            def check(msg):
                if(msg.author==ctx.author and msg.channel==ctx.channel):
                    if (msg.content.lower()=="n" or Regex.ValidURL(msg.content)):
                        return True
                return False 
            
            try:
                msg=await self.bot.wait_for('message',check=check,timeout=60)
                if(msg.content=="n"):
                    await msg.add_reaction(LIKE_EMOJI)
                    return
                await msg.add_reaction(LIKE_EMOJI)
                url=msg.content
                embed=Embeds.NewWeScribeNote(ctx,get(ctx.guild.roles,name=year).id,url,extratags)
            except asyncio.exceptions.TimeoutError:
                await ctx.send(f"<@{ctx.author.id}> Sorry, you didn't send any valid WeScribe note within 60 sec. Aborted.")
                return
        
        msg=await get(ctx.guild.channels,id=int(BOT_ANNOUNCEMENTS)).send(embed=embed)
        await msg.add_reaction(LIKE_EMOJI)
        await msg.add_reaction(DISLIKE_EMOJI)

        if(len(extratags)):
            xp_addup+=XP['tag']['share'][content_type]
        else:
            xp_addup+=XP['no-tag']['share']
        
        await self.IncreaseXP(ctx.guild.id,ctx.author.id,xp_addup)
        MessageUtil.LinkMessage(ctx.guild.id,msg.id,ctx.author.id)


    @commands.command("get-material")
    async def GetMaterial(self,ctx,year:str):
        pass


    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        if(user.bot or not (reaction.emoji==LIKE_EMOJI or reaction.emoji==DISLIKE_EMOJI)):
            return
        associated_user=MessageUtil.GetMessageMember(user.guild.id,reaction.message.id)

        if(associated_user is None or associated_user==user.id):
            return
        if reaction.emoji==LIKE_EMOJI:
            await self.IncreaseXP(reaction.message.guild.id,associated_user,XP['like'])
        else:
            await self.IncreaseXP(reaction.message.guild.id,associated_user,XP['dislike'])


    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction,user):
        if(user.bot or not (reaction.emoji==LIKE_EMOJI or reaction.emoji==DISLIKE_EMOJI)):
            return
        associated_user=MessageUtil.GetMessageMember(user.guild.id,reaction.message.id)
        if(associated_user is None or associated_user==user.id):
            return
        
        if reaction.emoji==LIKE_EMOJI:
            await self.DecreaseXP(reaction.message.guild.id,associated_user,XP['like'])
        else:
            await self.DecreaseXP(reaction.message.guild.id,associated_user,XP['dislike'])

def setup(bot):
    bot.add_cog(Share(bot))