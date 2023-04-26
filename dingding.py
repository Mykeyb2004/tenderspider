import requests
import json


def send_msg_to_dingtalk_webhook(webhook_url, msg, at_mobiles=None, is_at_all=False):
    """
    发送钉钉消息到指定群组或个人
    :param webhook_url: 钉钉机器人的 Webhook 地址
    :param msg: 发送的消息内容
    :param at_mobiles: 被 @ 的钉钉用户手机号列表，如 ["188xxxx8888", "177xxxx7777"]
    :param is_at_all: 是否 @ 所有人
    """
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'text',
        'text': {'content': msg},
        'at': {}
    }
    if at_mobiles:
        data['at']['atMobiles'] = at_mobiles
    if is_at_all:
        data['at']['isAtAll'] = True

    try:
        response = requests.post(url=webhook_url, data=json.dumps(data), headers=headers)
        response_json = json.loads(response.content.decode('utf-8'))
        if response.status_code == requests.codes.ok and response_json['errcode'] == 0:
            print("Message sent successfully.")
        else:
            print("Failed to send message. Response:", response.text)
    except Exception as e:
        print("Exception occurred while sending message:", e)


if __name__ == '__main__':
    token = '052ac1c5458f626404e315f58b5a9b081510ac94671375282b0a1a31178d785c'
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token  # 钉钉机器人 Webhook 地址，需要填入自己的 token。
    # https://oapi.dingtalk.com/robot/send?access_token=052ac1c5458f626404e315f58b5a9b081510ac94671375282b0a1a31178d785c
    msg = '招标：Hello, World!'

    # 发送消息给指定用户（手机号为 188xxxx8888）
    at_mobiles = ['13971008822']
    is_at_all = False
    send_msg_to_dingtalk_webhook(webhook_url, msg, at_mobiles=at_mobiles, is_at_all=is_at_all)
