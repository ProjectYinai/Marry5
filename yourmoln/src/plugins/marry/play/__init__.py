from nonebot import on_fullmatch, on_startswith, on_notice
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, PokeNotifyEvent
from api import reply, replyImg
import api,data
import os, json, random
script_path = os.path.split(os.path.realpath(__file__))[0]
def choose(kind:str):
    json_data = open(f"{script_path}/{kind}.json",encoding="UTF-8").read()
    cl = json.loads(json_data)
    return random.choice(cl)

from .wife import roll,marry,rank
from .hitokoto import generate_hitokoto_message

help_match={"茉莉帮助","茉莉使用手册","如何与茉莉玩","茉莉指令大全","茉莉使用说明书","茉莉和我玩"}
eat_match={"茉莉今天吃什么", "茉莉吃什么"}
drink_match={"茉莉今天喝什么", "茉莉喝什么"}
draw_match={"茉莉帮我抽个签", "茉莉抽个签", "茉莉抽签"}
roll_wife_match={"抽群老婆","抽群老婆十连","群老婆十连"}
wife_rank_match={"群老婆排行榜"}
marry_wife_start={"娶群老婆"}
helpTime=on_fullmatch(help_match,is_type(GroupMessageEvent),priority=10,block=True)
eatTime=on_fullmatch(eat_match,is_type(GroupMessageEvent),priority=10,block=True)
drinkTime=on_fullmatch(drink_match,is_type(GroupMessageEvent),priority=10,block=True)
drawTime=on_fullmatch(draw_match,is_type(GroupMessageEvent),priority=10,block=True)
rollWifeTime=on_fullmatch(roll_wife_match,is_type(GroupMessageEvent),priority=10,block=True)
wifeRankTime=on_fullmatch(wife_rank_match,is_type(GroupMessageEvent),priority=10,block=True)
marryWifeTime=on_startswith(marry_wife_start,is_type(GroupMessageEvent),priority=10,block=True)
pokeTime=on_notice(is_type(PokeNotifyEvent),priority=20,block=True)

@helpTime.handle()
async def helpFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=f"file:///{script_path}/marry_help.png"
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

@rollWifeTime.handle()
async def rollWifeFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=await roll(bot,e)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg)

@wifeRankTime.handle()
async def wifeRankFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=await rank(bot,e)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg)

@marryWifeTime.handle()
async def marryWifeFun(bot: Bot, e: GroupMessageEvent, matcher: Matcher):
    msg=await marry(bot,e)
    await bot.send_group_msg(group_id=str(e.group_id),message=msg)

@pokeTime.handle()
async def pokeFun(bot: Bot, e: PokeNotifyEvent, matcher: Matcher):
    if e.target_id == e.self_id:
        mode = random.randint(0,9)
        match mode:
            case x if x < 9:
                msg_o="˚‧º·(˚ ˃̣̣̥᷄⌓˂̣̣̥᷅ )‧º·˚不要再戳茉莉啦~"
                await bot.send_group_msg(group_id=str(e.group_id),message=msg_o)
            case 9:
                await bot.group_poke(group_id=str(e.group_id),user_id=str(e.user_id))
        fs = await api.myfriends()
        if e.user_id in fs:
            htk = hitokoto.generate_hitokoto_message()
            query=f"SELECT name FROM user where uid = ?"
            rows = data.sql(query,(e.user_id,))
            name = '店长' if rows[0][0] in [None] else rows[0][0]
            if htk["code"] == 200:
                htkdata = htk["response"]["data"]
                pmsg = f"{name}，梦中好呢ww~\n啊...刚刚在做梦吗？（。。）\n「{htkdata["hitokoto"]}」——{htkdata["source"]}...\n被吵醒有点困呢，再睡五分钟...（￣▽￣）"
                m=[{"type":"text","data":{"text":pmsg}}]
                await bot.send_private_msg(user_id=e.user_id,message=m)