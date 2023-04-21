import datetime
import time


def execute_periodic_task(task, interval_hours):
    """执行定期任务的函数。

    Args:
        task: 要执行的任务函数。
        interval_hours: 每隔指定时间间隔（以小时为单位）执行一次任务。
    """

    def run_task():
        # 这里定义要执行的高耗时任务
        task()

    while True:
        # 获取当前时间和下一个整点小时时间
        now = datetime.datetime.now()
        next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

        # 计算下一次任务开始的时间
        if (next_hour - now).total_seconds() > 60:
            run_time = next_hour
        else:
            run_time = now + datetime.timedelta(hours=1)

        # 等待到任务开始时间
        time_diff = (run_time - datetime.datetime.now()).total_seconds()
        print(f"Waiting {time_diff / 3600:.1f} hours until {run_time}")
        time.sleep(time_diff)

        print(f"Running task at {datetime.datetime.now()}")
        run_task()
        print(f"Task finished at {datetime.datetime.now()}")

        # 每隔指定间隔时间执行一次任务
        time.sleep(interval_hours * 3600)


# 测试示例，每隔1个小时输出当前时间
def my_task():
    print(f"Current time: {datetime.datetime.now()}")


execute_periodic_task(my_task, interval_hours=1)

# 以上是完整的代码，并在关键位置添加注释。 execute_periodic_task()函数接受两个参数，分别是要执行的任务和时间间隔（以小时为单位）。
# 在函数内部，我们首先定义了一个run_task()函数，用于执行实际的任务。然后使用一个while循环不断执行任务并计算等待时间，直到程序被中断。
# 在每次执行任务后，程序会等待指定的时间间隔再次执行任务。
# 我们可以将要执行的任务和时间间隔作为参数传入execute_periodic_task()函数中进行测试。
