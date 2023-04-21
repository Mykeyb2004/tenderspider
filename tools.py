import sqlite3


def get_cookie():
    """
    从 cookie.txt 文件中读取 cookie 值。
    Returns
    -------
        cookie : str, 即cookie的值

    """
    with open('cookie.txt', 'r') as f:
        cookie = f.read()
    return cookie


def create_connection(db_file="mydatabase.db"):
    """
    函数功能：创建和数据库的连接对象。
    参数说明：
    db_file：数据库文件路径，默认为"mydatabase.db"
    返回值：数据库连接对象
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("数据库连接已创建。")
        return conn
    except Exception as e:
        print(e)
    return conn


def close_connection(conn):
    """
    函数功能：关闭数据库连接对象。
    参数说明：
    conn：数据库连接对象
    返回值：无返回值
    """
    if conn:
        conn.close()
        print("数据库连接已关闭。")


def print_2d_array(arr, delimiter=' ', header=True, alignment='left'):
    """
    将二维数组以表格形式输出，支持带有表头和列对齐
    :param arr: 二维数组
    :param delimiter: 元素分隔符，默认为空格符
    :param header: 是否输出表头，默认为 True
    :param alignment: 对齐方式，可选值包括 'left'、'center' 和 'right'，默认为 'left'
    """
    # 判断对齐方式是否有效
    valid_alignments = ['left', 'center', 'right']
    if alignment not in valid_alignments:
        raise ValueError(f"Invalid alignment '{alignment}'. Valid values are {valid_alignments}")

    # 获取每列的最大宽度
    if header:
        rows = arr[1:]
    else:
        rows = arr
    max_widths = [max([len(str(row[i])) for row in rows]) for i in range(len(arr[0]))]

    # 输出表格
    if header:
        # 输出表头
        header_row = arr[0]
        for i, col in enumerate(header_row):
            col_str = str(col).ljust(max_widths[i]) if alignment == 'left' else (
                str(col).center(max_widths[i]) if alignment == 'center' else str(col).rjust(max_widths[i]))
            print(col_str, end=delimiter)
        print()

    # 输出表格数据
    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            col_str = str(col).ljust(max_widths[j]) if alignment == 'left' else (
                str(col).center(max_widths[j]) if alignment == 'center' else str(col).rjust(max_widths[j]))
            print(col_str, end=delimiter)
        print()


def generate_url_list(base_url, province_id, page_num):
    url_list = []
    for i in range(2, page_num + 1):
        url = f"{base_url}/fore_p_{i}_area_{province_id}.html"
        url_list.append(url)
    # 插入第一页的链接，它与其他页面的链接不同
    url_list.insert(0, f'https://zb.zhaobiao.cn/bidding_area_{province_id}.html')
    return url_list


if __name__ == '__main__':
    print("Running tools.py")
