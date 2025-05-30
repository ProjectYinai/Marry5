from nonebot import on_message
from nonebot.adapters import Bot, Event, Message
from nonebot.matcher import Matcher

from . import globe,api,sqlite

tea_message=on_message(priority=3,block=False)
@tea_message.handle()
async def tea_message(bot: Bot, event: Event, matcher: Matcher):
    #定时刷新信息
    #储存数据
    #监测领养人管理员身份#
    #未授权提示
    print("HANDLE:tea_message")
    id=await api.id(bot, event, matcher)
    iden=await api.iden(bot, event, matcher,id)
    await sqlite.update_uid(bot, event,matcher,id,iden)
