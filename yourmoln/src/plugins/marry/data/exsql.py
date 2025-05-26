import sqlite3
import os
script_path = os.path.split(os.path.realpath(__file__))[0]

import api
connection = sqlite3.connect(f'{script_path}/tea_data.db')
cursor = connection.cursor()
def sql(query,args=()) -> list:
    cursor.execute(query, args)
    rows = cursor.fetchall()
    connection.commit()
    return rows
def getLove(uid:int) -> tuple:
    uid=int(uid)
    """lv,nick,love,name"""
    query = 'SELECT A2, a4 FROM G5000 where user_id== ?'
    args=(uid,)
    cursor.execute(query, args)
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        name = '店长' if row[1] in [0,'0',None] else row[1]
        lv,nick = api.lv(row[0])
        return lv,nick,row[0],name
def addTeaTimes():
    day = api.stamp_def()[4]
    query = "UPDATE G5000 SET b1 = ?, p1 = CASE WHEN b1 = ? THEN p1 + 1 ELSE 1 END WHERE user_id = 1000;"
    cursor.execute(query,(day,day))
    connection.commit()
def getTeaTimes() -> int:
    query = 'SELECT p1 FROM G5000 where user_id== 1000'
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.commit()
    for row in rows:
        return row[0]
#数据库操作示例
"""
# 连接到SQLite数据库
connection = sqlite3.connect(f'{script_path}/example.db')
# 创建一个游标对象
cursor = connection.cursor()
# 创建一个表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER
)
''')
# 预编译插入语句
insert_query = 'INSERT INTO users (name, age) VALUES (?, ?)'
# 插入数据
users = [('Alice', 30), ('Bob', 25), ('Charlie', 35)]
cursor.executemany(insert_query, users)
# 提交事务
connection.commit()
# 查询数据
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
for row in rows:
    print(row)
# 关闭连接
connection.close()
"""