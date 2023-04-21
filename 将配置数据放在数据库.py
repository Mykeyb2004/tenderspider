import sqlite3


def create_database():
    conn = sqlite3.connect('config.db')
    c = conn.cursor()

    # 创建参数表
    c.execute('''CREATE TABLE IF NOT EXISTS config (name TEXT PRIMARY KEY, value TEXT)''')

    # 插入初始数据
    c.execute(
        "INSERT OR IGNORE INTO config (name, value) VALUES ('url', 'https://zb.zhaobiao.cn/bidding_area_330000.html')")
    c.execute("INSERT OR IGNORE INTO config (name, value) VALUES ('cookie_name', 'Cookies_token')")
    c.execute("INSERT OR IGNORE INTO config (name, value) VALUES ('cookie_url', 'https://zb.zhaobiao.cn/')")
    c.execute("INSERT OR IGNORE INTO config (name, value) VALUES ('db_name', 'tender.db')")

    conn.commit()
    conn.close()


def get_config(name):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute("SELECT value FROM config WHERE name=?", (name,))
    value = c.fetchone()
    conn.close()
    return value[0] if value else None


def set_config(name, value):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute("UPDATE config SET value=? WHERE name=?", (value, name))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()

    url = get_config('url')
    cookie_name = get_config('cookie_name')
    cookie_url = get_config('cookie_url')
    db_name = get_config('db_name')

    print(f"url: {url}")
    print(f"cookie_name: {cookie_name}")
    print(f"cookie_url: {cookie_url}")
    print(f"db_name: {db_name}")
