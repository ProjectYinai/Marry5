import json,os,random
from datetime import datetime
script_path = os.path.split(os.path.realpath(__file__))[0]
json_data = open(f"{script_path}/hi.json",encoding="UTF-8").read()
# 解析JSON为字典
greeting_dict = json.loads(json_data)
rc = random.choice

from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

def get_current_greeting_types():
    """获取当前时间段可用的问候类型列表"""
    current_hour = datetime.now().hour
    available_types = []
    
    for greeting in greeting_dict.values():
        if current_hour in greeting['range']:
            available_types.append(f"[{greeting['type']}]")
            available_types.append("和")
    return available_types[:-1]

def hi(e:GroupMessageEvent):
    msg=str(e.get_message())
    current_hour = datetime.now().hour
    
    # 检查输入的问候类型是否在当前时间范围内
    matched_greeting = None

    for greeting in greeting_dict.values():
        if greeting['type'] == msg:
            if current_hour in greeting['range']:
                matched_greeting = greeting
                break
            else:
                # 如果问候类型不在当前时间范围内，返回当前可用的问候类型列表
                res = f"(*ﾟーﾟ)【店长】，现在是{"".join(get_current_greeting_types())}的时间呢~"
                name = '店长'
                res = res.replace('_n_','\n').replace('【店长】',name)
                return res

    
    # 从normalN消息组中随机选择一条消息
    messages = matched_greeting['message']['normalN']
    if not messages:  # 如果normalN为空，使用其他可用的消息组
        for season in ['normalS', 'normalR', 'springN', 'summerN', 'autumnN', 'winterN']:
            if greeting_dict['message'][season]:
                messages = greeting_dict['message'][season]
                break
    
    res = rc(messages)[0]  # 获取消息内容
    ###########凌晨3点半了，燃尽了还没改##################
    name = '店长'
    res = res.replace('_n_','\n').replace('【店长】',name)
    num = 35
    lv = 100
    nick = "值得信赖的伙伴"
    res = f"[Lv.{lv}/0x{lv:x}-{nick}]\n{res}\n[好感度+{num}]"
    ########################################
    return res