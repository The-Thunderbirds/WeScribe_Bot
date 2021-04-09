import os
from discord.ext import commands
from discord import Intents
from settings import COGS
from secret import TOKEN


def main():
    
    intents=Intents.default()
    intents.members=True
    
    bot=commands.Bot(command_prefix="!",intents=intents)
    
    for PATH in COGS:
        bot.load_extension(PATH)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()