import asyncio
import datetime
import time
from typing import Any

from tools import *
from playwright.async_api import async_playwright

LIST_PAGE = 0
DETAIL_PAGE = 1


class TenderSpider:
    def __init__(self):
        self.cookie = {'name': 'Cookies_token', 'value': get_cookie(), 'url': 'https://zb.zhaobiao.cn/'}
        self.connection = create_connection()

    def __del__(self):
        close_connection(self.connection)

    def save_tender_list(self, table: list) -> tuple:
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

            # 建立数据表
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS tender (id INTEGER PRIMARY KEY, href TEXT UNIQUE, 
                title TEXT, area TEXT, post_date DATE, has_crawled INTEGER DEFAULT 0,html TEXT,
                created_at  TIMESTAMP default CURRENT_TIMESTAMP, updated_at TIMESTAMP default CURRENT_TIMESTAMP)''')

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

    async def get_tender_list(self, browser, url):
        context = await browser.new_context()
        tbody_list = []

        try:
            # 设置 cookies
            # await context.add_cookies([self.cookie])
            page = await context.new_page()
            print("Navigating to", url)
            await page.goto(url)
            # 获取tbody id=data tbody下全部tr标签文本内容并输出到控制台
            print("Accessing table data...")
            tbody = await page.query_selector('#datatbody')
            trs = await tbody.query_selector_all('tr')

            for tr in trs:
                tds = await tr.query_selector_all('td')
                tds_text = []
                for i, td in enumerate(tds):
                    if i == 0:
                        a_link = await td.query_selector('a')
                        href = await a_link.get_attribute('href')
                        title = await a_link.get_attribute('title')
                        tds_text.append(href)
                        tds_text.append(title)
                    else:
                        tds_text.append(await td.text_content())
                tbody_list.append(tds_text)
        except Exception as e:
            print(f"Error crawling list page - function(get_tender_list): {e}")
            # 打印并保存数据到数据库
            # # print_2d_array(tbody_list)
        finally:
            await context.close()
            return tbody_list

    def get_detail_href_to_crawl(self, query_count_limit: int = 50) -> list[Any]:
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

    async def run(self, page=LIST_PAGE):
        # 获取招标信息列表页
        if page == LIST_PAGE:
            browser = None
            try:
                async with async_playwright() as p:
                    print(f"{datetime.datetime.now()} - > Crawling list page. Launching browser...")
                    browser = await p.chromium.launch()

                    base_url = "https://zb.zhaobiao.cn"
                    page_num = 100
                    # 省份代码列表，按此遍历各省份招标信息
                    provinces = ['330000', '420000']
                    # 遍历各省份
                    for province in provinces:
                        print("Travelling province: " + province)
                        url_list = generate_url_list(base_url, province, page_num)
                        for url in url_list:
                            tender_list = await self.get_tender_list(browser, url)
                            dup_count, total_count, is_success = self.save_tender_list(tender_list)
                            print(
                                f"Duplicate data: {dup_count}/{total_count}. "
                                f"New data {total_count - dup_count} saved. ")
                            if dup_count == total_count:
                                print("Too many duplicate datas, skip to the rest province.")
                                break
                    await browser.close()
            except Exception as e:
                print(f"Error crawling list page: {e}")
                await browser.close()
        # 获取招标信息详情页
        if page == DETAIL_PAGE:
            browser = None
            try:
                async with async_playwright() as p:
                    print(f"{datetime.datetime.now()} - > Crawling detail page. Launching browser...")
                    browser = await p.chromium.launch()
                    # 获取待爬取的招标信息链接
                    href_list = self.get_detail_href_to_crawl(query_count_limit=1500)

                    # while len(href_list) > 0:
                    # 遍历招标信息链接
                    for href in href_list:
                        print(f"[{datetime.datetime.now()}] Travelling href: {href}")
                        total_count, not_null_count = self.count_crawled_html_records()
                        print(
                            f'Total/Crawled: {total_count}/{not_null_count}，'
                            f'Completed: {not_null_count / total_count * 100:.2f}%')

                        html = await self.get_tender_detail(browser, href[1])
                        print(html[:50] + '...')
                        # 保存招标信息详情页
                        if html is not None:
                            if self.save_detail_data_to_db(href[0], html):
                                print(f"Detail page saved")
                            else:
                                print(f"Detail page not saved")
                            # href_list = self.get_detail_href_to_crawl(query_count_limit=50)
            except Exception as e:
                print(f"Error crawling detail page (function run): {e}")
                return False
                await browser.close()
                print("Browser was shutdown.")
            print("All detail page crawled.")

    def start(self, page):
        asyncio.run(self.run(page=page))


if __name__ == '__main__':
    spider = TenderSpider()
    print("Starting to crawl list page...")
    spider.start(LIST_PAGE)
    # print("Starting to crawl detail page...")
    # spider.start(DETAIL_PAGE)
    print("Done.")
