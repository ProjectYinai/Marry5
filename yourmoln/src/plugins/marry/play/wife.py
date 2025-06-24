import time,random

rc = random.choice
from nonebot.adapters import Bot, Message
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import data,api

async def roll(bot:Bot, e:GroupMessageEvent) -> Message:
    gm = await api.myGroupMembers(gid=e.group_id)
    cgm=[]
    for i in range(2):
        for i in range(len(gm)):
            if (int(time.time()) - gm[i][2]) > 3600*12:
                break
            if (int(time.time()) - gm[i][2]) < 3600*3:
                cgm += [gm[i]]*4
            elif (int(time.time()) - gm[i][2]) < 3600*6:
                cgm += [gm[i]]*2
            elif (int(time.time()) - gm[i][2]) < 3600*12:
                cgm += [gm[i]]*1
        if len(cgm) == 0:
            gm = await api.myGroupMembers(gid=e.group_id,nc=True)
        else: break

    if str(e.message) == "抽群老婆":
        qid,name,sendtime = rc(cgm)
        img=f"http://q1.qlogo.cn/g?b=qq&nk={str(qid)}&s=100"
        res=[{"type":"reply","data":{"id":str(e.message_id)}},
            {"type":"text","data":{"text":"今天你亲爱的群老婆是："}},
            {"type":"image","data":{"file":img}},
            {"type":"text","data":{"text":f"{"[UP!]" if (int(time.time()) - sendtime) < 3600*3 else ""}【{name}】({qid})哒！" }}]
    elif str(e.message) == "抽群老婆十连":
        res=[{"type":"reply","data":{"id":str(e.message_id)}},
            {"type":"text","data":{"text":"今天你亲爱的群老婆是：\n"}}]+[
            {"type":"text","data":
             {"text":f"{"[UP!]" if (int(time.time()) - (w:=rc(cgm))[2]) < 3600*3 else ""}【{w[1]}】\n"}} for i in range(10)]+[
            {"type":"text","data":{"text":"这十个哒！"}}  
            ]
    return res