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
    regreet="".join(['1']+['0' for i in greeting_dict.keys()])
    regreet=int(regreet,2)
    if k==0:
        day = api.stamp_def()[4]
        query = f"UPDATE user SET ifgreet = ?, greetime = ?\
                WHERE uid = ? AND greetime != ?;"
        args = (regreet,day,uid,day)
    else:#强制刷新
        day = api.stamp_def()[4]
        query = f"UPDATE user SET ifgreet = ?, greetime = ?\
                WHERE uid = ?;"
        args = (regreet,day,uid,day)
    data.sql(query,args)
def get_current_greeting_types():
    """获取当前时间段可用的问候类型列表"""
    current_hour = datetime.now().hour
    available_types = []
    
    for greeting in greeting_dict.values():
        if current_hour in greeting['range']:
            if greeting['type'] == "晚安": continue
            available_types.append(f"[{greeting['type']}]")
            available_types.append("和")
    return available_types[:-1]

async def hi(bot:Bot, e:GroupMessageEvent) -> str:
    """这里是茉莉与店长打招呼的函数"""
    msg=str(e.get_message())
    uid=int(e.get_user_id())
    refresh(uid)
    current_hour = datetime.now().hour
    
    # 检查输入的问候类型是否在当前时间范围内
    matched_greeting = None
    t=0
    for greeting in greeting_dict.values():
        t+=1
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
    # 从normalN消息组中随机选择一条消息
    messages = matched_greeting['message']['normalN']
    if not messages:  # 如果normalN为空，使用其他可用的消息组
        for season in ['normalS', 'normalR', 'springN', 'summerN', 'autumnN', 'winterN']:
            if greeting_dict['message'][season]:
                messages = greeting_dict['message'][season]
                break
    res = rc(messages)[0]  # 获取消息内容
    query=f"SELECT love, name, ifgreet FROM user where uid== ?"
    args=(uid,)
    rows = data.sql(query,args)
    love = rows[0][0]
    ifgreet=list(bin(rows[0][2])[2:])
    name = '店长' if rows[0][1] in [0,'0',None] else rows[0][1]
    res = res.split('_n_')[0]
    res=res.replace('_n_','\n').replace('【店长】',name)
    if ifgreet[t] == '0' and sum(map(int,ifgreet)) <= 2:
        num=random.randint(12,20)
        ifgreet[t] = '1'
        ifgreet=int("".join(ifgreet),2) 
        query=f"update user set love=love+?, ifgreet=?, egreet=egreet+1 where uid== ?"
        args=(num,ifgreet,uid,)
        data.sql(query,args)
        lv,nick = api.lv(love+num,name)
        res = f"[Lv.{lv}-{nick}]\n{res}\n[好感度+{num}]"
    elif ifgreet[t] == '0':
        ifgreet[t] = '1'
        ifgreet=int("".join(ifgreet),2) 
        query=f"update user set ifgreet=?, egreet=egreet+1 where uid== ?"
        args=(ifgreet,uid,)
        data.sql(query,args)
        lv,nick = api.lv(love,name)
        res = f"[Lv.{lv}-{nick}]\n{res}\n今天聊得真开心呢ww~"
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