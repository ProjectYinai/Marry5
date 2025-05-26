from nonebot import on_fullmatch, on_startswith
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from api import reply
import data
admin1_match={"重置泡茶时间"}

admin1Time=on_fullmatch(admin1_match,is_type(GroupMessageEvent),priority=3,block=True)

@admin1Time.handle()
async def teaFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    query="update G5000 set b1=1 where user_id== 3402824831"
    data.sql(query)
    msg="重置成功"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
