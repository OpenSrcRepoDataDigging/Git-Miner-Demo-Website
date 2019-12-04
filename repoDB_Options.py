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

	# 获得每个日期开发者的commit次数
	def get_CommitTimesListByDay(self, repo_name):
		dates = ['2012', '2013', '2014','2015','2016']
		commits = []
		commits.append({
			'name': 'name1',
			'data': [320, 332, 301, 334, 390]
		})
		commits.append({
			'name': 'name1',
			'data': [220, 182, 191, 234, 290]
		})
		commits.append({
			'name': 'name1',
			'data': [150, 232, 201, 154, 190]
		})
		commits.append({
			'name': 'name1',
			'data': [98, 77, 101, 99, 40]
		})

		commitTimesListByDay = {}
		commitTimesListByDay['dates'] = dates
		commitTimesListByDay['commits'] = commits

		return commitTimesListByDay

if __name__ == '__main__':
	repoDB = repoDB_Options()
	datas = repoDB.get_repo_status()
