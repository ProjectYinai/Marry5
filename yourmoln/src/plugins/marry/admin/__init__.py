from nonebot import on_fullmatch, on_startswith
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import data,api
from .execute import buildcmd
import json,psutil

namesure = {"/同意昵称","/拒绝昵称"}
white={"/设置白名单等级","/设白"}
bcmd={"/生成指令"}
excmd={"/执行指令"}
exsend={"/发送群消息"}
recrash={"/刷新缓存","/强制刷新缓存"}
hoststate={"/服务器状态","/服务器"}

nameSureTime=on_startswith(namesure,is_type(GroupMessageEvent),priority=3,block=True)
whiteTime=on_startswith(white,is_type(GroupMessageEvent),priority=3,block=True)
bcmdTime=on_startswith(bcmd,is_type(GroupMessageEvent),priority=1,block=True)
excmdTime=on_startswith(excmd,is_type(GroupMessageEvent),priority=1,block=True)
exsendTime=on_startswith(exsend,is_type(GroupMessageEvent),priority=1,block=True)
recrashTime=on_fullmatch(recrash,is_type(GroupMessageEvent),priority=3,block=True)
hostStateTime=on_fullmatch(hoststate,is_type(GroupMessageEvent),priority=3,block=True)

@nameSureTime.handle()
async def nameSureFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=2:
        cmd = str(e.get_message()).split(" ")
        if len(cmd)<=2 or cmd[1] == '-h':
            msg='/[同意|拒绝]昵称 [qq号] [昵称]'
            msg_o=api.reply(e,msg)
            await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
            return
        query=f'SELECT prename FROM user where uid== ?'
        args=(cmd[1],)
        rows = data.sql(query,args)
        try: cmd[2] = " ".join(cmd[2:])
        except: pass
        if len(rows) == 0:
            msg=f"没有找到({cmd[1]})的申请"
        elif rows[0][0] == None:
            msg=f"({cmd[1]})没有申请昵称"
        elif cmd[2] == rows[0][0] and cmd[0]=='/同意昵称':
            msg=f"已将({cmd[1]})的昵称改为【{cmd[2]}】"
            query="update user set name=?, prename=NULL where uid = ?"
            if cmd[2] in ['老婆','老公']:
                data.sql(query,('笨蛋',cmd[1]))
            else:
                data.sql(query,(cmd[2],cmd[1]))
            fs = await api.myfriends()
            if cmd[1] in fs:
                pmsg=f"(◍ ´꒳` ◍)店长的昵称审核成功啦，茉莉以后就叫你【{cmd[2]}】了哦~"
                m=[{"type":"text","data":{"text":pmsg}}]
                await bot.send_private_msg(user_id=cmd[1],message=m)
        elif cmd[2] == rows[0][0] and cmd[0]=='/拒绝昵称':
            msg=f"已拒绝({cmd[1]})的昵称改为【{cmd[2]}】"
            query="update user set prename=NULL where uid = ?"
            data.sql(query,(cmd[1],))
            fs = await api.myfriends()
            if cmd[1] in fs:
                pmsg=f"( 〞 0 ˄ 0 )店长的昵称审核失败！若多次设置违规昵称，茉莉可能会不理店长了哦！"
                m=[{"type":"text","data":{"text":pmsg}}]
                await bot.send_private_msg(user_id=cmd[1],message=m)
        else:
            msg=f"({cmd[1]})申请的昵称是【{rows[0][0]}】"
        msg_o=api.reply(e,msg)
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)


@whiteTime.handle()
async def whiteFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=10:
        cmd = str(e.get_message()).split(" ")
        if len(cmd)<=2 or cmd[1] == '-h':
            msg='/设白 [qq号] [白名单等级(int)]'
            msg_o=api.reply(e,msg)
            await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
            return
        query=f'update user set white=? where uid = ?'
        args=(cmd[2],cmd[1])
        try:
            data.sql(query,args)
            msg=f'已将({cmd[1]})的白名单等级改为【{cmd[2]}】'
        except:
            msg="设置失败"
        msg_o=api.reply(e,msg)
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@bcmdTime.handle()
async def bcmdFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=10:
        await bot.send_group_msg(group_id=str(e.group_id),message="指令生成中...")
        msg = await buildcmd(bot,e)
        msg_o=api.reply(e,msg)
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@excmdTime.handle()
async def excmdFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=10:
        try:
            query=str(e.message)[5:].strip()
            data.sql(query)
            msg=f"指令：{query}\n执行成功"
        except:
            msg="执行失败"
        msg_o=api.reply(e,msg)
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@exsendTime.handle()
async def exsendFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=10:
        cmd = str(e.get_message()).split(" ")
        if len(cmd)==1 or cmd[1] == '-h':
            msg='/发送群消息 [群号] [CQ格式消息]'
            msg_o=api.reply(e,msg)
            await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
            return
        sgid = cmd[1]
        send = "".join(cmd[2:])
        try: await bot.send_group_msg(group_id=str(sgid),message=[json.loads(send)])
        except Exception as exc: msg_o=api.reply(e,f"消息：{send}\n发送失败\n{exc}")
        else: msg_o=api.reply(e,"发送成功")
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@recrashTime.handle()
async def recrashFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=5:
        await bot.clean_cache()
        fs = await api.myfriends()
        gs = await api.mygroups()
        msg=f"缓存已刷新，当前拥有\n{len(fs)}位好友\n{len(gs)}个群聊\n今天是茉莉诞生的第{api.marryNowTime().days}天"
        msg_o=api.reply(e,msg)
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@hostStateTime.handle()
async def hostStateFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=5:
        cpus = f"CPU：\t{psutil.cpu_percent(interval=0.5)}%"
        mem = psutil.virtual_memory()
        mems = f"内存：\t{mem.percent}%"
        disk = psutil.disk_usage('/')
        disks = f"硬盘：\t{disk.percent}%"
        msg = "====服务器====\n"+"\n".join([cpus,mems,disks])
        msg_o=api.reply(e,msg)
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)