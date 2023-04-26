# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

tbody_list = []

url = 'https://zb.zhaobiao.cn/bidding_area_330000.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': 'searchaltab-table'})
tbody = table.find('tbody', {'id': 'datatbody'})
trs = tbody.find_all('tr', {'class': 'datatr'})

tbody_list = []
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

print(tbody_list)

# for tr in trs:
#     tds = tr.find_all('td')
#     for td in tds:
#         print(td.text)
# for tr in trs:
#     tds = tr.find_all('td')
#     tds_text = []
#     for i, td in enumerate(tds):
#         if i == 0:
#             a_link = await td.query_selector('a')
#             href = await a_link.get_attribute('href')
#             title = await a_link.get_attribute('title')
#             tds_text.append(href)
#             tds_text.append(title)
#         else:
#             tds_text.append(await td.text_content())
#     tbody_list.append(tds_text)
# print(tbody_list)
