import sqlite3
import os
script_path = os.path.split(os.path.realpath(__file__))[0]
from .const import *
import api
connection = sqlite3.connect(f'{script_path}/tea_data.db')
cursor = connection.cursor()
def sql(query,args=()) -> list:
    """这只是一个对sql进行简单封装的函数，确保每句sql都被预处理，不被坏人入侵"""
    cursor.execute(query, args)
    rows = cursor.fetchall()
    connection.commit()
    return rows
def getLove(uid:int) -> tuple:
    """
    lv,nick,love,name,teatimes,greettimes,meettime
    获取一系列与好感度有关的信息，他们分别是
    等级，等级计算出来的头衔，好感度，昵称，泡茶总次数，问好总次数，相遇时间
    """
    uid=int(uid)
    query = f'SELECT love, name, etea, egreet, meet FROM user where uid== ?'
    args=(uid,)
    cursor.execute(query, args)
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        name = '店长' if row[1] in [0,'0',None] else row[1]
        lv,nick = api.lv(row[0],name)
        return lv,nick,row[0],name,row[2],row[3],row[4]
def getWhite(uid:int) -> int:
    """获取白名单等级，0位黑名单，1为普通用户"""
    return sql("select white from user WHERE uid == ?",(uid,))[0][0]
def addTeaTimes() -> None:
    """为当天的茉莉杯数+1，隔天则重置"""
    day = api.stamp_def()[4]
    query = f"UPDATE user SET teatime = ?, etea = CASE WHEN teatime = ? THEN etea + 1 ELSE 1 END WHERE uid = 1;"
    cursor.execute(query,(day,day))
    connection.commit()
def getTeaTimes() -> int:
    """获取今天的总杯数"""
    query = f'SELECT etea FROM user where uid== 1'
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.commit()
    for row in rows:
        return row[0]
    
#用户数据表不存在则创建
sql("""CREATE TABLE IF NOT EXISTS user (
        uid      INTEGER PRIMARY KEY,
        white    INTEGER DEFAULT (1) NOT NULL,
        love     INTEGER DEFAULT (0) NOT NULL,
        name     TEXT,
        prename  TEXT,
        nametime INTEGER DEFAULT (0) NOT NULL,
        meet     INTEGER DEFAULT (0) NOT NULL,
        etea     INTEGER DEFAULT (0) NOT NULL,
        egreet   INTEGER DEFAULT (0) NOT NULL,
        teatime  INTEGER DEFAULT (0) NOT NULL,
        greetime INTEGER DEFAULT (0) NOT NULL,
        ifgreet  INTEGER DEFAULT (0) NOT NULL
    )""")
sql("""CREATE TABLE IF NOT EXISTS auth (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        uid  INTEGER NOT NULL,
        gid  INTEGER NOT NULL,
        time INTEGER NOT NULL
    );""")
#茉莉的初始化数据行
sql(f"""INSERT OR IGNORE INTO user (
        uid
    ) values (
        1
    )""")

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