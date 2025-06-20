from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters import Bot
import data,api
from .buildsql import bsql
async def buildcmd(bot:Bot, e:GroupMessageEvent):
    msg = str(e.message)[5:]
    return bsql(msg,e.user_id)