from pprint import pprint

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
		print("Opened %s successfully"%self.database)
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

	def get_colname(self, repo_name):
		self.connect()
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM {}".format(repo_name))
		datas = cur.fetchall()
		col_name_list = [tuple[0] for tuple in cur.description]
		res = []
		res.append(col_name_list)
		for data in datas:
			res.append(list(data))
		return res

	def get_repo_status(self):
		repo_status = self.execute("SELECT * FROM REPOSTATUS")
		return repo_status

	# 获得每个日期开发者的commit次数
	def get_CommitTimesListByDay(self, repo_name):
		commitTimesListByDay = [
			['contributor', '欧阳', '刘笑今', '白家杨','刘岚峰'],
			['2015', 43.3, 85.8, 93.7, 83.1],
			['2016', 83.1, 73.4, 55.1, 86.4],
			['2017', 86.4, 65.2, 82.5, 72.4],
			['2018', 72.4, 53.9, 39.1, 7.4],
			['2019', 7.4, 45.9, 66.1, 42.4],
			['2020', 42.4, 22.9, 19.1, 43.3]
		]

		datas = self.get_colname(repo_name)

		return datas



if __name__ == '__main__':
	repoDB = repoDB_Options()
	# datas = repoDB.get_repo_status()
	datas = repoDB.get_CommitTimesListByDay('CommitTimesListByDay1')
	print(datas)