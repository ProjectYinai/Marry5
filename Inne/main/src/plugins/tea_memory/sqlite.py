import sqlite3 as sql
import os,json

from . import api,globe
#========
global stamp,cfg
stamp=globe.stamp.stamp
cfg=globe.cfg.cfg
VER=globe.cfg.VER#获取env中的版本号
tea_db=sql.connect(cfg["SP"]+"/tea/tea_data.db")
tea_cur=tea_db.cursor()

async def update_uid(bot, event,matcher,id,iden):
    pass


async def select(uid,table,column):
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

async def update_int(uid,ggid,code,value):
    tea_cur.execute(f"update {ggid} set {code}={value} where user_id=={uid}")
    tea_db.commit() 
 
async def update_text(uid,ggid,code,value):
    tea_cur.execute(f"update {ggid} set {code}='{value}' where user_id=={uid}")
    tea_db.commit() 
    
async def execute(code):
    feedback=tea_cur.execute(code)
    tea_db.commit()
    return(feedback)

#获取db中的版本号
tea_cur.execute("SELECT O1 FROM G0 WHERE user_id=1000;")
tables=tea_cur.fetchall()
version=[table[0] for table in tables]
if version[0]!=VER:
    print("update_version")
    tea_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=tea_cur.fetchall()
    table_names = [table[0] for table in tables if len(table[0])>=7]
    del table_names[0]
    SP=cfg["SP"]
    with open(f"{SP}/tea/column_names.json",encoding="UTF-8") as json_column_names:
        column_names = json.load(json_column_names)
        json_column_names.close()
        #列名和数据类型
    
    for table_name in table_names:
        if table_name=="G555679990" or table_name=="G1000":
            tea_cur.execute(f"PRAGMA table_info({table_name})")
            columns = tea_cur.fetchall()
            existing_columns = [col[1] for col in columns]
            print(existing_columns)
            print(column_names)
            for column_name in column_names:
                if column_name[0].lower() not in existing_columns and column_name[0].upper() not in existing_columns :
                    # 如果列不存在，则添加新列
                    tea_cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name[0]} {column_name[1]} NOT NULL DEFAULT 0")
                else:
                    pass
    tea_cur.execute(f"update G0 set O1={VER} where user_id==1000")
tea_db.commit()
        
 