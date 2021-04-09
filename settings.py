from pathlib import Path
import os

# Register your Cog here

COGS=[
    'Cogs.General',
    'Cogs.Base',
]


# Path to Database

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = os.path.join(BASE_DIR,"Database")

XP_PATH = os.path.join(DATABASE_PATH,"XP")
TIMETABLES_PATH = os.path.join(DATABASE_PATH,"Timetables")
MESSAGES_PATH = os.path.join(DATABASE_PATH,"Messages")

# Formula used to map XP and level

# Same as the one used in mee6 bot