import json,os,random
script_path = os.path.split(os.path.realpath(__file__))[0]
json_data = open(f"{script_path}/tea.json",encoding="UTF-8").read()
# 解析JSON为字典
tea_dict = json.loads(json_data)
rc = random.choice
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import data,api

def tea(e:GroupMessageEvent):
    msg=str(e.get_message())
    uid=int(e.get_user_id())
    if msg == "泡茉莉":
        kind = rc(list(tea_dict['kinds_of_tea'].items()))
        res:str = rc(tea_dict[kind[1]]['group'])
    else:
        try: 
            kind = tea_dict['kinds_of_tea'][msg]
            res:str = rc(tea_dict[kind]['group'])
        except:
            kind = rc(list(tea_dict['kinds_of_tea'].items()))
            res:str = rc(tea_dict[kind[1]]['group'])
    data.addTeaTimes()
    stamp=api.stamp_def()
    
    query=f"SELECT {data.LOVE},{data.TIMES},{data.LASTTIME},{data.NAME} FROM G5000 where user_id== ? or user_id== 1000"
    args=(uid,)
    rows = data.sql(query,args)
    order = rows[0][1]
    love = rows[1][0]
    lasttime = rows[1][2]
    name = '店长' if rows[1][3] in [0,'0',None] else rows[1][3]
    res=res.replace('_n_','\n').replace('【店长】',name)
    if lasttime != stamp[4]:
        num=random.randint(24,40)
        query=f"update G5000 set {data.LOVE}=?, {data.LASTTIME}=? where user_id== ?"
        args=(love+num,stamp[4],uid,)
        data.sql(query,args)
        lv,nick = api.lv(love+num)
        res = f"[Lv.{lv}/0x{lv:x}-{nick}]\n{res}\n[好感度+{num}|今天的第{order}杯茉莉~]"
    else:
        lv,nick = api.lv(love)
        res = f"[Lv.{lv}/0x{lv:x}-{nick}]\n{res}\n[今天的第{order}杯茉莉~]"
    
    return res