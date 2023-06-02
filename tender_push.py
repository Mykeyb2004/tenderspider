import sqlite3
import os
from datetime import datetime
from tools import send_dingtalk


class TenderPush:

    def __init__(self, db_file='mydatabase.db'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(script_dir, db_file)
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def split_array(push_list):
        MAX_SIZE = 15000  # 每个子数组的最大大小

        result_list = []  # 存储切割后的子数组

        left, right = 0, 0
        current_bytes_sum = 0
        for right, string in enumerate(push_list):
            string_bytes = len(string.encode('utf-8'))
            if current_bytes_sum + string_bytes > MAX_SIZE:
                # 当前子数组的大小超出限制，将其加入结果列表
                result_list.append(push_list[left:right])
                left = right
                current_bytes_sum = string_bytes
            else:
                current_bytes_sum += string_bytes

        if left < right:
            # 处理最后一个子数组
            result_list.append(push_list[left:right])

        return result_list

    def push(self, limit=10):
        # 扫描所有字段 has_crawled>=1 的数据
        print("Scanning records...")
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        print(f"Today is {today}.")

        sql = f"SELECT id, title, weight, href FROM tender WHERE post_date= '{today}' and weight > 0 " \
              f"order by weight limit {limit} offset(SELECT count(*) FROM tender WHERE post_date= '{today}' " \
              f"and weight > 0 ) - {limit};"
        rows = self.cursor.execute(sql).fetchall()

        push_list = []
        for i, row in enumerate(rows):
            id, title, weight, href = row
            push_list.append(f"{i + 1}. {title}，{weight}，{href}")

        # 发送钉钉消息
        if len(push_list) > 0:
            print("Sending dingtalk message...")
            send_msgs = self.split_array(push_list)
            print(f"共计{len(send_msgs)}信息.")
            for msg in send_msgs:
                # print("\n".join(msg))
                send_dingtalk("\n".join(msg))
        else:
            print("No records found.")


if __name__ == '__main__':
    tender_push = TenderPush()
    tender_push.push(200)
