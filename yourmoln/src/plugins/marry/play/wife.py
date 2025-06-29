import time,random,re,urllib,os
from PIL import Image
rc = random.choice
from nonebot.adapters import Bot, Message
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import data,api

script_path = os.path.split(os.path.realpath(__file__))[0]

async def roll(bot:Bot, e:GroupMessageEvent) -> Message:
    gm = await api.myGroupMembers(gid=e.group_id)
    cgm=[]
    for i in range(2):
        for i in range(len(gm)):
            if (int(time.time()) - gm[i][2]) > 3600*48:
                break
            if (int(time.time()) - gm[i][2]) < 3600*12:
                cgm += [gm[i]]*3
            elif (int(time.time()) - gm[i][2]) < 3600*24:
                cgm += [gm[i]]*2
            elif (int(time.time()) - gm[i][2]) < 3600*48:
                cgm += [gm[i]]*1
        if len(cgm) == 0:
            gm = await api.myGroupMembers(gid=e.group_id,nc=True)
        else: break

    if str(e.message) == "抽群老婆":
        qid,name,sendtime = rc(cgm)
        img=f"http://q1.qlogo.cn/g?b=qq&nk={str(qid)}&s=100"
        res=[{"type":"reply","data":{"id":str(e.message_id)}},
            {"type":"text","data":{"text":"今天你亲爱的群老婆是："}},
            {"type":"image","data":{"file":img}},
            {"type":"text","data":{"text":f"{"[UP!]" if (int(time.time()) - sendtime) < 3600*3 else ""}【{name}】({qid})哒！" }}]
    elif str(e.message) in ["抽群老婆十连","群老婆十连"]:
        res=[{"type":"reply","data":{"id":str(e.message_id)}},
            {"type":"text","data":{"text":"今天你亲爱的群老婆是：\n"}}]+[
            {"type":"text","data":
             {"text":f"{"[UP!]" if (int(time.time()) - (w:=rc(cgm))[2]) < 3600*3 else ""}【{w[1]}】\n"}} for i in range(10)]+[
            {"type":"text","data":{"text":"这十个哒！"}}  
            ]
    return res

async def rank(bot:Bot, e:GroupMessageEvent) -> Message:
    uid,gid=e.user_id,e.group_id
    ggid="G"+str(gid)
    s1_info=data.sql(f"select user_id,s1 from {ggid} where s1>=1 order by s1 desc")
    s1_list=[]
    for row in s1_info:
        s1_list.append(row)
    if len(s1_list)<=5:
        return api.reply(e,"( 〞 0 ˄ 0 )错误代码：E-1。\n排行榜数据过少，当前群老婆数为"+str(len(s1_list))+"名，到达6名后即可使用排行榜功能！")
    index_u=-1
    for i in range(len(s1_list)):
        if s1_list[i][0]==uid:
            index_u=i
            break
    gm = await api.myGroupMembers(gid)
    gm = dict(map(lambda x: x[:2],gm))
    #第一名
    rank_1_card=s1_list[0][0]
    a=f"1.【{gm[rank_1_card]}】"+str(s1_list[0][1] )+"次"
    #第二名
    rank_2_card=s1_list[1][0]
    b=f"2.【{gm[rank_2_card]}】"+str(s1_list[1][1])+"次"
    #第三名
    rank_3_card=s1_list[2][0]
    c=f"3.【{gm[rank_3_card]}】"+str(s1_list[2][1])+"次"
    #第四名
    rank_4_card=s1_list[3][0]
    d=f"4.【{gm[rank_4_card]}】"+str(s1_list[3][1])+"次"
    #第五名
    rank_5_card=s1_list[4][0]
    e5=f"5.【{gm[rank_5_card]}】"+str(s1_list[4][1])+"次"
    try:
        f=f"你的排名\n{index_u+1}.【{gm[uid]}】"+str(s1_list[index_u][1])+"次"
        return api.reply(e,f"==群老婆排行榜==\n{a}\n{b}\n{c}\n{d}\n{e5}\n{f}") 
    except:
        return api.reply(e,f"==群老婆排行榜==\n{a}\n{b}\n{c}\n{d}\n{e5}") 

async def marry(bot:Bot, e:GroupMessageEvent) -> Message:
    """旧代码移植"""
    msg = str(e.raw_message)
    mqid = re.findall("[0-9]{5,11}",msg)
    if len(mqid)==0:
        return api.reply(e,f"{msg}( 〞 0 ˄ 0 )错误代码：E5-1_n_请加上艾特对象！")
    mqid=mqid[0]
    #获取娶群老婆时间戳
    t3 = data.sql(f"SELECT t3 FROM G{e.group_id} where user_id = ?",(e.user_id,))[0][0]
    t3 = t3 if t3 != None else 0
    stamp = api.stamp_def()
    if t3<=stamp[2]:
        try:
            a = await bot.get_group_member_info(group_id=e.group_id,user_id=e.user_id,no_cache=False)
            b = await bot.get_group_member_info(group_id=e.group_id,user_id=mqid,no_cache=False)
        except:
            return api.reply(e,"( 〞 0 ˄ 0 )错误代码：E5-2_n_对象不在此群中！")
        card_a = a["card"] if a["card"] != "" else a["nickname"]
        card_b = b["card"] if b["card"] != "" else b["nickname"]
        #======== 
        #回复的消息
        urllib.request.urlretrieve("http://q1.qlogo.cn/g?b=qq&nk="+str(e.user_id)+"&s=100",f"{script_path}/temp/img_a.png")
        urllib.request.urlretrieve("http://q1.qlogo.cn/g?b=qq&nk="+str(mqid)+"&s=100",f"{script_path}/temp/img_b.png")
        img_a=Image.open(f"{script_path}/temp/img_a.png")
        img_acopy=img_a.copy()
        img_b=Image.open(f"{script_path}/temp/img_b.png")
        img_bcopy=img_b.copy()
        img_white=Image.open(f"{script_path}/temp/img_white.png")
        img_white.paste(img_acopy,(0,0))
        img_white.paste(img_bcopy,(100,0))
        img_white.save(f"{script_path}/temp/img_white.png")
        img_save=f"file:///{script_path}/temp/img_white.png"
        if int(e.user_id)==int(mqid):
            msg_1={"type":"text","data":{"text":"~婚礼现场~"}}
            msg_2={"type":"image","data":{"file":img_save}}
            if stamp[0]%2==0 or 1:
                msg_3={"type":"text","data":{"text":"(*ﾟーﾟ)自己娶自己是什么操作啦，虽然确实可以这要做就是了。"}}
            else:
                msg_3={"type":"text","data":{"text":"(*ﾟ∇ﾟ)祝【店长】的头像角色会成为你真正的老婆~"}}
            msg_0=[{"type":"reply","data":{"id":str(e.message_id)}},msg_1,msg_2,msg_3]    
        else:
            msg_1={"type":"text","data":{"text":"~婚礼现场~"}}
            msg_2={"type":"image","data":{"file":img_save}}
            msg_3={"type":"text","data":{"text":f"(*ﾟ∇ﾟ)祝【{card_a}】和【{card_b}】百年好合~"}}
            msg_0=[{"type":"reply","data":{"id":str(e.message_id)}},msg_1,msg_2,msg_3]
        #========
        #写入抽中次数与时间
        t3 = data.sql(f"UPDATE G{e.group_id} SET s1 = s1 + 1, t3 = ? WHERE user_id = ?;",(stamp[2]+30,e.user_id))
        return msg_0
    else:
        last_time=t3-stamp[2]
        msg_0=api.reply(e,f"( ｣ﾟДﾟ)｣＜还在转cd，\n冷却时间{last_time}分！")
        return msg_0
        
