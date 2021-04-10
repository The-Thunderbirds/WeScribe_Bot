import os
from dotenv import load_dotenv

BASEDIR=os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASEDIR,'.env'))

TOKEN=os.getenv("DISCORD_TOKEN")
GUILD=os.getenv("GUILD")
STUDENT=os.getenv("STUDENT")
CR=os.getenv("CR")
CR_NAME=os.getenv("CR_NAME")
LOG=os.getenv("LOG")
BOT_ANNOUNCEMENTS=os.getenv("BOT_ANNOUNCEMENTS")