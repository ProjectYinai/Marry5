import os
from . import schedule,sqlite

async def id(bot, event, matcher):
    code=[0,0,0]
    if str(event.post_type)=="message":
        if str(event.message_type)=="private":
            code=[1,0,1]
        elif str(event.message_type)=="group" and str(event.sub_type)=="normal":
            code=[1,1,1]
        elif str(event.message_type)=="group" and str(event.sub_type)=="notice":
            code=[0,1,0]
    elif str(event.post_type)=="notice":
        if "group" in str(event.notice_type):
            code=[0,1,0]
    elif str(event.post_type)=="request":
        if str(event.request_type)=="friend":
            code=[1,0,0]
        elif str(event.request_type)=="group":
            code=[1,1,0]
    id=[]
    for i in range(3):
        if code[i]==1:
            if i==0:
                id.append(int(event.user_id))
            elif i==1:
                id.append(int(event.group_id))
            elif i==2:
                id.append(int(event.message_id))
        else:
            id.append(0)
    return(id)

async def iden(bot, event, matcher,stamp,id):
    uid=id[0]
    gid=id[1]
    mid=id[2]
    puid="P"+str(uid)
    ggid="G"+str(gid)
    friend_list=schedule.schedule.friend_list()
    #是否为好友
    if puid in friend_list:
        friend=1
    else:
        friend=0
    #是否为个人白名单
    a1=await sqlite.select(uid,"G5000","a1")
    idenP=a1[0]
    #是否为群白名单
    if not gid:
        idenG=1
    else:
        g1=await sqlite.select(1000,ggid,"g1")
        g2=await sqlite.select(1000,ggid,"g2")
        if g1[0]:
            idenG=1
        else:
            idenG=0
        if g2[0]:
            authG=1
        else:
            authG=0


    return([friend,idenP,idenG,authG])

