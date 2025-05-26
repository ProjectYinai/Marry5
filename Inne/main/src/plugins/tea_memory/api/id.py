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