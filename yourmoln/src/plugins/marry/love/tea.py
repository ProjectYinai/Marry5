import json,os,random
script_path = os.path.split(os.path.realpath(__file__))[0]
json_data = open(f"{script_path}/tea.json",encoding="UTF-8").read()
# 解析JSON为字典
tea_dict = json.loads(json_data)
rc = random.choice
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import data,api

async def tea(bot:Bot, e:GroupMessageEvent) -> str:
    """这里是茉莉给店长泡茶的函数"""
    msg=str(e.get_message())
    uid=int(e.get_user_id())
    if msg == "泡茉莉":
        kind = rc(list(tea_dict['kinds_of_tea'].items()))
        res:str = rc(tea_dict[kind[1]]['group'])
        msg = "泡"+tea_dict[kind[1]]['type']
    else:
        try: 
            kind = (0,tea_dict['kinds_of_tea'][msg])
            res:str = rc(tea_dict[kind[1]]['group'])
        except:
            kind = rc(list(tea_dict['kinds_of_tea'].items()))
            res:str = rc(tea_dict[kind[1]]['group'])
            msg = "泡"+tea_dict[kind[1]]['type']
    data.addTeaTimes()
    stamp=api.stamp_def()
    
    query=f"SELECT love,etea,teatime,name FROM user where uid== ? or uid== 1"
    args=(uid,)
    rows = data.sql(query,args)
    order = rows[0][1]
    love = rows[1][0]
    lasttime = rows[1][2]
    name = '店长' if rows[1][3] in [0,'0',None] else rows[1][3]
    res=res.replace('_n_','\n').replace('【店长】',name)
    fs = await api.myfriends()
    if lasttime != stamp[4]:
        num=random.randint(24,40)
        query=f"update user set love=love+?, teatime=?, etea=etea+1 where uid== ?"
        args=(num,stamp[4],uid,)
        data.sql(query,args)
        lv,nick = api.lv(love+num,name)
        res = f"[Lv.{lv}-{nick}]\n{res}\n[好感度+{num}|今天的第{order}杯茉莉~]"
        if (num >= (40+(16*(50-(lv if lv < 100 else 100))*0.01)) or int(order) in [39] ) and uid in fs :
            voice=[{"type": "record","data": {"file": f"file:///{script_path}/voice/{msg}.wav"}}]
            try: await bot.send_private_msg(user_id=uid,message=voice)
            except Exception as e: print(e)
    else:
        query=f"update user set etea=etea+1 where uid== ?"
        args=(uid,)
        data.sql(query,args)
        lv,nick = api.lv(love,name)
        res = f"[Lv.{lv}-{nick}]\n{res}\n[今天的第{order}杯茉莉~]"
    if uid in fs:
        pmsg=rc(tea_dict[kind[1]]['message']["normalN"])[0]
        pmsg=pmsg.replace('_n_','\n').replace('【店长】',name)
        m=[{"type":"text","data":{"text":pmsg}}]
        await bot.send_private_msg(user_id=uid,message=m)
    return res