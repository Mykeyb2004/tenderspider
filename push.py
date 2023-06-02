from tender_push import TenderPush
import datetime

if __name__ == '__main__':
    # 推送招标信息
    print(f"[{datetime.datetime.now()}] Pushing tender info...")
    tender_push = TenderPush()
    tender_push.push(300)
