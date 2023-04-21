import sqlite3
import pymysql

# 连接SQLite数据库
conn_sqlite = sqlite3.connect('mydatabase.db')
cur_sqlite = conn_sqlite.cursor()

# 查询数据
cur_sqlite.execute('SELECT * FROM tender')
rows = cur_sqlite.fetchall()

# 关闭SQLite数据库连接
cur_sqlite.close()
conn_sqlite.close()

# 连接MySQL数据库
conn_mysql = pymysql.connect(
    host="tc.51insight.top",
    user="chaos",
    password="EFzmGSJz4Gw5ePPs",
    database="mydatabase"
)
cur_mysql = conn_mysql.cursor()

# 插入数据
total_rows = len(rows)
for i, row in enumerate(rows, 1):
    cur_mysql.execute(
        'INSERT INTO tender (id, href, title, area, post_date, has_crawled, html, created_at, updated_at, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        row)
    # 显示进度
    percentage = i / total_rows * 100
    progress_str = f'{i}/{total_rows} ({percentage:.2f}%)'
    bar_width = 20
    filled_bar_width = int(percentage / 100 * bar_width)
    remaining_bar_width = bar_width - filled_bar_width
    progress_bar = f"[{'=' * filled_bar_width}{' ' * remaining_bar_width}]"
    print(f'\r{progress_str} {progress_bar}', end='')

# 提交更改并关闭连接
conn_mysql.commit()
cur_mysql.close()
conn_mysql.close()
