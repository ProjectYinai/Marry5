class USER:
    #永久数据
    uid:int = 'uid'#qq号
    white:int = 'white'#白名单，1是好人
    love:int = 'love'#好感度
    name:str = 'name'#自定义昵称
    prename:str = 'prename'#未审核的昵称
    nametime:int = 'nametime'#改名cd
    meet:int = 'meet'#相遇的日子
    everytea:int = 'etea'#所有喝茶的日子(为什么不叫alltea呢，因为我觉得每个tea的瞬间更浪漫)
    everygreet:int = 'egreet'#所有问好的日子(同上)
    #临时数据
    teatime:int = 'teatime'#上次泡茉莉的时间
    greetime:int = 'greetime'#上次问好的时间
    ifgreet:int = 'ifgreet'#问好时间段100000000表示都没问，问了0变1，采用二进制转十进制的方式存储
    #对于uid为1的数据来说
    #everytea是所有人当天的喝茶次数
    #其它的也可以类推哦，uid1可以记录下茉莉自己的数据
class admin:
    group:list = ['947421516']#用于接收名字审核等通知
    id:list = ['3402824831','2373725901']#同意名字审核等权限,弃用,后续改为用white的数值代表权限等级
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