import json,os
from pathlib import Path
from settings import TIMETABLES_PATH
from datetime import date, datetime,timedelta
import requests

class TimetableUtil:
    def __init__(self):
        pass

    def init(guild_id:int):
        guild_id=str(guild_id)
        if not os.path.isdir(os.path.join(TIMETABLES_PATH,guild_id)):
            os.mkdir(os.path.join(TIMETABLES_PATH,guild_id))
            print(f"Timetables db not found for {guild_id}. Created one.")

    def StoreCSV(guild_id:int,year:str,link:str):
        guild_id=str(guild_id)
        matter=requests.get(link).content
        with open(os.path.join(TIMETABLES_PATH,guild_id,year+".csv"),'wb+') as f:
            f.write(matter)
        TimetableUtil.CSVtoJSON(int(guild_id),year)


    def CSVtoJSON(guild_id:int,year:str):
        guild_id=str(guild_id)
        with open(os.path.join(TIMETABLES_PATH,guild_id,year+".csv"),'rb+') as f:
            lines=f.read().decode('utf-16').split('\n')
        result={}
        for line in lines:
            data=line.split(',')
            if(len(data)==3):
                result[data[0]]={'year':year,'till':data[1],'subject':data[2]}

        with open(os.path.join(TIMETABLES_PATH,guild_id,year+".json"),'w+') as f:
            json.dump(result,f)

    def GetCSV(guild_id:int,year:str):
        guild_id=str(guild_id)
        path=os.path.join(TIMETABLES_PATH,guild_id,year+".csv")
        if os.path.exists(path):
            return path
        return None

    def GetJSON(guild_id:int,year:str):
        guild_id=str(guild_id)
        path=os.path.join(TIMETABLES_PATH,guild_id,year+'.json')
        if os.path.exists(path):
            with open(path,'r+') as f:
                data=json.load(f)
            return data
        return None


    def TimeCompare(time1:str):
        time2=str(datetime.now().time())
        time2=time2.split('.')[0]

        sec=lambda time:sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":"))) 

        return sec(time1)-sec(time2)