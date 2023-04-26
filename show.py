import json  # 导入JSON库
import sqlite3  # 导入SQLite库


# 定义一个函数，用于执行SQL语句并返回结果
def execute_sql(sql, db_file='mydatabase.db'):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()  # 获取游标
    cursor.execute(sql)  # 执行SQL语句
    rows = cursor.fetchall()  # 获取所有的查询结果
    cursor.close()  # 关闭游标
    conn.close()  # 关闭数据库连接
    return rows  # 返回查询结果


# 从JSON文件中读取查询语句和相应的文字描述
with open('queries.json', 'r', encoding='utf-8') as f:
    queries = json.load(f)

# 遍历数组，执行查询并输出结果
for query in queries:
    result = execute_sql(query['sql'])  # 执行SQL语句并获取结果
    print(query['description'])  # 输出文字描述作为标题
    print('-' * 40)  # 打印分割线
    for row in result:
        print(row)  # 逐行输出查询结果
    print('-' * 40)  # 打印分割线
