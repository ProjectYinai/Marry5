from nonebot import on_fullmatch, on_startswith
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from api import reply
from .tea import tea
from .hi import hi
from .getlove import getLove
from .call import callme
tea_match={"泡茉莉","泡红茶","泡咖啡","泡牛奶","泡奶茶","泡音奈"}
hi_match={"午夜好","凌晨好","清晨好","早上好","中午好","下午好","黄昏好","晚上好","晚安"}
love_match={"我的好感度","红茶浓度"}
call_start={"茉莉以后叫我","茉莉请叫我","茉莉叫我"}
teaTime=on_fullmatch(tea_match,is_type(GroupMessageEvent),priority=10,block=True)
hiTime=on_fullmatch(hi_match,is_type(GroupMessageEvent),priority=10,block=True)
loveTime=on_fullmatch(love_match,is_type(GroupMessageEvent),priority=10,block=True)
callTime=on_startswith(call_start,is_type(GroupMessageEvent),priority=10,block=True)

@teaTime.handle()
async def teaFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=await tea(bot,e)
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@hiTime.handle()
async def hiFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=await hi(bot,e)
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@loveTime.handle()
async def loveFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=await getLove(bot,e)
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@callTime.handle()
async def callFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=await callme(bot,e)
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)