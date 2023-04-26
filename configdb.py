import sqlite3


class ConfigDB:
    def __init__(self, dbname='mydatabase.db'):
        """
        初始化 ConfigDB 类，连接指定数据库并创建数据表 config（如果不存在）
        :param dbname: 数据库文件名（默认为 mydatabase.db）
        """
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT,
                value TEXT,
                PRIMARY KEY (key, value)
            )
        ''')

    def set(self, key, value):
        """
        设置指定 key 对应的 value，若 value 为数组，则将其元素拆分存储到多个数据行中
        :param key: 配置项名称
        :param value: 配置项的值
        """
        if isinstance(value, list):
            # 如果 value 是数组，则将其元素拆分存储到多个数据行中
            for v in value:
                self.cursor.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', (key, v))
        else:
            # 如果 value 不是数组，则直接存储到数据表中
            self.cursor.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', (key, value))

        self.conn.commit()

    def get(self, key):
        """
        获取指定 key 对应的 value，返回值可能是单值或数组
        :param key: 配置项名称
        :return: 配置项的值（单值或数组）或 None（如果不存在）
        """
        self.cursor.execute('SELECT value FROM config WHERE key = ?', (key,))
        rows = self.cursor.fetchall()
        if rows:
            values = [row[0] for row in rows]
            if len(values) == 1:
                return values[0]
            else:
                return values
        else:
            return None

    def delete(self, key):
        """
        删除指定 key 对应的配置项（可能有多个 value）
        :param key: 配置项名称
        """
        self.cursor.execute('DELETE FROM config WHERE key = ?', (key,))
        self.conn.commit()

    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    # 创建 ConfigDB 实例并进行简单操作
    db = ConfigDB()

    # 写入配置项到数据库中
    db.set('key1', 'value1')
    db.set('key2', [1, 2])
    db.set('key3', ['value4'])

    # 获取某个配置项的值
    print(db.get('key1'))  # 输出：value1
    print(db.get('key2'))  # 输出：['value2', 'value3']
    print(db.get('key3'))  # 输出：['value4']

    # 删除某个配置项
    db.delete('key1')

    # 关闭数据库连接
    db.close()
