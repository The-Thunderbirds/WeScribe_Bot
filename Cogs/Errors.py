#discord
from discord.ext import commands
from discord.utils import get
from discord.channel import DMChannel
#secret
from secret import LOG,GUILD


class Errors(commands.Cog,name="Errors Cog"):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.errors.CheckFailure) or isinstance(error, commands.errors.UserInputError) or isinstance(error,commands.errors.CommandNotFound) or isinstance(error,commands.errors.CommandOnCooldown):
            await ctx.send(f"<@{ctx.author.id}> {error}")
        else:
            await ctx.send("Encountered some unexpected error. Notified Admins.")
            log_channel=get(get(self.bot.guilds,id=int(GUILD)).channels,id=int(LOG))
            summary=f"Error :\n{error}\nFor the message :\n{ctx.message.content}\nUsed by :\n{ctx.author}"
            await log_channel.send(summary)

def setup(bot):
    bot.add_cog(Errors(bot))