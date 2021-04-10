from Utils.MessageUtil import MessageUtil
from Utils.XPutils import XPUtil
from Utils.TimetableUtil import TimetableUtil


class MainUtil:
    def __init__(self):
        pass
    def init(guild_id:int):
        MessageUtil.init(guild_id)
        XPUtil.init(guild_id)
        TimetableUtil.init(guild_id)