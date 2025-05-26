from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import re
import data
call_start={"茉莉以后叫我","茉莉请叫我","茉莉叫我"}
def callme(e:GroupMessageEvent):
    NAME = 'a4'
    msg = str(e.get_message())
    uid = int(e.get_user_id())
    for i in call_start:
        msg=msg.replace(i,"")
    query=f"update G5000 set {NAME}=? where user_id== ?"
    args=(msg,uid,)
    data.sql(query,args)
    res = f"(◍ ´꒳` ◍)店长的昵称审核成功啦，茉莉以后就叫你【{msg}】了哦~"
    return res