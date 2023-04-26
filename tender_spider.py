# -*- coding: utf-8 -*-

import asyncio
import random
# import datetime
import time
import sys
import requests

from tools import *
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

LIST_PAGE = 0
DETAIL_PAGE = 1
QUERY_COUNT_LIMIT = 100


class TenderSpider:
    def __init__(self):
        self.cookie = {'name': 'Cookies_token', 'value': get_cookie(), 'url': 'https://zb.zhaobiao.cn/'}
        self.connection = create_connection()

    def __del__(self):
        self.summary()
        close_connection(self.connection)

    def save_tender_list(self, table):
        """
        将数据存储到 SQLite 数据库中，并返回未重复数据的数量、总数据量和操作是否成功。
        :param table: 包含招标信息的列表，每个元素都是一个记录
        :return: 元组，包含未重复数据的数量、总数据量和操作是否成功
        """
        # 用于存储未重复数据的列表
        unique_data_list = []

        try:
            # 连接到指定 SQLite 数据库
            cursor = self.connection.cursor()

            # 对数据进行去重，并将未重复的数据添加到unique_data_list中
            for row in table:
                if not cursor.execute("SELECT * FROM tender WHERE href=?", (row[0],)).fetchone():
                    unique_data_list.append(row)

            # 批量插入数据到数据库中
            cursor.executemany(
                'INSERT INTO tender (href, title, area, post_date) VALUES (?, ?, ?, ?)',
                unique_data_list)
            # 提交更改并关闭连接
            self.connection.commit()
            # 重复数据数量
            duplicate_count = len(table) - len(unique_data_list)
            return duplicate_count, len(table), True
        except Exception as e:
            # 如果出现错误，回滚事务并关闭连接
            print(f"保存数据时发生错误：{str(e)}")
            self.connection.rollback()
            return 0, len(table), False

    def save_detail_data_to_db(self, record_id: int, html: str) -> bool:
        try:
            # 连接到指定 SQLite 数据库
            cursor = self.connection.cursor()
            # 更新html、has_crawled、updated_at字段
            sql = "UPDATE tender SET has_crawled=?, updated_at=?, html=? WHERE id=?"
            cursor.execute(sql, (1, datetime.datetime.now(), html, record_id))
            # 提交更改并关闭连接
            self.connection.commit()
            cursor.close()
            print()
            return True
        except Exception as e:
            # 如果出现错误，回滚事务并关闭连接
            print(f"保存数据时发生错误：{str(e)}")
            self.connection.rollback()
            cursor.close()
            return False

    async def get_tender_detail(self, browser, url):

        context = await browser.new_context()
        try:
            # 设置 cookies
            await context.add_cookies([self.cookie])
            page = await context.new_page()
            print("Navigating to", url)
            await page.goto(url)

            # 等待iframe加载完成
            await page.wait_for_selector("#iframe_son")
            frame = page.frame(name="iframe_son")
            # 等待内容加载完成
            await frame.wait_for_selector(".bid_details_zw")
            element = await frame.query_selector(".bid_details_zw")
            content = await element.inner_html()  # 获取html内容
            # content = await element.text_content()  # 获取文本内容
            await context.close()
            return content
        except Exception as e:
            print(f"Error crawling detail page - function(get_tender_detail): {e}")
            return None
            # await context.close()

    async def get_tender_list(self, url):
        tbody_list = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            print(f"Navigating to {url}. Getting the tender list.")

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'searchaltab-table'})
            tbody = table.find('tbody', {'id': 'datatbody'})
            trs = tbody.find_all('tr', {'class': 'datatr'})

            for tr in trs:
                row = []
                tds = tr.find_all('td')
                for i, td in enumerate(tds):
                    if i == 0:  # 第一个td标签
                        a_tag = td.find('a')
                        if a_tag is not None:
                            row.append(a_tag['href'])  # 获取href属性值
                            row.append(a_tag['title'])  # 获取title属性值
                        else:
                            row.append('')
                            row.append('')
                    else:
                        row.append(td.text.strip())  # 去除空白字符
                tbody_list.append(row)
        except Exception as e:
            print(f"Error crawling list page - function(get_tender_list): {e}")
        finally:
            return tbody_list

    def get_detail_href_to_crawl(self, query_count_limit=50):
        href_list = []
        # 获取今天的日期并格式化
        today = datetime.date.today()
        today_str = today.strftime('%Y-%m-%d')

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"SELECT id, href FROM tender WHERE has_crawled = 0 AND post_date = '{today_str}' ORDER BY post_date DESC LIMIT {query_count_limit}")
            rows = cursor.fetchall()
            for row in rows:
                href_list.append([row[0], row[1]])
        except Exception as e:
            print(f"查询数据时发生错误：{str(e)}")
        return href_list

    def count_crawled_html_records(self):
        # 获取游标对象
        cursor = self.connection.cursor()

        # 执行 SELECT 查询，获取 html 字段不为空的记录总条数
        total_query = "SELECT COUNT(id) FROM tender"
        cursor.execute(total_query)
        total_count = cursor.fetchone()[0]

        not_null_query = "SELECT COUNT(id) FROM tender WHERE html IS NOT NULL"
        cursor.execute(not_null_query)
        not_null_count = cursor.fetchone()[0]

        # 关闭游标和连接
        cursor.close()

        return total_count, not_null_count

    def summary(self):
        # 获取游标对象
        cursor = self.connection.cursor()
        today_sql = "SELECT COUNT(*) FROM tender WHERE DATE(post_date) = DATE('now', 'localtime')"
        yesterday_sql = "SELECT COUNT(*) FROM tender WHERE DATE(post_date) = DATE('now', '-1 day', 'localtime')"
        before_yesterday_sql = "SELECT COUNT(*) FROM tender WHERE DATE(post_date) = DATE('now', '-2 day', 'localtime')"
        crawled_today_sql = "SELECT COUNT(*) FROM tender WHERE DATE(post_date) = DATE('now', 'localtime') AND html IS NOT NULL"
        # 执行 SQL 查询语句并获取总数
        today_count = cursor.execute(today_sql).fetchone()[0]
        yesterday_count = cursor.execute(yesterday_sql).fetchone()[0]
        before_yesterday_count = cursor.execute(before_yesterday_sql).fetchone()[0]
        crawled_today_count = cursor.execute(crawled_today_sql).fetchone()[0]
        return today_count, yesterday_count, before_yesterday_count, crawled_today_count

    def show_summary_info(self):
        today_count, yesterday_count, before_yesterday_count, crawled_today_count = self.summary()
        sum_text = f"今天新增：{today_count} 条；昨天新增：{yesterday_count} 条；前天新增：{before_yesterday_count} 条。\n" \
                   f"今天已爬取：{crawled_today_count} 条。"
        print(sum_text)
        log(sum_text)

    async def run(self, page=LIST_PAGE):
        # 获取招标信息列表页
        if page == LIST_PAGE:
            print(f"{datetime.datetime.now()} - > Crawling list page. Launching browser...")
            base_url = "https://zb.zhaobiao.cn"
            page_num = 100
            # 省份代码列表，按此遍历各省份招标信息
            provinces = ['330000', '420000']
            # 遍历省份列表
            for province in provinces:
                print("Travelling province: " + province)
                log("Travelling province: " + province)
                url_list = generate_url_list(base_url, province, page_num)
                for url in url_list:
                    tender_list = await self.get_tender_list(url)
                    dup_count, total_count, is_success = self.save_tender_list(tender_list)
                    print(
                        f"Duplicate data: {dup_count}/{total_count}. "
                        f"New data {total_count - dup_count} saved. ")
                    if dup_count == total_count:
                        print("Too many duplicate data, skip.")
                        break
            self.show_summary_info()

        # 获取招标信息详情页
        if page == DETAIL_PAGE:
            browser = None
            try:
                async with async_playwright() as p:
                    print(f"{datetime.datetime.now()} - > Crawling detail page. Launching browser...")
                    print(f"Cookie: {self.cookie}")
                    browser = await p.chromium.launch()
                    # 获取待爬取的招标信息链接
                    href_list = self.get_detail_href_to_crawl(query_count_limit=QUERY_COUNT_LIMIT)

                    # while len(href_list) > 0:
                    # 遍历招标信息链接
                    for href in href_list:
                        travel_href_text = f"[{datetime.datetime.now()}] Travelling href: {href}"
                        log(travel_href_text)
                        print(travel_href_text)
                        total_count, not_null_count = self.count_crawled_html_records()
                        print(
                            f'Total/Crawled: {total_count}/{not_null_count}，'
                            f'Completed: {not_null_count / total_count * 100:.2f}%')

                        # delay_time = random.randint(1, 5)
                        # print(f"Waiting for {delay_time} seconds...")
                        # time.sleep(delay_time)
                        html = await self.get_tender_detail(browser, href[1])
                        # 保存招标信息详情页
                        if html is not None:
                            if self.save_detail_data_to_db(href[0], html):
                                print(f"Detail page saved")
                        else:
                            log("Error crawling detail page.")
                            await browser.close()
                            print(f"Empty html. {href[1]}")
                            execute_at_daytime(send_dingtalk, (f"爬虫被网站禁止，{href[1]}",))
                            break
                    # href_list = self.get_detail_href_to_crawl(query_count_limit=50)
            except Exception as e:
                print(f"Error crawling detail page (function run): {e}")
                await browser.close()
                print("Browser was shutdown.")
            self.show_summary_info()

    def start(self, page):
        asyncio.run(self.run(page=page))


if __name__ == '__main__':
    # 获取命令行参数
    arg = sys.argv[1]
    if arg == 'list':
        print("Starting to crawl list page...\n")
        spider = TenderSpider()
        spider.start(LIST_PAGE)
    elif arg == 'detail':
        print("Starting to crawl detail page...\n")
        spider = TenderSpider()
        spider.start(DETAIL_PAGE)
    elif arg is None:
        print("Need a parameter in command line.\n")
    else:
        print("Invalid parameter.\n")
