import json
import random
import re
import time
import urllib
import os

#========
import sqlite3 as sql

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
from . import globe,sqlite,api,schedule

script_path = os.path.split(os.path.realpath(__file__))[0]
data_path = f'{script_path}\\tea_data.db'
#========

#================


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





