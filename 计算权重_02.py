import re

def count_total_w(target_text, conn):

    cursor = conn.cursor()
    # 将目标内容拆分为关键词列表
    # keywords = set(jieba.cut(target_text))
    # print(keywords)

    # 遍历词汇表中的每个单词，并将匹配的 w 值进行累加
    total_weight = 0
    for row in cursor.execute("SELECT word, w FROM dictionary"):
        if re.search(row[0], target_text):
            print("匹配到关键词：", row[0], "，w 值为：", row[1])
            total_weight += row[1]

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 返回总 w 值汇总分数
    return total_weight


# 测试封装好的函数
target = """
        <b class="new_tit">硅谷幼儿园招标文件预公示</b><br><table width="80%"> 
     <tbody>
      <tr> 
       <td>&nbsp;&nbsp;&nbsp;&nbsp;根据《浙江省人民政府关于进一步加强工程建设项目招标投标领域依法治理的意见》等有关规定，现对硅谷幼儿园项目进行招标文件预公示，欢迎合格的投标人前来投标，对招标文件预公示的反馈意见请于 本公告发出后3日内向招标人（招标代理机构）提出。 </td> 
      </tr> 
      <tr> 
       <td>项目名称：硅谷幼儿园</td> 
      </tr> 
      <tr> 
       <td>项目编号：A3301110200506384001211</td> 
      </tr> 
      <tr> 
       <td>招标人单位：杭州富阳开发区基础设施建设有限公司</td> 
      </tr> 
      <tr> 
       <td>代理机构单位：建经投资咨询有限公司</td> 
      </tr> 
      <tr> 
       <td>代理机构联系方式：15857076509</td> 
      </tr> 
      <tr> 
       <td>一、招标项目内容：打桩工程，土建工程，安装工程，装饰装修，室外附属，弱电工程，消防工程，市政，绿化工程，其它工程，</td> 
      </tr> 
      <tr> 
       <td>二、招标控制价：3272.3382(万元)</td> 
      </tr> 
      <tr> 
       <td>附件下载：<a href="https://zbfile.zhaobiao.cn/resources/styles/v2/jsp/bidFile.jsp?id=2045372154" target="_parent">点击下载</a></td> 
      </tr> 
      <tr> 
       <td></td> 
      </tr> 
     </tbody>
    </table>

"""
target = html2text.html2text(target)
print(target)
total_w = count_total_w(target)
print("总 w 值汇总分数为：", total_w)
