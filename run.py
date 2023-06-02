import tender_spider as ts
from tender_weight import TenderWeightCalculator

if __name__ == '__main__':
    spider = ts.TenderSpider()
    spider.start(ts.LIST_PAGE)
    spider.start(ts.DETAIL_PAGE)
    print("Updating tender weights...")
    tender_calc = TenderWeightCalculator()
    tender_calc.update_tender_weight(refresh_all=False)
    print("Updating tender weights finished.")
