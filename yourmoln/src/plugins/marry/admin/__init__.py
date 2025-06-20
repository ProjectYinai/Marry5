from nonebot import on_fullmatch, on_startswith
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import data,api
from .execute import buildcmd
admin1_match={"重置泡茶时间"}
namesure = {"/同意昵称","/拒绝昵称"}
white={"/设置白名单等级","/设白"}
bcmd={"/生成指令"}
excmd={"/执行指令"}
admin1Time=on_fullmatch(admin1_match,is_type(GroupMessageEvent),priority=3,block=True)
nameSureTime=on_startswith(namesure,is_type(GroupMessageEvent),priority=3,block=True)
whiteTime=on_startswith(white,is_type(GroupMessageEvent),priority=3,block=True)
bcmdTime=on_startswith(bcmd,is_type(GroupMessageEvent),priority=1,block=True)
excmdTime=on_startswith(excmd,is_type(GroupMessageEvent),priority=1,block=True)
@admin1Time.handle()
async def teaFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    query="update G5000 set b1=1 where user_id== 3402824831"
    data.sql(query)
    msg="重置成功"
    msg_o=api.reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@nameSureTime.handle()
async def nameSureFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id or data.getWhite(e.user_id)>=2:
        cmd = str(e.get_message()).split(" ")
        if len(cmd)==1 or cmd[1] == '-h':
            msg='/[同意|拒绝]昵称 [qq号] [昵称]'
            msg_o=api.reply(e,msg)
            await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
            return
        query=f'SELECT prename FROM user where uid== ?'
        args=(cmd[1],)
        rows = data.sql(query,args)
        if len(rows) == 0:
            msg=f"没有找到({cmd[1]})的申请"
        elif rows[0][0] == None:
            msg=f"({cmd[1]})没有申请昵称"
        elif cmd[2] == rows[0][0] and cmd[0]=='/同意昵称':
            msg=f"已将({cmd[1]})的昵称改为【{cmd[2]}】"
            query="update user set name=?, prename=NULL where uid = ?"
            data.sql(query,(cmd[2],cmd[1]))
            fs = await api.myfriends()
            if cmd[1] in fs:
                pmsg=f"(◍ ´꒳` ◍)店长的昵称审核成功啦，茉莉以后就叫你【{cmd[2]}】了哦~"
                m=[{"type":"text","data":{"text":pmsg}}]
                await bot.send_private_msg(user_id=cmd[1],message=m)
        elif cmd[2] == rows[0][0] and cmd[0]=='/拒绝昵称':
            msg=f"已拒绝({cmd[1]})的昵称改为【{cmd[2]}】"
            query="update user set prename=NULL where uid = ?"
            data.sql(query,(cmd[1]))
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
        if len(cmd)==1 or cmd[1] == '-h':
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