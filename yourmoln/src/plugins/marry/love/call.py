from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, MessageEvent
from nonebot.adapters import Bot
import data,api
call_start={"茉莉以后叫我","茉莉请叫我","茉莉叫我"}
async def callme(bot:Bot, e:MessageEvent) -> str:
    """这个功能是申请昵称用哒"""
    msg = str(e.get_message())
    uid = int(e.get_user_id())
    for i in call_start:
        msg=msg.replace(i,"")
    msg=msg.strip()
    if len(msg) == 0: return "(*ﾟーﾟ)茉莉要叫店长什么呢？"
    elif len(msg) >= 16: return "(*ﾟーﾟ)店长的名字太长啦，稍微改短一点吧~"
    fl = await api.myfriends()
    stamp = api.stamp_def()
    query=f'SELECT nametime,name FROM user where uid = ?'
    args=(uid,)
    rows = data.sql(query,args)
    name = '店长' if rows[0][1] in [0,'0',None] else rows[0][1]
    if msg in ["茉莉","三色仮茉莉"]: return "(*ﾟーﾟ)如果【店长】是茉莉，那茉莉是谁呢······".replace("【店长】",name)
    if uid not in fl: return "(*ﾟーﾟ)抱歉，【店长】需要先和茉莉加好友才能使用自定义昵称呢~".replace("【店长】",name)
    if rows[0][1] != None:
        if rows[0][1] == msg: return f'(*ﾟーﾟ)店长不就叫{msg}吗？'
    if int(rows[0][0]) == stamp[4]:
        return '(*ﾟーﾟ)店长今天已经提交过申请了，明天再来吧！'
    query=f"update user set prename=?, nametime=? where uid = ?"
    args=(msg,stamp[4],uid,)
    data.sql(query,args)
    res = f"(*ﾟ∇ﾟ)明白啦，审核成功后茉莉就叫店长【{msg}】了哦~"
    if type(e) == GroupMessageEvent:
        am1=f"申请人QQ: {uid}\n申请所在群: {e.group_id}\n申请昵称: {msg}"
    else:
        am1=f"申请人QQ: {uid}\n申请昵称: {msg}"
    am1=[{"type":"text","data":{"text":am1}}]
    am2=f"/同意昵称 {uid} {msg}"
    am2=[{"type":"text","data":{"text":am2}}]
    for i in data.getAdminGroups():
        await bot.send_group_msg(group_id=str(i),message=am1)
        await bot.send_group_msg(group_id=str(i),message=am2)
    return res