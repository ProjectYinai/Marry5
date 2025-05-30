from nonebot import on_fullmatch, on_startswith
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from api import reply
import data
admin1_match={"重置泡茶时间"}
namesure = {"/同意昵称"}
admin1Time=on_fullmatch(admin1_match,is_type(GroupMessageEvent),priority=3,block=True)
nameSureTime=on_startswith(namesure,is_type(GroupMessageEvent),priority=3,block=True)
@admin1Time.handle()
async def teaFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    query="update G5000 set b1=1 where user_id== 3402824831"
    data.sql(query)
    msg="重置成功"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@nameSureTime.handle()
async def nameSureFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    if str(e.user_id) in data.admin.id:
        cmd = str(e.get_message()).split(" ")
        query=f'SELECT prename FROM user where uid== ?'
        args=(cmd[1],)
        rows = data.sql(query,args)
        if len(rows) == 0:
            msg=f"没有找到({cmd[1]})的申请"
        elif rows[0][0] == None:
            msg=f"({cmd[1]})没有申请昵称"
        elif cmd[2] == rows[0][0]:
            msg=f"已将({cmd[1]})的昵称改为【{cmd[2]}】"
            query="update user set name=?, prename=NULL where uid = ?"
            data.sql(query,(cmd[2],cmd[1]))
        else:
            msg=f"({cmd[1]})申请的昵称是【{rows[0][0]}】"
        msg_o=reply(e,msg)
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
