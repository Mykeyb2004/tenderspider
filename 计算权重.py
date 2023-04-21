import sqlite3
import html2text
import re


def count_weight(target_text, conn):
    cursor = conn.cursor()
    # 遍历词汇表中的每个单词，并将匹配的 w 值进行累加
    total_weight = 0
    for row in cursor.execute("SELECT word, w FROM dictionary"):
        if re.search(row[0], target_text):
            print("匹配到关键词：", row[0], "，w 值为：", row[1])
            total_weight += row[1]

    # 返回总 w 值汇总分数
    return total_weight


def update_tender_weight(conn):
    # 创建表 keyword
    sql = '''
    CREATE TABLE IF NOT EXISTS dictionary (
        id INTEGER PRIMARY KEY,
        word TEXT,
        w INTEGER
    )
    '''
    conn.execute(sql)

    # 扫描所有字段 has_crawled>=1 的数据
    print("Scanning records...")
    # sql = "SELECT id, html FROM tender WHERE has_crawled >= 1 AND weight = 0"
    sql = "SELECT id, html FROM tender WHERE has_crawled >= 1"
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    print(f"Found {len(rows)} records.")

    # 读取 dictionary 表
    print("Reading keywords...")
    sql = "SELECT word, w FROM dictionary"
    cursor = conn.execute(sql)
    keyword_rows = cursor.fetchall()
    keywords = {row[0]: row[1] for row in keyword_rows}

    # 逐条将字段 html 的内容转为纯文字，并把 weight 累加起来
    print("Updating record weights...")
    for i, row in enumerate(rows):
        id, html = row
        text = html2text.html2text(html)
        weight = count_weight(text, conn)
        if weight > 0:
            print(f"id = {id} weight={weight}\n{text[:100]}... ")

        # 更新 tender 表 weight 字段的值
        id = row[0]
        sql = f"UPDATE tender SET weight = {weight} WHERE id = {id}"
        conn.execute(sql)

    # 提交事务
    conn.commit()
    print("Update complete.")


# 连接 SQLite 数据库
conn = sqlite3.connect('mydatabase.db')
# 更新 tender 表的 weight 字段
update_tender_weight(conn)
# 关闭数据库连接
conn.close()
