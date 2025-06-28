from nonebot import require,get_bot, on_request
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, RequestEvent
from nonebot.matcher import Matcher
from nonebot.adapters import Bot
require("nonebot_plugin_apscheduler")
import requests
from nonebot_plugin_apscheduler import scheduler

teaRequest=on_request(priority=99,block=False)
@teaRequest.handle()
async def teaRequestFun(bot: Bot, e:RequestEvent, matcher: Matcher):
    request_type=str(e.request_type)
    if request_type=="friend":
        print("加好友申请٩( 'ω' )و get！")
        flag_a=str(e.flag)
        await bot.set_friend_add_request(flag=flag_a,approve=True)
    elif request_type=="group":
        print("邀请加入群٩( 'ω' )و get！")
        sub_type=str(e.sub_type)
        if sub_type=="invite":
            flag_a=str(e.flag)
            await bot.set_group_add_request(flag=flag_a,approve=True)

#@scheduler.scheduled_job("cron", hour="22",minute="55",second="0", id="job_4")
async def run_every_4_day():
    print("SCHEDULER:job_4")
    bot = get_bot()
    msg_t="(*ﾟ∇ﾟ)店长们晚安哦——"
    await bot.send_group_msg(group_id=str(555679990),message=msg_t)

@scheduler.scheduled_job("cron", hour="23",minute="55",second="0", id="h_end")
async def run_every_5_day():
    print("SCHEDULER:h_end")
    haruki_url="http://43.139.144.147:6099/api/OB11Config/SetConfig"
    payload = {"config":"{\"network\":{\"httpServers\":[{\"enable\":true,\"name\":\"http\",\"host\":\"127.0.0.1\",\"port\":3000,\"enableCors\":true,\"enableWebsocket\":true,\"messagePostFormat\":\"array\",\"token\":\"\",\"debug\":true}],\"httpSseServers\":[],\"httpClients\":[],\"websocketServers\":[],\"websocketClients\":[{\"enable\":true,\"name\":\"marry\",\"url\":\"ws://127.0.0.1:3010/onebot/v11/ws\",\"reportSelfMessage\":false,\"messagePostFormat\":\"array\",\"token\":\"marry\",\"debug\":false,\"heartInterval\":30000,\"reconnectInterval\":5000},{\"enable\":false,\"name\":\"haruki\",\"url\":\"ws://127.0.0.1:2525/ws\",\"reportSelfMessage\":false,\"messagePostFormat\":\"array\",\"token\":\"\",\"debug\":false,\"heartInterval\":30000,\"reconnectInterval\":30000}],\"plugins\":[]},\"musicSignUrl\":\"\",\"enableLocalFile2Url\":false,\"parseMultMsg\":false}"}
    requests.post(haruki_url, json=payload)
    bot = get_bot()
    msg_t="(*ﾟ∇ﾟ)店长们晚安哦——"
    await bot.send_group_msg(group_id=str(555679990),message=msg_t)

@scheduler.scheduled_job("cron", hour="5",minute="55",second="0", id="h_start")
async def run_every_6_day():
    print("SCHEDULER:h_start")
    haruki_url="http://43.139.144.147:6099/api/OB11Config/SetConfig"
    payload = {"config":"{\"network\":{\"httpServers\":[{\"enable\":true,\"name\":\"http\",\"host\":\"127.0.0.1\",\"port\":3000,\"enableCors\":true,\"enableWebsocket\":true,\"messagePostFormat\":\"array\",\"token\":\"\",\"debug\":true}],\"httpSseServers\":[],\"httpClients\":[],\"websocketServers\":[],\"websocketClients\":[{\"enable\":true,\"name\":\"marry\",\"url\":\"ws://127.0.0.1:3010/onebot/v11/ws\",\"reportSelfMessage\":false,\"messagePostFormat\":\"array\",\"token\":\"marry\",\"debug\":false,\"heartInterval\":30000,\"reconnectInterval\":5000},{\"enable\":true,\"name\":\"haruki\",\"url\":\"ws://127.0.0.1:2525/ws\",\"reportSelfMessage\":false,\"messagePostFormat\":\"array\",\"token\":\"\",\"debug\":false,\"heartInterval\":30000,\"reconnectInterval\":30000}],\"plugins\":[]},\"musicSignUrl\":\"\",\"enableLocalFile2Url\":false,\"parseMultMsg\":false}"}
    requests.post(haruki_url, json=payload)
    bot = get_bot()
    msg_t="(*ﾟ∇ﾟ)店长们早上好——"
    await bot.send_group_msg(group_id=str(555679990),message=msg_t)
    