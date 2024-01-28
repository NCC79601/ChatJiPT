import sqlite3
import json

# 连接到 SQLite 数据库（如果数据库不存在，将会创建一个数据库）
cursor = None
conn = None

def init():
    global conn
    global cursor
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            data TEXT
        )
    ''')


def query(username):
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))

    # 如果用户不存在
    if cursor.fetchone() is None:
        # 新建一个用户
        cursor.execute('''
            INSERT INTO users (username, data) VALUES (?, ?)
        ''', (username, json.dumps({
            'history': []
        })))

        # 提交事务
        conn.commit()

        return {
            'history': []
        }

    # 如果用户存在，返回用户的数据
    cursor.execute('''
        SELECT data FROM users WHERE username = ?
    ''', (username,))
    data = cursor.fetchone()
    if data is not None:
        return json.loads(data[0])


def insert(username, data):
    cursor.execute('''
        INSERT INTO users (username, data) VALUES (?, ?)
    ''', (username, json.dumps(data)))
    conn.commit()


def update(username, data):
    cursor.execute('''
        UPDATE users SET data = ? WHERE username = ?
    ''', (json.dumps(data), username))
    conn.commit()


def close():
    conn.close()