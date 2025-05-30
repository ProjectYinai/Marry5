from nonebot import get_bot
from nonebot_plugin_apscheduler import scheduler
import json,os,psutil
from . import globe,api
global friend_list_sch,cfg
cfg=globe.cfg.cfg

with open(cfg["SP"]+"/tea/friend_list.json","r",encoding='utf-8') as tea_json:
    friend_list_sch=json.load(tea_json)
    tea_json.close()


@scheduler.scheduled_job("cron", minute="5", id="job_1")
async def run_every_1_hour():
    print("SCHEDULER:job_1")
    bot = get_bot()
    stamp=globe.stamp.stamp()
    global friend_list_sch
    with open(cfg["SP"]+"/tea/friend_list.json","r",encoding='utf-8') as tea_json:
        friend_list_sch=json.load(tea_json)
        tea_json.close()


@scheduler.scheduled_job("cron", hour="*/1", id="job_2")
async def refriend_def():
    print("SCHEDULER:job_2")
    global cfg
    bot = get_bot()
    if not os.path.isfile(cfg["SP"]+"/tea/friend_list.json"):
        os.chdir(cfg["SP"])
        file=open(cfg["SP"]+"/tea/friend_list.json","w")
        file.write("")
        file.close
    friend=await bot.get_friend_list()
    friend_list={}
    for i in friend:
        puid_a="P"+str(i["user_id"])
        temp_1={puid_a:i}
        friend_list.update(temp_1)
    with open(cfg["SP"]+"/tea/friend_list.json","w",encoding='utf-8') as tea_json:
        json.dump(friend_list,tea_json,indent=1)
        tea_json.close()


@scheduler.scheduled_job("cron", hour="6",minute="55",second="0", id="job_3")
async def run_every_3_day():
    print("SCHEDULER:job_3")
    os.startfile("E:\\HarukiClient\\HarukiClient-Windows-x64-v1.1.5.exe")
    

@scheduler.scheduled_job("cron", hour="22",minute="55",second="0", id="job_4")
async def run_every_4_day():
    print("SCHEDULER:job_4")
    bot = get_bot()
    msg_t="(*ﾟ∇ﾟ)店长们晚安哦——"
    await bot.send_group_msg(group_id=str(555679990),message=msg_t)
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'HarukiClient-Windows-x64-v1.1.5.exe':
            print(f"找到进程: PID={proc.info['pid']}, 名称={proc.info['name']}")
            pid=proc.info['pid']
            proccess=psutil.Process(pid)
            proccess.terminate()



class schedule():
    global friend_list_sch
    friend_list=friend_list_sch
