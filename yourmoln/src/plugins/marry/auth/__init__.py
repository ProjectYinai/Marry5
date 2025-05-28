from nonebot import on_fullmatch, on_startswith, get_bot, on_message
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from api import reply, stamp_def
import data

try:
    AUTH = data.sql("select * from auth")
except data.sqlite3.OperationalError:
    data.sql("""CREATE TABLE auth (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            uid  INTEGER,
            gid  INTEGER,
            time INTEGER
            );""")
    

get_auth_start={"授权申请","申请授权"}
search_auth_match={"查授权"}
getauthTime=on_startswith(get_auth_start,is_type(GroupMessageEvent),priority=10,block=True)
authTime=on_message(is_type(GroupMessageEvent),priority=3,block=False)
searchAuthTime=on_fullmatch(search_auth_match,is_type(GroupMessageEvent),priority=10,block=True)
def getauth(gid):
    rows = data.sql("select uid from auth WHERE gid == ?",(gid,))
    if len(rows) < 1:
        return False
    return rows[0][0]

@authTime.handle()
async def authFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    gid=e.group_id
    uid=e.user_id
    flag = 1
    at = data.sql("select uid from auth WHERE gid == ?",(gid,))
    for i in at:
        role = await bot.get_group_member_info(group_id=gid,user_id=i[0],no_cache=False)
        role = role['role']
        if role in ['admin','owner']:
            flag=0
            break
    msg=gid
    msg_o=reply(e,msg)
    #await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
    if flag: #没有授权
        matcher.stop_propagation()
    else:
        data.sql(f"INSERT OR IGNORE INTO G5000 \
                 (user_id,group_id,{data.MEETTIME},{data.WHITELIST},a2,a7,a8) values \
                 (?,5000,?,1,0,0,0)",
                 (uid,stamp_def()[4]))#如果是新店长则添加数据

@getauthTime.handle()
async def getauthFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg_i=str(e.get_message())
    uid=int(e.get_user_id())
    for i in get_auth_start:
        msg_i = msg_i.replace(i,'')
    lv,nick,love,name = data.getLove(uid)
    who = getauth(msg_i)
    if lv<0x100:
        msg="( 〞 0 ˄ 0 )错误代码：D-1-5。\n领养人好感度等级未到100级！"
    elif who:
        msg="( 〞 0 ˄ 0 )错误代码：D-1-3。\n本群已授权且已存在领养人。若想更改领养人，请联系茉莉的主人音奈更改。\n不过更新了一下pjsk的授权~"
    else:
        time = stamp_def()[0]
        data.sql("INSERT INTO auth (uid, gid, time) VALUES (?, ?, ?)",(uid,msg_i,time))
        msg = f"｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡领养成功~\n领养群：{msg_i}\n领养有效期：-1天，大概。\n请领养人不要删除茉莉好友！不要退出主群！可永久屏蔽主群！"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@searchAuthTime.handle()
async def searchAuthFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    gid=e.group_id
    who = getauth(gid)
    if who:
        msg = f"授权查询：已授权\n领养人：{who}"
    else:
        msg = "授权查询：未授权"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)