from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters import Bot
import re
import data
call_start={"茉莉以后叫我","茉莉请叫我","茉莉叫我"}
async def callme(bot:Bot, e:GroupMessageEvent):
    msg = str(e.get_message())
    uid = int(e.get_user_id())
    for i in call_start:
        msg=msg.replace(i,"")
    #query=f"update G5000 set {data.NAME}=? where user_id== ?"
    query=f"update user set prename=? where uid== ?"
    args=(msg,uid,)
    data.sql(query,args)
    res = f"(*ﾟ∇ﾟ)明白啦，审核成功后茉莉就叫店长【{msg}】了哦~"
    return res