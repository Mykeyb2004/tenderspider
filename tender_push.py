import sqlite3
from datetime import datetime
from tools import send_dingtalk


class TenderPush:

    def __init__(self, db_file='mydatabase.db'):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def push(self, limit=10):
        # 扫描所有字段 has_crawled>=1 的数据
        print("Scanning records...")
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        sql = f"SELECT id, title, weight, href FROM tender WHERE post_date= '{today}' AND weight is not null " \
              f"order by weight desc limit {limit};"
        rows = self.cursor.execute(sql).fetchall()

        push_list = []
        for i, row in enumerate(rows):
            id, title, weight, href = row
            push_list.append(f"{i + 1}. {title}，w={weight}，url={href}")

        # 发送钉钉消息
        if len(push_list) > 0:
            send_dingtalk("\n".join(push_list))
        else:
            print("No records found.")


if __name__ == '__main__':
    tender_push = TenderPush()
    tender_push.push(100)
