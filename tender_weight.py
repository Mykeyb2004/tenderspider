import sqlite3
import html2text
import re
from datetime import datetime
import os


class TenderWeightCalculator:
    def __init__(self, db_file='mydatabase.db'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(script_dir, db_file)

    def count_weight(self, target_text, conn):
        cursor = conn.cursor()
        # 遍历词汇表中的每个单词，并将匹配的 w 值进行累加
        total_weight = 0
        for row in cursor.execute("SELECT word, w FROM dictionary"):
            if re.search(row[0], target_text):
                print("匹配到关键词：", row[0], "，w 值为：", row[1])
                total_weight += row[1]

        # 返回总 w 值汇总分数
        return total_weight

    def update_tender_weight(self, refresh_all=False):
        # 连接 SQLite 数据库
        conn = sqlite3.connect(self.db_file)

        # 扫描所有字段 has_crawled>=1 的数据
        print("Scanning records...")
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        if refresh_all:  # 刷新所有数据
            sql = f"SELECT id, title, weight, href, html FROM tender WHERE has_crawled >= 1"
        else:  # 只刷新今天的数据
            sql = f"SELECT id, title, weight, href, html FROM tender WHERE post_date = '{today}' AND " \
                  f"has_crawled >= 1 AND weight is null"
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        print(f"Found {len(rows)} records.")

        # 逐条将字段 html 的内容转为纯文字，并把 weight 累加起来
        print("Updating record weights...")

        for i, row in enumerate(rows):
            id, title, weight, href, html = row
            # print(row)
            if html:
                text = html2text.html2text(html)
                total_weight = self.count_weight(title + text, conn)

                print(f"{i + 1}. 标题：{title}，权重值：{total_weight}，链接：{href}")

                # 更新 tender 表 weight 字段的值
                sql = f"UPDATE tender SET weight = {total_weight} WHERE id = {id}"
                conn.execute(sql)

        # 提交事务
        conn.commit()
        print("Update complete.")

        # 关闭数据库连接
        conn.close()


if __name__ == '__main__':
    print("Updating tender weights...")
    tender_calc = TenderWeightCalculator()
    tender_calc.update_tender_weight(refresh_all=False)
