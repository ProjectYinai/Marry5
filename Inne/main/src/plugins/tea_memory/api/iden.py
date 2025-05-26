import os
async def iden_def(bot, event, matcher,stamp,id,SP):
    global tea_db,tea_cur
    uid=id[0]
    gid=id[1]
    mid=id[2]
    puid="P"+str(uid)
    ggid="G"+str(gid)
    global friend_list
    
    #是否为好友
    if puid in friend_list:
        friend=1
    else:
        friend=0
    #是否为个人白名单
    a1=await V.selecting(uid,"G5000","a1")
    idenP=a1[0]
    #是否为群白名单
    if not gid:
        idenG=1
    else:
        g1=await V.selecting(1000,ggid,"g1")
        g2=await V.selecting(1000,ggid,"g2")
        if g2[0]==1:
            idenG=1
        elif g2[0]==2:
            idenG=2
        else:
            idenG=0
        if g1[0]==0:
            idenG=-1
    #群内是否存在辅助机
    if os.path.exists(SP+"/tea/group/"+str(gid)+".json"):
        getsize=os.path.getsize(SP+"/tea/group/"+str(gid)+".json")
        if getsize>=256:
            idenSub=1
        else:
            os.remove(SP+"/tea/group/"+str(gid)+".json")
            idenSub=0
    else:
        idenSub=0

    return([friend,idenP,idenG,idenSub])