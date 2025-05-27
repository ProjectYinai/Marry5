from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters import Bot
import data, api
async def getLove(bot:Bot, e:GroupMessageEvent):
    uid = int(e.get_user_id())
    lv,nick,love,name,teatimes,greettimes,meettime = data.getLove(uid)
    meettime = api.stamp_def()[4] - meettime
    res = f"茉莉对店长大人的好感度超级大呢！\n大概{love}点吧ww~~"
    res = res.replace('_n_','\n').replace('【店长】',name)
    res = f"[Lv.{lv}/0x{lv:x}-{nick}]\n{res}"
    fs = await api.myfriends()
    if uid in fs:
        pmsg=f"一杯红茶，溶入{love}点互相的爱慕；一吮香甜，回想{teatimes}杯红茶的时光。点燃引路之灯，见证{greettimes}次欢乐的笑容；牵引系心之线，忆起{meettime}天前相遇的过往。至此，感谢【店长】的陪伴！"
        pmsg=pmsg.replace('_n_','\n').replace('【店长】',name)
        m=[{"type":"text","data":{"text":pmsg}}]
        await bot.send_private_msg(user_id=uid,message=m)
    else: res+="\n[更详细的内容跟茉莉加好友后会偷偷发给店长呢ww~]"
    return res