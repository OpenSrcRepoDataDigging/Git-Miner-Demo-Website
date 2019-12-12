from pprint import pprint

import pymysql
import sqlite3
import getpass
import numpy as np


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

    # TODO:展示仓库的基本信息
    def get_repo_base_information(self, repo_name):
        res = dict()
        res['commits'] = 0  # commits总数
        res['contributors'] = 0  # contributors数量
        res['start_time'] = '2010'  # 建立时间
        res['top_ten_commits'] = []
        for i in range(10):
            res['top_ten_commits'].append({'name': 'x' + str(i), 'commits': 10 - i})
        # 下面是弗雷歇距离参照 https://www.echartsjs.com/examples/en/editor.html?c=dataset-encode0&theme=light
        source = [
            ['frechet', 'commits', 'contributor'],
            [89.3, 58212, 'Matcha Latte'],
            [57.1, 78254, 'Milk Tea'],
            [74.4, 41032, 'Cheese Cocoa'],
            [50.1, 12755, 'Cheese Brownie'],
            [89.7, 20145, 'Matcha Cocoa'],
            [68.1, 79146, 'Tea'],
            [19.6, 91852, 'Orange Juice'],
            [10.6, 101852, 'Lemon Juice'],
            [32.7, 20112, 'Walnut Brownie']
        ]
        res['top_ten_frechet'] = source
        res['max_frechet'] = 100
        # TODO: try except
        # return res

        index = self.get_repo_index(repo_name)
        # 实现前十的commit对应关系
        db_name = "LOCSumLastCommit" + str(index)
        topten = []
        topname = []
        topcommits = []
        infor = self.execute("select name from {} order by commits desc ".format(db_name))
        for i in infor:
            for j in i:
                topname.append(j)
        infor = self.execute("select commits from {} order by commits desc ".format(db_name))
        for i in infor:
            for j in i:
                topcommits.append(j)
        for i in range(min(10, topname.__len__())):
            tmprow = dict()
            tmprow['name'] = topname[i]
            tmprow['commits'] = topcommits[i]
            topten.append(tmprow)
        res['top_ten_commits'] = topten
        # 计数
        commit_sum = 0
        for i in range(topcommits.__len__()):
            commit_sum += int(topcommits[i])
        res['commits'] = commit_sum
        res['contributors'] = topname.__len__()
        # TODO :还要加上最早时间
        # TODO：现在从0开始构建，没有这些文件，Run不起来呀
        source = []
        header = ['frechet', 'commits', 'contributor']
        source.append(header)
        # TODO:获得前缀路径
        dirpath = self.get_repo_path_prefix(repo_name)
        filename = dirpath + "OvR_Normal_Divide_day.csv"
        topfilename = dirpath + "frechet_topday.csv"
        allindex = []
        allcommit = []
        allname = []
        max_frechet = 0
        with open(topfilename, 'r')as top:
            for line in top.readlines():
                line = line.strip()
                line = line.split(',')
                allindex.append(int(line[0]))
                allcommit.append(int(line[2]))
                allname.append(line[1])
        with open(filename, 'r')as f:
            line = f.readline()
            line = f.readline()
            line = line.strip()
            line = line.split(',')
            for i in range(len(allindex)).__reversed__():
                insertrow = []
                index = allindex[i]
                frechetnum = float(line[index + 1]) * 10000
                if frechetnum > max_frechet:
                    max_frechet = frechetnum

                insertrow.append(frechetnum)
                insertrow.append(allcommit[i])
                insertrow.append(allname[i])
                source.append(insertrow)
        print('top10_new:',source)
        print('top10_old:',res['top_ten_frechet'])
        res['max_frechet'] = max_frechet
        res['top_ten_frechet'] = source
        return res

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
                    # 判断是否内容为空
                    content = self.execute("select * from {}".format(table_name))
                    if not content:
                        return False
                    else:
                        return True
        return False

    # 获得序号
    def get_repo_index(self, repo_name):
        repo_status = self.get_repo_status()
        index = "null"
        for repo in repo_status:
            if (repo['REPONAME'] == repo_name):
                index = repo['REPOLOCALPATH'].split('/')[-2]
                return index
        return index

    # 获得每个日期开发者的commit次数
    def get_CommitTimesListByDay(self, table_name):
        res = dict()
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
        classify = dict()
        classify['date'] = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        classify['add'] = [120, 132, 101, 134, 90, 230, 210]
        classify['delete'] = [220, 182, 191, 234, 290, 330, 310]
        classify['mod'] = [150, 232, 201, 154, 190, 330, 410]
        classify['fix'] = [320, 332, 301, 334, 390, 330, 320]

        res['commits_list'] = datas
        res['commits_classify'] = classify

        barcodes = dict()
        barcode = dict()
        hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
                 '7a', '8a', '9a', '10a', '11a',
                 '12p', '1p', '2p', '3p', '4p', '5p',
                 '6p', '7p', '8p', '9p', '10p', '11p',
                 '12a', '1a', '2a', '3a', '4a', '5a', '6a',
                 '7a', '8a', '9a', '10a', '11a',
                 '12p', '1p', '2p', '3p', '4p', '5p',
                 '6p', '7p', '8p', '9p', '10p', '11p'
                 ]
        days = ['']
        data = [[0, 0, 5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0], [0, 8, 0],
                [0, 9, 0], [0, 10, 0], [0, 11, 2], [0, 12, 4], [0, 13, 1], [0, 14, 1], [0, 15, 3], [0, 16, 4],
                [0, 17, 6], [0, 18, 4], [0, 19, 4], [0, 20, 3], [0, 21, 3], [0, 22, 2], [0, 23, 5],
                [0, 24, 5], [0, 25, 1], [0, 26, 0], [0, 27, 0], [0, 28, 0], [0, 29, 0], [0, 30, 0], [0, 31, 0],
                [0, 32, 0],
                [0, 33, 0], [0, 34, 0], [0, 35, 2], [0, 36, 4], [0, 37, 1], [0, 38, 1], [0, 39, 3], [0, 40, 4],
                [0, 41, 6], [0, 42, 4], [0, 43, 4], [0, 44, 3], [0, 45, 3], [0, 46, 2], [0, 47, 5]
                ]
        barcode['x'] = hours
        barcode['y'] = days
        barcode['data'] = data
        barcode['max'] = 6

        barcodes['all'] = barcode
        barcodes['top'] = []
        for i in range(5):
            barcodes['top'].append(barcode)

        res['barcodes'] = barcodes

        # 计算BarCode
        if self.is_table_exist(table_name):
            x_axis = []
            y_axis = ['']
            data_axis = []
            date_raw = self.execute("select Date from {}".format(table_name))
            for i in date_raw:
                for j in i:
                    x_axis.append(j)

            infor = self.get_col_and_datas(table_name)
            for i in range(1, infor.__len__()):
                newdata = []
                newdata.append(0)  # y_axis
                newdata.append(i - 1)  # x_axis
                newdata.append(infor[i][1])
                data_axis.append(newdata)
            barcode = dict()
            barcode['x'] = x_axis
            barcode['y'] = y_axis
            barcode['data'] = data_axis
            barcode['max'] = 6
            barcodes['all'] = barcode
            # 上面计算的是整个项目的barcode，接下来计算commit前五的人
            # 先统计个数：
            commits_sum = []
            name_all = []
            for i in range(2, infor[0].__len__()):
                name = infor[0][i]
                name_all.append(name)
                data_row = self.execute("select sum(\"{}\") from {}".format(name, table_name))
                for tmpi in data_row:
                    for tmpj in tmpi:
                        commits_sum.append(int(tmpj))
            sequence = np.argsort(commits_sum)
            barcodes['top'] = []
            for i in range(min(5, sequence.__len__())):
                index = sequence[len(sequence) - 1 - i]
                name = name_all[index]
                print(name)
                commit = commits_sum[index]
                tmp_data_axis = []
                for row in range(1, infor.__len__()):
                    newdata = []
                    newdata.append(0)
                    newdata.append(row - 1)
                    newdata.append(infor[row][index + 2])
                    tmp_data_axis.append(newdata)
                tmpbarcode = dict()
                tmpbarcode['x'] = x_axis
                tmpbarcode['y'] = y_axis
                tmpbarcode['data'] = tmp_data_axis
                tmpbarcode['max'] = 6
                barcodes['top'].append(tmpbarcode)
            res['barcodes'] = barcodes

        if self.is_table_exist(table_name):
            res['commits_list'] = self.get_col_and_datas(table_name)
            classify_table_name = str(table_name).replace('CommitTimesListByDay', 'ClassifiedCommitList')
            res['commits_classify'] = self.get_ClassifiedCommitList(classify_table_name)
        else:
            print("表", table_name, "不存在")
        return res

    # TODO: 从数据库读取格式化数据
    # Finish 2019/12/8，由于不明确所以这里实现的只是总的commit四个类别随时间的图表
    def get_ClassifiedCommitList(self, table_name):
        res = dict()
        res['date'] = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        res['add'] = [120, 132, 101, 134, 90, 230, 210]
        res['delete'] = [220, 182, 191, 234, 290, 330, 310]
        res['mod'] = [150, 232, 201, 154, 190, 330, 410]
        res['fix'] = [320, 332, 301, 334, 390, 330, 320]

        if self.is_table_exist(table_name):
            date_raw = self.execute("select Date from {}".format(table_name))
            dates = []
            for i in date_raw:
                for j in i:
                    dates.append(j)
            res['date'] = dates
            classifiedcommit = []
            '''
			all_col = self.execute("select LeoDarcy from {}".format(table_name))
			for i in date_raw:
				for j in i:
					classifiedcommit.append(j)'''
            all_col = self.get_col_and_datas(table_name)
            for i in range(1, len(dates)):
                classifiedcommit.append(all_col[i][1])
            adddata = []
            deldata = []
            moddata = []
            fixdata = []
            for line in classifiedcommit:
                parts = line.split('-')
                adddata.append(int(parts[0]))
                deldata.append(int(parts[1]))
                moddata.append(int(parts[2]))
                fixdata.append(int(parts[3]))
            res['date'] = dates
            res['add'] = adddata
            res['delete'] = deldata
            res['mod'] = moddata
            res['fix'] = fixdata

        else:
            print("表", table_name, "不存在")
        # print(res)
        return res

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
        datas['max'] = 10

        nodes, links = self.get_ContributorNetworkGraph(table_name)
        datas['nodes'] = nodes
        datas['links'] = links

        if self.is_table_exist(table_name):
            names_raw = self.execute("select name from {}".format(table_name))
            names = []
            for i in names_raw:
                for j in i:
                    names.append(j)
            infos = self.get_col_and_datas(table_name)
            data = []
            max = 10
            for i in range(1, infos.__len__()):
                for j in range(1, infos[0].__len__()):
                    data.append([i - 1, j - 1, infos[i][j]])
                    if infos[i][j] > max:
                        max = infos[i][j]

            datas['x'] = names
            datas['y'] = names
            datas['data'] = data
            datas['max'] = max
        else:
            print("表", table_name, "不存在")

        return datas

    def get_FileContributorMatrix(self, table_name):
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
        datas['max'] = 10

        # return datas

        if self.is_table_exist(table_name):
            filenames_raw = self.execute("select filename from {}".format(table_name))
            filenames = []
            for i in filenames_raw:
                for j in i:
                    filenames.append(j)
            infos = self.get_col_and_datas(table_name)
            data = []
            max = 10
            for i in range(1, infos[0].__len__()):
                for j in range(1, infos.__len__()):
                    data.append([j - 1, i - 1, infos[j][i]])
                    if infos[j][i] > max:
                        max = infos[j][i]

            datas['x'] = infos[0][1:]
            datas['y'] = filenames

            datas['data'] = data
            datas['max'] = max
        else:
            print("表", table_name, "不存在")

        return datas

    # TODO: 从数据库获取数据自定义节点和边
    # Finish dot 建议传入的是repo_name,因为需要打开两个表
    def get_ContributorNetworkGraph(self, table_name):
        # node，表示关系图的节点，除了name，其他可以自定义成任何东西，比如commit，LOC之类的
        nodes = [{
            'name': '南小紫',
            'creditPts': 97,
            'financialPts': 85,
            'schoolPts': 67,
        }, {
            'name': '张秀英',
            'creditPts': 97,
            'financialPts': 85,
            'schoolPts': 67,
            'creditChange': 1,
        }, {
            'name': '曹老板',
            'creditPts': 97,
            'financialPts': 85,
            'schoolPts': 67,
            'creditChange': 1,
        }]
        # links，表示关系图的边，除了source,target，其他可以自定义成任何东西，需要注意的是width最好是协作的权重
        links = [{
            'source': '南小紫',
            'target': '张秀英',
            'name': '同学',
            'relation': '您最近的关系没什么变化',
            'lineStyle': {
                'normal': {
                    'type': 'dashed',
                    'width': 5
                }
            },
        }, {
            'source': '曹老板',
            'target': '张秀英',
            'name': '压迫',
            'relation': '您最近的关系没什么变化',
            'lineStyle': {
                'normal': {
                    'type': 'solid',
                    'width': 3
                }
            },
        }, {
            'source': '曹老板',
            'target': '南小紫',
            'name': '压迫',
            'relation': '您最近的关系没什么变化',
            'lineStyle': {
                'normal': {
                    'type': 'solid',
                    'width': 10
                }
            },
        }]

        if self.is_table_exist(table_name):
            # TODO: 下面又跑不动了
            nodes = []
            links = []
            # TODO 获得名字与commit数量的关系
            name_commit_dic = {}
            name_commit_table_name = str(table_name).replace("CommitTimesListByDay", "LOCSumLastCommit")
            all_infor = self.get_col_and_datas(name_commit_table_name)
            for i in range(1, all_infor.__len__()):
                member_name = all_infor[i][0]
                menmber_commit = all_infor[i][1]
                name_commit_dic[member_name] = int(menmber_commit)

            name_raw = self.execute("select Name from {}".format(table_name))
            members = []
            for i in name_raw:
                for j in i:
                    members.append(j)
                    newtmp = {}
                    newtmp['name'] = j
                    if name_commit_dic.__contains__(j):
                        newtmp['commit'] = name_commit_dic[j]
                    else:
                        newtmp['commit'] = -1
                    nodes.append(newtmp)
            all_info = self.get_col_and_datas(table_name)

            max = 0
            for i in range(1, all_info.__len__()):
                for j in range(1, i):
                    relation = int(all_info[i][j])
                    if relation > max:
                        max = relation

            WIDTH_DIV = max/5 #改为相对值
            for i in range(1, all_info.__len__()):
                for j in range(1, i):
                    relation = int(all_info[i][j])
                    newlink = {}
                    newlink['source'] = members[i - 1]
                    newlink['target'] = members[j - 1]
                    newlink['relation'] = relation
                    newlink['lineStyle'] = {'normal': {'type': 'solid', 'width': relation / WIDTH_DIV}}
                    links.append(newlink)
            print(nodes, links)
            return nodes, links
        else:
            print("表", table_name, "不存在")

        return nodes, links

    # 格式化输出
    def print_format_datas(self, datas):
        for data in datas:
            for item in data:
                print(item, '\t', end="")
            print()

    # 得到前缀，包括序号的，比如/home/username/.gitminer/0/
    def get_repo_path_prefix(self, repo_name):
        prefix = '/home/' + getpass.getuser() + '/.gitminer/'
        prefix = prefix + str(self.get_repo_index(repo_name)) + '/csv/'
        return prefix


if __name__ == '__main__':
    repoDB = repoDB_Options()
    table_name = "FileContributorMatrix6"
    datas = repoDB.get_FileContributorMatrix(table_name)
    infos = repoDB.get_col_and_datas(table_name)
    # datas = repoDB.get_ClassifiedCommitList("ClassifiedCommitList0")
    # datas, newdatas = repoDB.get_ContributorNetworkGraph("ContributorNetworkMatrix0")
    # datas = repoDB.get_repo_base_information("a")
