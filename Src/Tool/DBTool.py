"数据库工具"
import MySQLdb


class MySQL():
    "mysql类"

    def __init__(self, host, port, u, p, db):
        "初始化连接"
        self.conn = MySQLdb.connect(host=host, port=port, user=u, passwd=p, db=db, charset="utf8")
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        "执行语句"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

    def query(self, sql):
        "查询"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            print("查询失败")
