
import json
import random
import re
import time
import urllib
import os

#========
import sqlite3 as sql

from dateutil import rrule
from dateutil.parser import parse
import nonebot
import nonebot.drivers.aiohttp 


#========
_n="\n"
FP=str(os.getcwd())
FP=FP.replace(str(os.path.basename(os.getcwd())),"")
global tea_db,tea_cur
tea_db=sql.connect(FP+"tea\\tea_data.db")
tea_cur=tea_db.cursor()

async def selecting(uid,table,column):

    feedback=[]
    try:
        selection=tea_cur.execute("select "+column+" from "+table+" where user_id=="+str(uid))
        for row in selection:
            feedback.append(row[0])
            break
    except:
        pass
    if len(feedback)==0 or str(feedback[0])=="None":
        feedback=[0]
    tea_db.commit() 

    return(feedback)

async def select_nowhere(table,column):
    feedback=[]
    try:
        if len(column)==1:
            selection=tea_cur.execute("select "+column[0]+" from "+table)
        elif len(column)>=2:
            column_a=str(column[0])
            for i in range (len(column)):
                if i != 0:
                    column_a+=","+str(column[i])
            selection=tea_cur.execute("select "+column+" from "+table)
        for row in selection:
            feedback.append(row)
    except:
        pass
    if len(feedback)==0 or str(feedback[0])=="None":
        feedback=[0]
    return(feedback)

async def update(uid,ggid,code,value):
    tea_cur.execute("update "+str(ggid)+" set "+str(code)+"="+str(value)+" where user_id=="+str(uid))
    tea_db.commit() 
 
async def update_text(uid,ggid,code,value):
    tea_cur.execute("update "+str(ggid)+" set "+str(code)+"=\'"+str(value)+"\' where user_id=="+str(uid))
    tea_db.commit() 

async def execute(code):
    feedback=tea_cur.execute(code)
    tea_db.commit()
    return(feedback)