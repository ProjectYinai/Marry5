from nonebot import on_fullmatch, on_startswith, on_notice
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, PokeNotifyEvent
from api import reply, replyImg

import os, json, random
script_path = os.path.split(os.path.realpath(__file__))[0]
def choose(kind:str):
    json_data = open(f"{script_path}/{kind}.json",encoding="UTF-8").read()
    cl = json.loads(json_data)
    return random.choice(cl)

help_match={"茉莉帮助","茉莉使用手册","如何与茉莉玩","茉莉指令大全","茉莉使用说明书","茉莉和我玩"}
eat_match={"茉莉今天吃什么", "茉莉吃什么"}
drink_match={"茉莉今天喝什么", "茉莉喝什么"}
draw_match={"茉莉帮我抽个签", "茉莉抽个签", "茉莉抽签"}
helpTime=on_fullmatch(help_match,is_type(GroupMessageEvent),priority=10,block=True)
eatTime=on_fullmatch(eat_match,is_type(GroupMessageEvent),priority=10,block=True)
drinkTime=on_fullmatch(drink_match,is_type(GroupMessageEvent),priority=10,block=True)
drawTime=on_fullmatch(draw_match,is_type(GroupMessageEvent),priority=10,block=True)
pokeTime=on_notice(is_type(PokeNotifyEvent),priority=20,block=True)

@helpTime.handle()
async def helpFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=f"file:///{script_path}\marry_help.png"
    msg_o=replyImg(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@eatTime.handle()
async def eatFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=f"(ฅ・▽・)ฅ茉莉今天推荐店长吃【{choose('eat')}】呢！"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@drinkTime.handle()
async def drinkFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=f"(ฅ・▽・)ฅ茉莉今天推荐店长吃【{choose('drink')}】呢！"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@drawTime.handle()
async def drawFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    draw=choose('draw')
    msg=draw[0]+random.choice(draw[1:])+"！"
    msg_o=reply(e,msg)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)

@pokeTime.handle()
async def pokeFun(bot: Bot, e: PokeNotifyEvent, matcher: Matcher):
    if e.target_id == e.self_id:
        msg_o="˚‧º·(˚ ˃̣̣̥᷄⌓˂̣̣̥᷅ )‧º·˚不要再戳茉莉啦~"
        await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)