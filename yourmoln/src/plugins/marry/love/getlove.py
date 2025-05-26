from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters import Bot
import data
async def getLove(bot:Bot, e:GroupMessageEvent):
    lv,nick,love,name = data.getLove(e.get_user_id())
    res = f"茉莉对店长大人的好感度超级大呢！\n大概{love}点吧ww~~\n[更详细的内容跟茉莉加好友后会偷偷发给店长呢ww~]"
    res = res.replace('_n_','\n').replace('【店长】',name)
    res = f"[Lv.{lv}/0x{lv:x}-{nick}]\n{res}"
    return res