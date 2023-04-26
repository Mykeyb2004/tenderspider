# -*- coding: utf-8 -*-
import os
import sqlite3
import datetime
import requests
import json


def send_dingtalk(msg):
    """
    发送钉钉消息到指定群组或个人
    :param webhook_url: 钉钉机器人的 Webhook 地址
    :param msg: 发送的消息内容
    :param at_mobiles: 被 @ 的钉钉用户手机号列表，如 ["188xxxx8888", "177xxxx7777"]
    :param is_at_all: 是否 @ 所有人
    """
    token = '052ac1c5458f626404e315f58b5a9b081510ac94671375282b0a1a31178d785c'
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token  # 钉钉机器人 Webhook 地址，需要填入自己的 token。

    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'text',
        'text': {'content': '招标：\n' + msg},
        'at': {}
    }
    at_mobiles = '13971008822'
    is_at_all = False

    # if at_mobiles:
    #     data['at']['atMobiles'] = at_mobiles
    # if is_at_all:
    #     data['at']['isAtAll'] = True

    try:
        response = requests.post(url=webhook_url, data=json.dumps(data), headers=headers)
        response_json = json.loads(response.content.decode('utf-8'))
        if response.status_code == requests.codes.ok and response_json['errcode'] == 0:
            print("Message sent successfully.")
        else:
            print("Failed to send message. Response:", response.text)
    except Exception as e:
        print("Exception occurred while sending message:", e)


def execute_at_daytime(func, args=()):
    """
    限制只在白天执行指定函数
    :param func: 要执行的函数
    :param args: 函数参数（位置参数）
    :param kwargs: 函数参数（关键字参数）
    """
    now = datetime.datetime.now()
    hour = now.hour

    if hour >= 0 and hour < 7:
        print("当前时间为晚上，不执行钉钉发送信息函数")
    else:
        func(*args)


def log(text, filename='log.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, filename)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write(f"[{now}] {text}\n")


def get_cookie(cookie_file='cookie.txt'):
    """
    从 cookie.txt 文件中读取 cookie 值。
    Returns
    -------
        cookie : str, 即cookie的值

    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_file = os.path.join(script_dir, cookie_file)
    with open(cookie_file, 'r') as f:
        cookie = f.read()
    print(f"cookie: {cookie}, cookie_file: {cookie_file}")
    return cookie


def create_connection(db_file="mydatabase.db"):
    """
    函数功能：创建和数据库的连接对象。
    参数说明：
    db_file：数据库文件路径，默认为"mydatabase.db"
    返回值：数据库连接对象
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(script_dir, db_file)
    print(f"db_file:{db_file}")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("数据库连接已创建。")
        return conn
    except Exception as e:
        print(e)
    return conn


def close_connection(conn):
    """
    函数功能：关闭数据库连接对象。
    参数说明：
    conn：数据库连接对象
    返回值：无返回值
    """
    if conn:
        conn.close()
        print("数据库连接已关闭。")


def generate_url_list(base_url, province_id, page_num):
    url_list = []
    for i in range(2, page_num + 1):
        url = f"{base_url}/fore_p_{i}_area_{province_id}.html"
        url_list.append(url)
    # 插入第一页的链接，它与其他页面的链接不同
    url_list.insert(0, f'https://zb.zhaobiao.cn/bidding_area_{province_id}.html')
    return url_list


if __name__ == '__main__':
    print(f"Travelling href: {get_cookie()}")
    # print(get_cookie())
