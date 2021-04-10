import os,json
from settings import XP_PATH
from pathlib import Path

class XPUtil:
    def __init__(self):
        pass

    def init(guild_id:int):
        guild_id=str(guild_id)
        if not Path(os.path.join(XP_PATH,f'{guild_id}.json')).is_file():
            with open(os.path.join(XP_PATH,f'{guild_id}.json'),'w+') as f:
                json.dump({},f)
            print(f"XP db not found for {guild_id}. Created one.")


    def GetLvlXP(currentLvl:int):
        if(currentLvl<0):
            return 0
        return (5*currentLvl*currentLvl)+(50*currentLvl)+100

    def AddNewUser(guild_id:int,member_id:int):
        guild_id=str(guild_id)
        member_id=str(member_id)

        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        data[member_id]={'xp':0,'level':0}
        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'w+') as f:
            json.dump(data,f)
        print("Created New User:XP")

    def IncreaseXP(guild_id:int,member_id:int,xp:int,level:int):
        # accordingly increases level if required   (Returns true if leveled up)
        guild_id=str(guild_id)
        member_id=str(member_id)

        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        
        ok=False
        if member_id in data:
            data[member_id]['xp']+=xp
        
            # add upper limit of levels, i.e. if level is max possible then ok=false
            if(data[member_id]['xp']>=XPUtil.GetLvlXP(level+1)):
                data[member_id]['level']+=1
                ok=True
        else:
            data[member_id]={'xp':xp,'level':level}

        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'w+') as f:
            json.dump(data,f)

        return ok
        
    
    def DecreaseXP(guild_id:int,member_id:int,xp:int,level:int):
        # accordingly decrease level
        guild_id=str(guild_id)
        member_id=str(member_id)

        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        
        ok=False
        if member_id in data:
            data[member_id]['xp']-=xp
        
            if(level and data[member_id]['xp']<XPUtil.GetLvlXP(level-1)):
                data[member_id]['level']=max(0,data[member_id]['level']-1)
                ok=True
        else:
            data[member_id]={'xp':xp,'level':level}

        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'w+') as f:
            json.dump(data,f)

        return ok

    def GetXP(guild_id:int,member_id:int):
        # Returns both xp and level  (level,xp)
        guild_id=str(guild_id)
        member_id=str(member_id)
        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        
        if member_id in data:
            return (data[member_id]['level'],data[member_id]['xp'])
        
        return (0,0)

    def RemoveUser(guild_id:int,member_id:int):
        guild_id=str(guild_id)
        member_id=str(member_id)

        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'r+') as f:
            data=json.load(f)
        
        if member_id in data:
            data[member_id]={'xp':0,'level':0}
        
        with open(os.path.join(XP_PATH,f"{guild_id}.json"),'w+') as f:
            json.dump(data,f)
        print("Removed existing user:XP")