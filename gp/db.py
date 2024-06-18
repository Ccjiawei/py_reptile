#数据库测试
import pymysql

conn = pymysql.connect(host='81.68.197.104', password='Baiwa@0601', port=3307, user='root', charset='utf8')
cur = conn.cursor()

cur.execute('show databases')
print(cur.fetchone())  # 返回前一条记录
print(cur.fetchmany(2))  # 返回前两条记录
print(cur.fetchall())  # 返回所有记录

cur.close()
conn.close()
