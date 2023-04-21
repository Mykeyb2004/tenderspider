import asyncio
from playwright.async_api import async_playwright
import re


def filter_unreadable_chars(text):
    """
    过滤文本中的不可读字符
    Args:
        text: 待处理的文本字符串
    Returns:
        经过过滤后的文本字符串
    """
    # 使用正则表达式匹配不可读字符并去除
    filtered_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\xFF]', '', text)
    # 使用正则表达式匹配连续的回车符和换行符并替换为单个回车符
    # filtered_text = re.sub(r'(\r\n){2,}', '\r\n', filtered_text)
    # 使用正则表达式匹配连续的空白字符并替换为单个换行符
    filtered_text = re.sub(r'\s+', '\n', text)
    return filtered_text


async def main():
    url = 'https://zb.zhaobiao.cn/bidding_v_123152343.html'
    path = 'page.html'
    cookie = {'name': 'Cookies_token', 'value': '3c47b459-7a7d-4173-ba30-622aae68f754', 'url': url}

    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch()
        context = await browser.new_context()
        # 设置 cookies
        await context.add_cookies([cookie])
        page = await context.new_page()
        print("Navigating to page...")
        await page.goto(url)
        # content = await page.content()
        # # 将内容写入 HTML 文件
        # with open(path, 'w', encoding='utf-8') as f:
        #     f.write(content)

        # 等待iframe加载完成
        await page.wait_for_selector("#iframe_son")
        frame = page.frame(name="iframe_son")
        # 等待内容加载完成
        await frame.wait_for_selector(".bid_details_zw")
        element = await frame.query_selector(".bid_details_zw")
        # content = await element.inner_html()  # 获取html内容
        content = await element.text_content()  # 获取文本内容
        print(filter_unreadable_chars(content))

        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
