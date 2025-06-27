from nonebot import get_bot
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, MessageEvent
import time,datetime
import json,os,random,operator
import data
script_path = os.path.split(os.path.realpath(__file__))[0]
json_data = open(f"{script_path}/lv.json",encoding="UTF-8").read()
lv_list = json.loads(json_data)
def reply(e:MessageEvent,msg:str):
    """生成回复消息"""
    res=[{"type":"reply","data":{"id":str(e.message_id)}},{"type":"text","data":{"text":msg}}]
    return res
def replyImg(e:MessageEvent,img:str):
    """生成图片回复消息"""
    res=[{"type":"reply","data":{"id":str(e.message_id)}},{"type":"image","data":{"file":img}}]
    return res
def lv(love:int,name='0'):
    """计算好感度等级"""
    love = int(love)
    lv = int(((192*(192+love))**0.5-192)*100//1536)
    for i in lv_list[::-1]:
        if lv >= i['lv']:
            nick = i['nick']
            break
    nick = nick.replace('【店长】',name)
    return lv,nick

async def myfriends(nc=False) -> list:
    """获取好友列表的函数"""
    bot=get_bot()
    fl = await bot.get_friend_list(no_cache=nc)
    friends=[i["user_id"] for i in fl]
    return friends

async def mygroups(nc=False) -> list:
    """获取群聊列表的函数"""
    bot=get_bot()
    gl = await bot.get_group_list()
    groups=[i["group_id"] for i in gl]
    return groups

async def myGroupMembers(gid,nc=False) -> list[tuple[int,str,int]]:
    """qid,name,sendtime
    获取群成员列表的函数,按最近发言时间正序"""
    bot=get_bot()
    gm = await bot.get_group_member_list(group_id=gid,no_cache=nc)
    gm=[(i["user_id"],i["card"],int(i["last_sent_time"])) if i["card"] != "" else (i["user_id"],i["nickname"],int(i["last_sent_time"])) for i in gm]
    gm = sorted(gm, key=operator.itemgetter(2),reverse=True)
    return gm

def stamp_def():
    """很抽象的获取各类时间的函数"""
    birthday=1513972500
    time_stamp=int(time.time())
    time_interval=time_stamp-birthday
    time_stamp_sec=int(time_interval)
    time_stamp_min=int(time_interval/60)
    time_stamp_hour=int(time_interval/3600)
    time_stamp_day=int(time_interval/86400)
    
    birthday="2017-12-23"
    time_stamp_mon=0#rrule.rrule(rrule.MONTHLY,dtstart=parse("2017-12-23"),until=datetime.date.today()).count()
    time_stamp_year=0#rrule.rrule(rrule.YEARLY,dtstart=parse("2017-12-23"),until=datetime.date.today()).count()


    time_local_yday=int(time.localtime().tm_yday)
    time_local_wday=int(time.localtime().tm_wday)
    time_local_sec=int(time.localtime().tm_sec)
    time_local_min=int(time.localtime().tm_min)
    time_local_hour=int(time.localtime().tm_hour)
    time_local_mday=int(time.localtime().tm_mday)
    time_local_mon=int(time.localtime().tm_mon)
    time_local_year=int(time.localtime().tm_year)

    stamp=[time_stamp,
    time_stamp_sec,
    time_stamp_min,
    time_stamp_hour,
    time_stamp_day,
    time_stamp_mon,
    time_stamp_year,
    time_local_yday,
    time_local_wday,
    time_local_sec,
    time_local_min,
    time_local_hour,
    time_local_mday,
    time_local_mon,
    time_local_year]

    return(stamp)