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

	# 执行一条SQL语句
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
			if(repo['REPONAME'] == repo_name):
				index = repo['REPOLOCALPATH'].split('/')[-2]
				return index
		return index

	# 获得每个日期开发者的commit次数
	def get_CommitTimesListByDay(self, table_name):
		# 数据原型
		datas = [
			['contributor', '没有', '这个', '对应的','数据'],
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

	def print_format_datas(self, datas):
		for data in datas:
			for item in data:
				print(item, '\t', end="")
			print()


if __name__ == '__main__':
	repoDB = repoDB_Options()
	datas = repoDB.get_CommitTimesListByDay('CommitTimesListByDay1')
	repoDB.print_format_datas(datas)