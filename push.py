from tender_weight import TenderWeightCalculator
from tender_push import TenderPush

if __name__ == '__main__':
    # 更新权重
    print("Updating tender weights...")
    tender_calc = TenderWeightCalculator()
    tender_calc.update_tender_weight(refresh_all=False)
    # 推送招标信息
    tender_push = TenderPush()
    tender_push.push(100)
