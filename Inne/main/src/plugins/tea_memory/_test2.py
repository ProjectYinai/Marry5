import os,sys,sqlite3

script_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(script_path)
db_path = f'{script_path}\\tea_data.db'  # 替换为你的数据库文件路径
db_path_new = f'{script_path}\\tea_data_2.db'
def get_table_names(db_path):
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 执行查询以获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # 提取表名并返回
    table_names = [table[0] for table in tables]
    
    # 关闭连接
    conn.close()
    
    return table_names

# 示例用法

#table_names = get_table_names(db_path)
#print("Tables in the database:", table_names)


#================
def get_column_data(db_path, table_name, column_name):
    # 连接到SQLite数据库
    conng = sqlite3.connect(db_path)
    cursorg = conng.cursor()
    
    # 执行查询以获取指定表和列的数据
    queryg = f"SELECT {column_name} FROM {table_name}"
    cursorg.execute(queryg)
    datag = cursorg.fetchall()
    
    # 提取列数据并返回
    column_data = [row[0] for row in datag]
    
    # 关闭连接
    conng.close()
    
    return column_data

# 示例用法




def create_database_and_table(db_path_new, table_name, columns):
    # 连接到SQLite数据库（如果数据库不存在，则会自动创建）
    conn = sqlite3.connect(db_path_new)
    cursor = conn.cursor()
    
    # 构建CREATE TABLE语句
    columns_with_types = ", ".join([f"{col} {data_type} NOT NULL" for col, data_type in columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"
    db_path = f'{script_path}\\tea_data.db'
    uid=get_column_data(db_path, 'g5000', 'user_id')
    gid=get_column_data(db_path, 'g5000', "group_id")
    a1=get_column_data(db_path, 'g5000', "a1")
    a2=get_column_data(db_path, 'g5000', "a2")
    a3=get_column_data(db_path, 'g5000', "a3")
    a4=get_column_data(db_path, 'g5000', "a4")
    a5=get_column_data(db_path, 'g5000', "a5")
    a6=get_column_data(db_path, 'g5000', "a6")
    a7=get_column_data(db_path, 'g5000', "a7")
    a8=get_column_data(db_path, 'g5000', "a8")
    a9=get_column_data(db_path, 'g5000', "a9")
    a10=get_column_data(db_path, 'g5000', "a10")
    p1=get_column_data(db_path, 'g5000', "p1")

    # 执行CREATE TABLE语句
    
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully.")
    for i in range(len(uid)):
        if uid[i]==None:
            uidn=0
        else:
            uidn=uid[i]
        if gid[i]==None:
            gidn=0
        else:
            gidn=gid[i]
        if a1[i]==None:
            a1n=0
        else:
            a1n=a1[i]
        if a2[i]==None:
            a2n=0
        else:
            a2n=a2[i]
        if a3[i]==None:
            b1n=0
        else:
            b1n=a3[i]
        if a4[i]==None:
            b2n=0
        else:
            b2n=a4[i]
        if a5[i]==None:
            b3n=0
        else:
            b3n=a5[i]
        if a6[i]==None:
            a3n=0
        else:
            a3n=a6[i]
        if a7[i]==None:
            a4n=0
        else:
            a4n=a7[i]
        if a8[i]==None:
            a5n=0
        else:
            a5n=a8[i]
        if a9[i]==None:
            a6n=0
        else:
            a6n=a9[i]
        if a10[i]==None:
            a7n=0
        else:
            a7n=a10[i]
        
        cursor.execute(f"""insert into G1000(uid,gid,A1,A2,A3,A4,A5,A6,A7,B1,B2,B3,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,G1,G2,G3,G4,G5,H1,I1,I2,R1,S1,T1,T2,T3,T4) 
                    values({uidn},{1000},{a1n},{a2n},{a3n},{a4n},{a5n},{a6n},{a7n},'{b1n}','{b2n}','{b3n}',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'0',0,0,0,'0',0,0,0,0)""")
    # 提交更改并关闭连接
    conn.commit()
    conn.close()

# 示例用法
  # 替换为你的数据库文件路径
table_name = 'G1000'
columns = [("uid", "INTEGER"), 
           ("gid", "INTEGER"), 
           ("A1", "INTEGER"), 
           ("A2", "INTEGER"),
           ("A3", "INTEGER"),
           ("A4", "INTEGER"),
           ("A5", "INTEGER"),
           ("A6", "INTEGER"),
           ("A7", "INTEGER"), 
           ("B1", "TEXT"),
           ("B2", "TEXT"),
           ("B3", "TEXT"), 
           ("C1", "INTEGER"),
           ("C2", "INTEGER"),
           ("C3", "INTEGER"),
           ("C4", "INTEGER"),
           ("C5", "INTEGER"),
           ("C6", "INTEGER"),
           ("C7", "INTEGER"),
           ("C8", "INTEGER"),
           ("C9", "INTEGER"),
           ("C10", "INTEGER"),
           ("C11", "INTEGER"),
           ("C12", "INTEGER"),
           ("G1", "INTEGER"),
           ("G2", "INTEGER"),
           ("G3", "INTEGER"),
           ("G4", "INTEGER"),
           ("G5", "INTEGER"),
           ("H1", "TEXT"),
           ("I1", "INTEGER"),
           ("I2", "INTEGER"),
           ("R1", "INTEGER"),
           ("S1", "TEXT"),
           ("T1", "INTEGER"),
           ("T2", "INTEGER"),
           ("T3", "INTEGER"),
           ("T4", "INTEGER")]  # 列名和数据类型
    
create_database_and_table(db_path_new, table_name, columns)

