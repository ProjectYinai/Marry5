from nonebot import on_fullmatch, on_startswith, get_bot, on_message, on_notice
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, PokeNotifyEvent
from api import reply, stamp_def, mygroups
import data
import requests,datetime
get_auth_start={"授权申请","申请授权","申请领养"}
search_auth_start={"查授权"}
getauthTime=on_startswith(get_auth_start,is_type(GroupMessageEvent),priority=10,block=True)
authTime=on_message(is_type(GroupMessageEvent),priority=5,block=False)
whiteTime=on_message(is_type(GroupMessageEvent),priority=4,block=False)
searchAuthTime=on_startswith(search_auth_start,is_type(GroupMessageEvent),priority=10,block=True)
pokeTime=on_notice(is_type(PokeNotifyEvent),priority=5,block=False)
def getauth(gid):
    rows = data.sql("select uid from auth WHERE gid == ?",(gid,))
    if len(rows) < 1:
        return 0
    return rows[-1][0]

@whiteTime.handle()
async def authFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    w = data.getWhite(e.user_id)
    if w < 1:
        matcher.stop_propagation()
@authTime.handle()
@pokeTime.handle()
async def authFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    gid=e.group_id
    uid=e.user_id
    flag = 1
    at = data.sql("select uid from auth WHERE gid == ?",(gid,))
    for i in at:
        if int(i[0]) < 10000: 
            flag=0 #是特殊群则不检测
            break
        try: role = await bot.get_group_member_info(group_id=gid,user_id=i[0],no_cache=False)
        except: role = 0
        else: role = role['role']
        if role == 0:
            pmsg=f"( 〞 0 ˄ 0 )错误代码：D-2-2。\n店长不是群聊({gid})的成员呢。\n(*ﾟーﾟ)店长请在成为群主或管理员后重新授权吧"
            m=[{"type":"text","data":{"text":pmsg}}]
            await bot.send_private_msg(user_id=i[0],message=m)
        elif role in ['admin','owner']:
            flag=0
            break
        else:
            pmsg=f"( 〞 0 ˄ 0 )错误代码：D-2-1。\n店长不是群聊({gid})的管理员或群主呢。\n(*ﾟーﾟ)店长请在成为群主或管理员后重新授权吧"
            m=[{"type":"text","data":{"text":pmsg}}]
            await bot.send_private_msg(user_id=i[0],message=m)
    if flag: #没有授权
        #删除群授权
        data.sql("DELETE FROM auth WHERE gid=?;",(gid,))
        haruki_url="http://127.0.0.1:2525/haruki_client/controller/remove_whitelist"
        payload = {"module":"pjsk","group_ids":[int(gid)]}
        requests.post(haruki_url, json=payload)
        #退群
        lastsent = await bot.get_group_member_info(group_id=gid,user_id=bot.self_id,no_cache=False)
        lastsent = int(lastsent["last_sent_time"])
        if (stamp_def()[0] - lastsent) > 36000:
            pass
            #await bot.set_group_leave(group_id=gid)
        matcher.stop_propagation()
    else:
        data.sql(f"INSERT OR IGNORE INTO user \
                 (uid, meet) values \
                 (?,?)",
                 (uid,stamp_def()[4]))#如果是新店长则添加数据

@getauthTime.handle()
async def getauthFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg_i=str(e.get_message())
    uid=int(e.get_user_id())
    for i in get_auth_start:
        msg_i = msg_i.replace(i,'')
    lv = data.getLove(uid)[0]
    now = datetime.datetime.now()
    #if now.hour <=5 or (now.hour==23 and now.minute>=50):
    if (stamp_def()[1]-7200)%86400 >= 64800:
        msg="( 〞 0 ˄ 0 )错误代码：D-1-5。\n茉莉已经睡觉啦，请早上6点之后再申请授权哦~"
    elif e.group_id not in data.getMainGroups():
        msg="( 〞 0 ˄ 0 )错误代码：D-1-4。\n请添加主群后领养。\nps:发送茉莉帮助就能看到主群的二维码哦~"
    elif lv<70:
        msg="( 〞 0 ˄ 0 )错误代码：D-1-3。\n领养人好感度等级未到70级！"
    elif int(msg_i) not in (gl := await mygroups()):
        msg="( 〞 0 ˄ 0 )错误代码：D-1-2。\n茉莉不在该群内。"
    elif (who := getauth(msg_i)) >= 10000:
        msg="( 〞 0 ˄ 0 )错误代码：D-1-1。\n本群已授权且已存在领养人。若想更改领养人，请联系茉莉的主人音奈更改。\n不过更新了一下pjsk的授权~"
        haruki_url="http://127.0.0.1:2525/haruki_client/controller/add_whitelist"
        payload = {"module":"pjsk","group_ids":[int(msg_i)]}
        requests.post(haruki_url, json=payload)
    else:
        try: role = await bot.get_group_member_info(group_id=msg_i,user_id=uid,no_cache=False)
        except: role = 0
        else: role = role['role']
        try: gml = await bot.get_group_member_list(group_id=gid,no_cache=False)
        except: gml = 1
        else: gml = len(gml)
        if role == 0: msg=f"( 〞 0 ˄ 0 )错误代码：D-2-2。\n店长不是群聊({msg_i})的成员呢。"
        elif role not in ['admin','owner']:
            msg=f"( 〞 0 ˄ 0 )错误代码：D-2-1。\n店长不是群聊({msg_i})的管理员或群主呢。"
        elif role == 'admin' and lv < 100:
            msg="( 〞 0 ˄ 0 )错误代码：D-1-6。\n领养人作为管理员好感度等级未到100级！"
        elif gml > 500 and role != 'owner':
            msg="( 〞 0 ˄ 0 )错误代码：D-2-3。\n群聊人数大于500，领养人需为群主！"
        else:
            time = stamp_def()[0]
            data.sql("INSERT INTO auth (uid, gid, time) VALUES (?, ?, ?)",(uid,msg_i,time))
            msg = f"｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡领养成功~\n领养群：{msg_i}\n领养有效期：-1天，大概。\n请领养人不要删除茉莉好友！不要退出主群！可永久屏蔽主群！\n(PS: 领养人需要保持群主或者管理员身份才不会掉授权哦)"
            haruki_url="http://127.0.0.1:2525/haruki_client/controller/add_whitelist"
            payload = {"module":"pjsk","group_ids":[int(msg_i)]}
            requests.post(haruki_url, json=payload)
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@searchAuthTime.handle()
async def searchAuthFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg_i = str(e.get_message())
    for i in search_auth_start:
        msg_i = msg_i.replace(i,'')
    if msg_i == "":
        gid=e.group_id
    else:
        gid=int(msg_i)
    who = getauth(gid)
    if who:
        msg = f"授权群号:{gid}\n授权查询:已授权\n领养の人:{who}"
    else:
        msg = f"授权群号:{gid}\n授权查询:未授权"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)