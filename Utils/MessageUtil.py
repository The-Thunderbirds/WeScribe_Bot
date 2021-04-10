import os,json
from settings import MESSAGES_PATH
from pathlib import Path

class MessageUtil:
    def __init__(self):
        pass

    def init(guild_id:int):
        guild_id=str(guild_id)
        if not Path(os.path.join(MESSAGES_PATH,f'{guild_id}.json')).is_file():
            with open(os.path.join(MESSAGES_PATH,f'{guild_id}.json'),'w+') as f:
                json.dump({},f)
            print(f"Message db not found for {guild_id}. Created one.")

    def LinkMessage(guild_id:int,message_id:int,member_id:int):
        guild_id=str(guild_id)
        message_id=str(message_id)
        member_id=str(member_id)

        with open(os.path.join(MESSAGES_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        data[message_id]=member_id
        with open(os.path.join(MESSAGES_PATH,f"{guild_id}.json"),'w+') as f:
            json.dump(data,f)

    def UnLinkMessage(guild_id:int,message_id:int,member_id:int):
        guild_id=str(guild_id)
        message_id=str(message_id)
        member_id=str(member_id)

        with open(os.path.join(MESSAGES_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        data.pop(message_id,None)
        with open(os.path.join(MESSAGES_PATH,f"{guild_id}.json"),'w+') as f:
            json.dump(data,f)

    def GetMessageMember(guild_id:int,message_id:int):
        guild_id=str(guild_id)
        message_id=str(message_id)

        with open(os.path.join(MESSAGES_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        
        if message_id in data:
            return int(data[message_id])
        
        return None