class USER:
    #永久数据
    uid:int = 'uid'#qq号
    white:int = 'white'#白名单，1是好人
    love:int = 'love'#好感度
    nick:str = 'nick'#自定义昵称
    prenick:str = 'prenick'#未审核的昵称
    meet:int = 'meet'#相遇的日子
    everytea:int = 'etea'#所有喝茶的日子(为什么不叫alltea呢，因为我觉得每个tea的瞬间更浪漫)
    everygreet:int = 'everygreet'#所有问好的日子(同上)
    #临时数据
    teatime:int = 'teatime'#今天泡茉莉的时间
    greetime:int = 'greetime'#今天问好的时间，'00000000'表示都没问，问了变1

    #对于uid为1的数据来说
    #everytea表示所有人的喝茶的次数(暂时是还没有记录的，要是喜欢就以后统计一下吧)
    #teatime是所有人当天的喝茶次数
    #其它的也可以类推哦，uid1可以记录下茉莉自己的数据

LOVE = 'A2'
TIMES = 'p1'
LASTTIME = 'b1'
NAME = 'a4'
HILASTTIME="b11"
TEATIMES = 'A7'
MEETTIME = 'A6'
GREETTIMES = 'A8'
WHITELIST = 'a1'
#个人临时数据
# B1：个人泡茉莉时间戳/时间戳天
# B2：清晨好好时间戳/时间戳天
# B3：早上好时间戳/时间戳天
# B4：中午好时间戳/时间戳天
# B5：下午好时间戳/时间戳天
# B6：黄昏好时间戳/时间戳天
# B7：晚上好时间戳/时间戳天
# B8：午夜好时间戳/时间戳天
# B9：凌晨好时间戳/时间戳天
# B10：晚安时间戳/时间戳天
# B11：打招呼时间戳/时间戳天
# B12：自定义昵称时间戳/时间戳分