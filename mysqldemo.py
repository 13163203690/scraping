import pymysql

db = pymysql.connect(
    host="127.0.0.1",
    user='root',
    password='root',
    database='student',
    port=3306
)
cursor = db.cursor()

sql = """
update student set stuname='花花' where stuno=18
"""

cursor.execute(sql)
db.commit()
db.close()
