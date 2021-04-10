from discord import Embed

class Embeds:
    def __init__(self):
        pass

    def ListEmbed(title:str,content_list:list,color:int):
        description=','.join(content_list)
        embed=Embed(title=title,description=description,color=color)
        embed.set_footer(text="All are Case-sensitive")
        return embed
    
    def TagEmbed(title:str,content:dict,color:int):
        embed=Embed(title=title,color=color)
        for chapter in content:
           embed.add_field(name=chapter,value=','.join([tag for tag in content[chapter]]))
        embed.set_footer(text="Only for better classification, the above representation is used.")
        return embed

    def XPEmbed(ctx,level:int,xp:int,next_level_xp:int,color:int):
        embed=Embed(title=f"**Hey {ctx.message.author}!**",description="Here below are your stats.",color=color)
        embed.add_field(name="Current Level",value=level)
        embed.add_field(name="Current XP",value=f"{xp}")
        embed.add_field(name="Next Level XP",value=next_level_xp)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text=f"You need { next_level_xp-xp } more XP to level up! Keep going!")
        return embed
    
    def NewFile(ctx,role,name:str,link:str,tags):
        embed=Embed(title="New File",description=f"<@{ctx.author.id}> Shared a new file for <@&{role}>.\nContent : [{name}]({link})")
        embed.add_field(name="Tags",value=tags)
        embed.set_footer(text="You can like or dis-like to support this.")
        return embed
    
    def NewLink(ctx,role,link:str,tags):
        embed=Embed(title="New Link",description=f"<@{ctx.author.id}> Shared a new link for <@&{role}>.\nContent : {link}")
        embed.add_field(name="Tags",value=tags)
        embed.set_footer(text="You can like or dis-like to support this.")
        return embed
    
    def LevelUp(author,level,xp,color):
        embed=Embed(title="Level Up!",description=f"<@{author.id}> Congratulations! You have level up!",color=color)
        embed.add_field(name="Current Level",value=level)
        embed.add_field(name="Current XP",value=xp)
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text="Your role has been updated.")
        return embed
    
    def LevelDown(author,level,xp,color):
        embed=Embed(title="Sorry, Level Down!",description=f"<@{author.id}> You got down by a level!",color=color)
        embed.add_field(name="Current Level",value=level)
        embed.add_field(name="Current XP",value=xp)
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text="Your role has been updated.")
        return embed
    
    def Live(author,role,color,tags):
        embed=Embed(title="Live Alert!",description=f'<@{author.id}> has started a session! <@&{role.id}> You might find it useful.',color=color)
        embed.add_field(name="Tags",value=tags)
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text=f"You can DM author to get the link.")
        return embed
    
    def NewWeScribeNote(ctx,role,link:str,tags):
        embed=Embed(title="New WeScribe Note",description=f"<@{ctx.author.id}> Shared a new WeScribe note for <@&{role}>.\nContent : {link}")
        embed.add_field(name="Tags",value=tags)
        embed.set_footer(text="You can like or dis-like to support this.")
        return embed