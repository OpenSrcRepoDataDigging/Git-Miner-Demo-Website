import pymysql
import sqlite3

class repoDB_Options():

	def __init__(self,database = '/home/young/.gitminer/repo.db') -> None:
		super().__init__()
		self.database = database

	def connect(self):
		self.conn = sqlite3.connect(self.database)

	def close(self):
		self.conn.close()

	def execute(self, sql_command):
		# 链接数据库
		self.connect()
		# 制定数据形式
		self.conn.row_factory = sqlite3.Row
		print("Opened %s successfully",self.database)
		c = self.conn.cursor()
		cursor = c.execute(sql_command)
		datas = cursor.fetchall()
		for data in datas:
			res = []
			for item in data:
				res.append(item)
			print(res)
		# 关闭数据库链接
		self.close()
		# 返回数据
		return datas

	def get_repo_status(self):
		repo_status = self.execute("SELECT * FROM REPOSTATUS")
		return repo_status


if __name__ == '__main__':
	repoDB = repoDB_Options()
	datas = repoDB.get_repo_status()
