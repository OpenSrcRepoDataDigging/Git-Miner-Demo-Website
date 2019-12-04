from pprint import pprint

import pymysql
import sqlite3
import getpass


class repoDB_Options():

	def __init__(self, database='/home/' + getpass.getuser() + '/.gitminer/repo.db') -> None:
		super().__init__()
		self.database = database

	def connect(self):
		self.conn = sqlite3.connect(self.database)

	def close(self):
		self.conn.close()

	# 执行一条SQL语句
	def execute(self, sql_command):
		# 链接数据库
		self.connect()
		# 制定数据形式
		self.conn.row_factory = sqlite3.Row
		print("Opened %s successfully" % self.database)
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

	# 获得带有列名的数据库信息
	def get_col_and_datas(self, table_name):
		self.connect()
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM {}".format(table_name))
		datas = cur.fetchall()
		col_name_list = [tuple[0] for tuple in cur.description]
		res = []
		res.append(col_name_list)
		for data in datas:
			res.append(list(data))
		return res

	# 获得数据库的简略信息
	def get_repo_status(self):
		repo_status = self.execute("SELECT * FROM REPOSTATUS")
		return repo_status

	def get_tables(self):
		tables = self.execute("select name from sqlite_master where type='table' order by name;")
		return tables

	# 看表是否存在
	def is_table_exist(self, table_name):
		tables = self.get_tables()
		if tables != None:
			for table in tables:
				if table[0] == table_name:
					return True
		return False

	# 获得序号
	def get_repo_index(self, repo_name):
		repo_status = self.get_repo_status()
		index = -1
		for repo in repo_status:
			if (repo['REPONAME'] == repo_name):
				index = repo['REPOLOCALPATH'].split('/')[-2]
				return index
		return index

	# 获得每个日期开发者的commit次数
	def get_CommitTimesListByDay(self, table_name):
		# 数据原型
		datas = [
			['contributor', '没有', '这个', '对应的', '数据'],
			['2015', 43.3, 85.8, 93.7, 83.1],
			['2016', 83.1, 73.4, 55.1, 86.4],
			['2017', 86.4, 65.2, 82.5, 72.4],
			['2018', 72.4, 53.9, 39.1, 7.4],
			['2019', 7.4, 45.9, 66.1, 42.4],
			['2020', 42.4, 22.9, 19.1, 43.3]
		]
		if self.is_table_exist(table_name):
			datas = self.get_col_and_datas(table_name)
		else:
			print("表", table_name, "不存在")
		return datas

	def get_ContributorNetworkMatrix(self, table_name):
		# 数据原型
		datas = {}
		hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
				 '7a', '8a', '9a', '10a', '11a',
				 '12p', '1p', '2p', '3p', '4p', '5p',
				 '6p', '7p', '8p', '9p', '10p', '11p']
		days = ['数据', '根本', '不存在',
				'温馨', '提示', '有', 'BUG']
		data = [[0, 0, 5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0], [0, 8, 0],
				[0, 9, 0], [0, 10, 0], [0, 11, 2], [0, 12, 4], [0, 13, 1], [0, 14, 1], [0, 15, 3], [0, 16, 4],
				[0, 17, 6], [0, 18, 4], [0, 19, 4], [0, 20, 3], [0, 21, 3], [0, 22, 2], [0, 23, 5], [1, 0, 7],
				[1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0], [1, 5, 0], [1, 6, 0], [1, 7, 0], [1, 8, 0], [1, 9, 0],
				[1, 10, 5], [1, 11, 2], [1, 12, 2], [1, 13, 6], [1, 14, 9], [1, 15, 11], [1, 16, 6], [1, 17, 7],
				[1, 18, 8], [1, 19, 12], [1, 20, 5], [1, 21, 5], [1, 22, 7], [1, 23, 2], [2, 0, 1], [2, 1, 1],
				[2, 2, 0], [2, 3, 0], [2, 4, 0], [2, 5, 0], [2, 6, 0], [2, 7, 0], [2, 8, 0], [2, 9, 0], [2, 10, 3],
				[2, 11, 2], [2, 12, 1], [2, 13, 9], [2, 14, 8], [2, 15, 10], [2, 16, 6], [2, 17, 5], [2, 18, 5],
				[2, 19, 5], [2, 20, 7], [2, 21, 4], [2, 22, 2], [2, 23, 4], [3, 0, 7], [3, 1, 3], [3, 2, 0], [3, 3, 0],
				[3, 4, 0], [3, 5, 0], [3, 6, 0], [3, 7, 0], [3, 8, 1], [3, 9, 0], [3, 10, 5], [3, 11, 4], [3, 12, 7],
				[3, 13, 14], [3, 14, 13], [3, 15, 12], [3, 16, 9], [3, 17, 5], [3, 18, 5], [3, 19, 10], [3, 20, 6],
				[3, 21, 4], [3, 22, 4], [3, 23, 1], [4, 0, 1], [4, 1, 3], [4, 2, 0], [4, 3, 0], [4, 4, 0], [4, 5, 1],
				[4, 6, 0], [4, 7, 0], [4, 8, 0], [4, 9, 2], [4, 10, 4], [4, 11, 4], [4, 12, 2], [4, 13, 4], [4, 14, 4],
				[4, 15, 14], [4, 16, 12], [4, 17, 1], [4, 18, 8], [4, 19, 5], [4, 20, 3], [4, 21, 7], [4, 22, 3],
				[4, 23, 0], [5, 0, 2], [5, 1, 1], [5, 2, 0], [5, 3, 3], [5, 4, 0], [5, 5, 0], [5, 6, 0], [5, 7, 0],
				[5, 8, 2], [5, 9, 0], [5, 10, 4], [5, 11, 1], [5, 12, 5], [5, 13, 10], [5, 14, 5], [5, 15, 7],
				[5, 16, 11], [5, 17, 6], [5, 18, 0], [5, 19, 5], [5, 20, 3], [5, 21, 4], [5, 22, 2], [5, 23, 0],
				[6, 0, 1], [6, 1, 0], [6, 2, 0], [6, 3, 0], [6, 4, 0], [6, 5, 0], [6, 6, 0], [6, 7, 0], [6, 8, 0],
				[6, 9, 0], [6, 10, 1], [6, 11, 0], [6, 12, 2], [6, 13, 1], [6, 14, 3], [6, 15, 4], [6, 16, 0],
				[6, 17, 0], [6, 18, 0], [6, 19, 0], [6, 20, 1], [6, 21, 2], [6, 22, 2], [6, 23, 6]]

		datas['x'] = hours
		datas['y'] = days
		datas['data'] = data

		if self.is_table_exist(table_name):
			names_raw = self.execute("select name from {}".format(table_name))
			names = []
			for i in names_raw:
				for j in i:
					names.append(j)
			infos = self.get_col_and_datas(table_name)
			data = []
			for i in range(1, infos.__len__()):
				for j in range(1, infos[0].__len__()):
					data.append([i-1, j-1, infos[i][j]])

			datas['x'] = names
			datas['y'] = names
			datas['data'] = data
		else:
			print("表", table_name, "不存在")

		return datas

	# 格式化输出
	def print_format_datas(self, datas):
		for data in datas:
			for item in data:
				print(item, '\t', end="")
			print()


if __name__ == '__main__':
	repoDB = repoDB_Options()
	datas = repoDB.get_ContributorNetworkMatrix('ContributorNetworkMatrix1')
	print(datas)
