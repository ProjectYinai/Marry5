import sqlite3 as sql
import globe

from . import api
#========
global stamp,cfg
stamp=api.stamp()
cfg=api.cfg()
tea_db=sql.connect(FP+"/tea/tea_data.db")
tea_cur=tea_db.cursor()

async def sql_select(uid,table,column):
    try:
        selection=tea_cur.execute(f"select {column} from {table} where user_id=={uid}")
        for row in selection:
            feedback.append(row[0])
            break
    except:
        feedback=[]
    if len(feedback)==0 or str(feedback[0])=="None" or feedback[0]==None:
        feedback=[0]
    tea_db.commit() 
    return(feedback)

async def sql_update_int(uid,ggid,code,value):
    tea_cur.execute(f"update {ggid} set {code}={value} where user_id=={uid}")
    tea_db.commit() 
 
async def sql_update_text(uid,ggid,code,value):
    tea_cur.execute(f"update {ggid} set {code}='{value}' where user_id=={uid}")
    tea_db.commit() 
    
async def execute(code):
    feedback=tea_cur.execute(code)
    tea_db.commit()
    return(feedback)