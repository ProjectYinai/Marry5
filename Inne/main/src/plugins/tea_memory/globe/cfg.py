from nonebot import get_driver

def cfg_def():
    env=get_driver().config
    MG=env.MAINGROUP#main group 主群
    BG=env.BACKGROUP#background group 后台群
    AG=env.ADMINGROUP#admin group 管理权限群
    SU=env.SUPERUSERS
    MB=env.MAINBOT#主bot号
    SB=env.SUBBOT#辅助bot号
    #=======
    #下列为文本
    SP=env.SCRIPTPATH#默认路径
    #=======
    #简易汇总
    cfg={"MG":MG,"BG":BG,"AG":AG,"SU":SU,"MB":MB,"SB":SB,"SP":SP}
    return(cfg)