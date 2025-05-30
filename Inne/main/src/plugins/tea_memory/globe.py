from nonebot import get_driver
import time

def overall():
    stamp=stamp_def()
    cfg=cfg_def()
    return(stamp,cfg)
    
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

def stamp_def():
    birthday=1513972500
    time_stamp=int(time.time())
    time_interval=time_stamp-birthday
    time_stamp_sec=int(time_interval)
    time_stamp_min=int(time_interval/60)
    time_stamp_hour=int(time_interval/3600)
    time_stamp_day=int(time_interval/86400)
    
    birthday="2017-12-23"
    time_stamp_mon=0#rrule.rrule(rrule.MONTHLY,dtstart=parse("2017-12-23"),until=datetime.date.today()).count()
    time_stamp_year=0#rrule.rrule(rrule.YEARLY,dtstart=parse("2017-12-23"),until=datetime.date.today()).count()


    time_local_yday=int(time.localtime().tm_yday)
    time_local_wday=int(time.localtime().tm_wday)
    time_local_sec=int(time.localtime().tm_sec)
    time_local_min=int(time.localtime().tm_min)
    time_local_hour=int(time.localtime().tm_hour)
    time_local_mday=int(time.localtime().tm_mday)
    time_local_mon=int(time.localtime().tm_mon)
    time_local_year=int(time.localtime().tm_year)

    stamp=[time_stamp,
    time_stamp_sec,
    time_stamp_min,
    time_stamp_hour,
    time_stamp_day,
    time_stamp_mon,
    time_stamp_year,
    time_local_yday,
    time_local_wday,
    time_local_sec,
    time_local_min,
    time_local_hour,
    time_local_mday,
    time_local_mon,
    time_local_year]

    return(stamp)