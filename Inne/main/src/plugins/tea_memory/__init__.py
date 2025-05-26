import json
import random
import re
import time
import urllib
import os

#========
import sqlite3 as sql
import psutil
import keyboard
import pathlib
import asyncio
import datetime
import dateutil#python-dateutil
from dateutil import rrule
from dateutil.parser import parse
import PIL# type: ignore #pillow
import nonebot # type: ignore
import nonebot.drivers.aiohttp  # type: ignore # type: ignore
from nonebot import get_driver, on_message, on_command, get_bot, on_startswith, on_fullmatch, on_notice, on_request # type: ignore
from nonebot.adapters import Bot, Event, Message # type: ignore
from nonebot.params import EventMessage, EventPlainText, Arg, CommandArg, ArgPlainText, EventType # type: ignore
from nonebot.matcher import Matcher # type: ignore
from nonebot.rule import to_me, keyword, startswith # type: ignore
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent # type: ignore
from nonebot_plugin_apscheduler import scheduler

_n="\n"
#========
temp_stamp=int(time.time())
start_stamp=temp_stamp+30
version=250405
code_lista=["a1","a2","a3","a4","a5","a6","a7","a8","a9","a10",
            "b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","b11","b12",
            "p1",
            "q1","q2","q3"]
code_listg=["g1","g2","g3","g4","g5",
            "h1","h2",
            "s1","s2","s3",
            "t1","t2","t3","t4"]
#========
import api,globe
global stamp,cfg
stamp=globe.stamp()
cfg=globe.cfg()
#========

#================
X_tea_message=on_message(priority=99,block=False)
@X_tea_message.handle()
async def X_tea_message(bot: Bot, event: Event, matcher: Matcher):
    #定时刷新信息
    #储存数据
    #监测领养人管理员身份#
    #未授权提示
    print("HANDLE:X")
    global stamp,cfg
    id=await api.id(bot, event, matcher)
    iden=await api.iden(bot, event, matcher,id)
    await X.tea_message(bot, event,matcher,stamp,id,iden)
    await matcher.finish()

Y_tea_notice=on_notice(priority=99,block=False)
#@Y_tea_notice.handle()
async def Y_tea_notice(bot: Bot, event: Event, matcher: Matcher):
    print("HANDLE:Y")
    id=await id_def(bot, event, matcher)
    await Y.tea_notice(bot, event,matcher,stamp,id)
    await matcher.finish()

Z_tea_request=on_request(priority=99,block=False)
#@Z_tea_request.handle()
async def Z_tea_request(bot: Bot, event: Event, matcher: Matcher):
    print("HANDLE:Z")
    global stamp
    id,iden=await birthday(bot, event, matcher)
    await Z.tea_request(bot, event,matcher,stamp,id,iden)
    await matcher.finish()

#================



async def renew_def(bot, event, matcher,stamp,id):
    global tea_db,tea_cur
    puid="P"+str(id[0])
    ggid="G"+str(id[1])
    #查找个人代码是否齐全，主要为G5000
    #tea_cur.execute("select a0 from G5000 where user_id==1000")
    #for tea_row in tea_cur:
        #A0=tea_row[0]
    #if A0!=version:
        #for i in code_lista:
            #tea_cur.execute("alter table G5000 add column "+str(i)+" int if not exists (select "+str(i)+" from G5000)")
    #检查是否存在该群表
    #检查群代码是否齐全
    if id[1]:
        #tea_cur.execute("select g0 from "+ggid+" where user_id==1000")
        go=await V.selecting(1000,ggid,"g0")
        if go[0]!=version:
            try:#尝试创建新表，若存在报错跳过
                await V.execute("create table "+str(ggid)+"""(user_id integer primary key autoincrement not null,
                                group_id int not null,
                                g0 int)""")
            except:
                pass
            try:#尝试创建uid1000，若存在报错跳过
                await V.execute("insert into "+str(ggid)+"""(user_id,group_id,g0,g1,g4) values(1000,5000,171223,1,3)""")
            except:
                pass
            for i in code_listg:
                try:
                    if i in ["s3"]:#该列需用text格式储存数据
                        await V.execute("alter table "+ggid+" add column "+i+" text")
                    else:#该列需用int格式储存数据
                        await V.execute("alter table "+ggid+" add column "+i+" int")
                except:
                    pass
            await V.update(1000,ggid,"g0",version)

    #判断表G5000是否存在此uid
    temp_1=await V.selecting(id[0],"G5000","user_id")
    if temp_1[0]==0 and id[0]:
        await V.execute("insert into G5000 (user_id,group_id) values ("+str(id[0])+",5000)")

    #判断该uid在G5000是否为最新版
    ao=await V.selecting(id[0],"G5000","a0")
    if ao[0]!=version:
        print("判断该uid在G5000是否为最新版")
        a1=await V.selecting(id[0],"G5000","a1")
        a6=await V.selecting(id[0],"G5000","a6")
        for i in code_lista:
            if i=="a1" and a1[0]==0:#好友黑白名单
                await V.update(id[0],"G5000","a1",1)
            elif i=="a6" and a6[0]==0:#相遇日子（原优先）
                await V.update(id[0],"G5000","a6",stamp[4])
        await V.update(id[0],"G5000","a0",version)

    #判断表G****是否存在此uid
    temp_2=await V.selecting(id[0],ggid,"user_id")
    if temp_2[0]==0:
        await V.execute("insert into "+ggid+" (user_id,group_id) values ("+str(id[0])+","+str(id[1])+")")

    #判断该uid在G****是否为最新版
    go=await V.selecting(id[0],ggid,"g0")
    if go[0]!=version:
        print("判断该uid在G****是否为最新版")
        for i in code_listg:
            if i=="a1" :#and a1[0]==0:#好友黑白名单
                await V.update(id[0],"G5000","a1",1)
        await V.update(id[0],ggid,"g0",version)





#==============================================================================
#普通的初始化
if not os.path.exists(FP+"/tea"):
    os.chdir(FP)
    os.makedirs("tea")
tea_db=sql.connect(FP+"/tea/tea_data.db")
tea_cur=tea_db.cursor()
try:
    tea_cur.execute("""select * from G5000""")
    GV=tea_cur.fetchall()#global variable
except sql.OperationalError:
    tea_cur.execute("""create table G5000
                    (user_id integer primary key autoincrement not null,
                    group_id int not null,
                    a0 int)""")

    tea_cur.execute("""insert into G5000(user_id,group_id,a0)
                    values(1000,5000,171223)""")
tea_cur.execute("select a0 from G5000 where user_id==1000")
for tea_row in tea_cur:
        A0=tea_row[0]
if A0!=version:
    for i in code_lista:
        try:
            if i in ["a3","a4","a5"]:
                tea_cur.execute("alter table G5000 add column "+i+" text")
            else:
                tea_cur.execute("alter table G5000 add column "+i+" int")
        except:
            pass
    tea_cur.execute("update G5000 set a0="+str(version)+" where user_id==1000")
tea_db.commit()
tea_db.close()
with open(FP+"/tea/friend_list.json","r",encoding='utf-8') as tea_json:
            friend_list=json.load(tea_json)
            tea_json.close()