from tender_spider import *
import schedule
import time
import datetime


# 定义整点调用函数
def run_scheduler(task_func, task_param):
    # 在整点调用任务函数
    schedule.every().hour.at(":00").do(task_func, task_param)

    # 程序循环运行，直到手动终止
    while True:
        try:
            schedule.run_pending()
        except ValueError as e:
            if "at least one job" in str(e):
                print(f"未找到可执行的任务，每小时整点将重新开始")
            else:
                raise e
        time.sleep(1)


def start_crawl(task_param=None):
    print("当前任务启动时间：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Starting to crawl list page...")
    my_spider = TenderSpider()
    my_spider.start(LIST_PAGE)
    # print("Starting to crawl detail page...")
    # my_spider.start(DETAIL_PAGE)
    print("Done.")


if __name__ == "__main__":
    print("Watching ...")
    run_scheduler(start_crawl, None)
