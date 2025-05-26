import json,os,random
from datetime import datetime
script_path = os.path.split(os.path.realpath(__file__))[0]
json_data = open(f"{script_path}/hi.json",encoding="UTF-8").read()
# 解析JSON为字典
greeting_dict = json.loads(json_data)
rc = random.choice

from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters import Bot
import data,api
def refresh(uid:int,k=0):
    """刷新问好时间"""
    if k==0:
        day = api.stamp_def()[4]
        query = f"UPDATE G5000 SET b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0, b7 = 0, b8 = 0, b9 = 0, b10 = 0, {data.HILASTTIME} = ?\
                WHERE user_id = ? AND {data.HILASTTIME} != ?;"
        args = (day,uid,day)
    else:#强制刷新
        day = api.stamp_def()[4]
        query = f"UPDATE G5000 SET b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0, b7 = 0, b8 = 0, b9 = 0, b10 = 0, {data.HILASTTIME} = 0\
                WHERE user_id = ?;"
        args = (uid,)
    data.sql(query,args)
def get_current_greeting_types():
    """获取当前时间段可用的问候类型列表"""
    current_hour = datetime.now().hour
    available_types = []
    
    for greeting in greeting_dict.values():
        if current_hour in greeting['range']:
            available_types.append(f"[{greeting['type']}]")
            available_types.append("和")
    return available_types[:-1]

async def hi(bot:Bot, e:GroupMessageEvent):
    msg=str(e.get_message())
    uid=int(e.get_user_id())
    refresh(uid)
    current_hour = datetime.now().hour
    
    # 检查输入的问候类型是否在当前时间范围内
    matched_greeting = None
    t=0
    for greeting in greeting_dict.values():
        if greeting['type'] == msg:
            if current_hour in greeting['range']:
                matched_greeting = greeting
                break
            else:
                # 如果问候类型不在当前时间范围内，返回当前可用的问候类型列表
                res = f"(*ﾟーﾟ)【店长】，现在是{"".join(get_current_greeting_types())}的时间呢~"
                name = '店长'
                res = res.replace('_n_','\n').replace('【店长】',name)
                return res
        t+=1

    
    # 从normalN消息组中随机选择一条消息
    messages = matched_greeting['message']['normalN']
    if not messages:  # 如果normalN为空，使用其他可用的消息组
        for season in ['normalS', 'normalR', 'springN', 'summerN', 'autumnN', 'winterN']:
            if greeting_dict['message'][season]:
                messages = greeting_dict['message'][season]
                break
    
    res = rc(messages)[0]  # 获取消息内容
    
    query=f"SELECT {data.LOVE}, {data.NAME}, b2, b3, b4, b5, b6, b7, b8, b9, b10 FROM G5000 where user_id== ?"
    args=(uid,)
    rows = data.sql(query,args)
    love = rows[0][0]
    b=rows[0][2:]
    name = '店长' if rows[0][1] in [0,'0',None] else rows[0][1]
    res = res.split('_n_')[0]
    res=res.replace('_n_','\n').replace('【店长】',name)
    if b[t] == 0 and sum(b) <= 2:
        num=random.randint(12,20)
        query=f"update G5000 set {data.LOVE}=?, b{t+2}=1 where user_id== ?"
        args=(love+num,uid,)
        data.sql(query,args)
        lv,nick = api.lv(love+num,name)
        res = f"[Lv.{lv}/0x{lv:x}-{nick}]\n{res}\n[好感度+{num}]"
    elif b[t] == 0:
        query=f"update G5000 set b{t+2}=1 where user_id== ?"
        args=(uid,)
        data.sql(query,args)
        lv,nick = api.lv(love,name)
        res = f"[Lv.{lv}/0x{lv:x}-{nick}]\n{res}\n今天聊得真开心呢ww~"
    else:
        res = f"(*ﾟーﾟ)【店长】今天已经说过[{msg}]啦~"
        return res
    fs = await api.myfriends()
    if uid in fs:
        pmsg=rc(messages)[0]
        pmsg=pmsg.replace('_n_','\n').replace('【店长】',name)
        m=[{"type":"text","data":{"text":pmsg}}]
        await bot.send_private_msg(user_id=uid,message=m)
    return res