from . import sqlite,globe
import sqlite3 as sql
import os 

VER=globe.cfg.VER#获取env中的版本号
script_path = os.path.split(os.path.realpath(__file__))[0]
data_path=script_path+"\\tea_data.db"
conn=sql.connect(data_path)
cursor=conn.cursor()
#获取db中的版本号
cursor.execute("SELECT O1 FROM G0 WHERE uid=1000;")
tables=cursor.fetchall()
version=[table[0] for table in tables]
if version[0]!=VER:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=cursor.fetchall()
    table_names = [table[0] for table in tables if len(table[0])>=7]
    column_names = open(f"{script_path}/column_names.json",encoding="UTF-8").read()#列名和数据类型
    for table_name in table_names:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        existing_columns = [col[1] for col in columns]
        for column_name in column_names:
            if column_name[0] not in existing_columns:
                # 如果列不存在，则添加新列
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name[0]} {column_name[1]} NOT NULL")
            else:
                pass
    conn.commit()    
conn.close()        
