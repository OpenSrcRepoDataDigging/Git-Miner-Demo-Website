import pymysql
import sqlite3
import numpy

class SQLite_Options():
    def create_database(self):
        conn = sqlite3.connect('MOOC.db')
        print("Opened database successfully")
        conn.close()

    def create_table(self):
        conn = sqlite3.connect('MOOC.db')
        c = conn.cursor()
        
        """ 创建课程表 COURSE"""
        c.execute('''
        DROP TABLE IF EXISTS COURSE;
        ''')
        c.execute('''
        CREATE TABLE COURSE(
                CID TEXT PRIMARY KEY     NOT NULL,
                CNAME   TEXT    NOT NULL,
                TEACHER    TEXT    NOT NULL,
                MAX_COUNT  INT    NOT NULL,
                COUNT   INT    NOT NULL);
        ''')
        print("TABLE COURSE created successfully")
        
        """ 创建学生表 STUDENTS"""
        c.execute('''
        DROP TABLE IF EXISTS STUDENTS;
        ''')
        c.execute('''
        CREATE TABLE STUDENTS(
                SID   TEXT PRIMARY KEY     NOT NULL,
                PASSWORD   TEXT    NOT NULL);
        ''')
        print("TABLE STUDENTS created successfully")

        """ 创建选课表 STUDY"""
        c.execute('''
        DROP TABLE IF EXISTS STUDY;
        ''')
        c.execute('''
        CREATE TABLE STUDY(
                SID   TEXT    NOT NULL,
                CID   TEXT    NOT NULL,
                PROGRESS REAL NOT NULL,
                foreign key(SID) references STUDENTS(SID),
                foreign key(CID) references COURSE(CID));
        ''')
        print("TABLE STUDY created successfully")

        conn.commit()
        conn.close()


    def get_List(self):
        listA = [
            {'cid': 1, 'cname': '大学语文', 'teacher': '金老师', 'max_count': 20, 'count': 0},
            {'cid': 2, 'cname': '大学数学', 'teacher': '陈老师', 'max_count': 20, 'count': 0},
            {'cid': 3, 'cname': '大学英语', 'teacher': '莎老师', 'max_count': 20, 'count': 0},
            {'cid': 4, 'cname': '大学历史', 'teacher': '汪老师', 'max_count': 20, 'count': 0},
            {'cid': 5, 'cname': '大学地理', 'teacher': '李老师', 'max_count': 20, 'count': 0},
            {'cid': 6, 'cname': '大学化学', 'teacher': '张老师', 'max_count': 20, 'count': 0},
        ]

        return listA

    def insertCourses(self):
        conn = sqlite3.connect('MOOC.db')
        print("Opened database successfully")
        c = conn.cursor()

        listA = self.get_List()

        for item in listA:
            # 用这个方法写，比较容易测试参数啥的
            data = (item['cid'], item['cname'], item['teacher'], item['max_count'], item['count'])
            print(data)
            c.execute("INSERT INTO COURSE (CID,CNAME,TEACHER,MAX_COUNT,COUNT) VALUES (?,?,?,?,?)", data);

        conn.commit()
        print("Records created successfully")
        conn.close()



    def insertUsers(self,username=None,password=None):
        conn = sqlite3.connect('MOOC.db')
        print("Opened database successfully")
        c = conn.cursor()

        listA = []
        if username==None and password == None :
            listA = [
                {'sid': '1001', 'password': 'a123456'},
                {'sid': '1002', 'password': 'b123456'},
                {'sid': '1003', 'password': 'c123456'},
            ]
        else:
            listA.append({'sid': username,'password':password})

        for item in listA:
            # 用这个方法写，比较容易测试参数啥的
            data = (item['sid'], item['password'])
            print(data)
            c.execute("INSERT INTO STUDENTS (SID,PASSWORD) VALUES (?,?)", data);

        conn.commit()
        print("Records created successfully")
        conn.close()

    def insertList(self):
        conn = sqlite3.connect('MOOC.db')
        print("Opened database successfully")
        c = conn.cursor()

        listA = [
            {'sid': '1001','cid': 1,'progress':0.25},
            {'sid': '1002','cid': 1,'progress':0.25},
            {'sid': '1002','cid': 2,'progress':0.25},
            {'sid': '1001','cid': 1,'progress':0.25},
            {'sid': '1001','cid': 2,'progress':0.25},
            {'sid': '1001','cid': 1,'progress':0.25},
        ]

        for item in listA:
            # 用这个方法写，比较容易测试参数啥的
            data = (item['sid'], item['cid'],item['progress'])
            print(data)
            c.execute("INSERT INTO STUDY (SID,CID,PROGRESS) VALUES (?,?,?)", data);

        conn.commit()
        print("Records created successfully")
        conn.close()

    def select(self,TABLE):
        conn = sqlite3.connect('MOOC.db')
        conn.row_factory = sqlite3.Row
        print("Opened database successfully")
        c = conn.cursor()

        cursor = c.execute("SELECT * from "+TABLE)
        datas = cursor.fetchall()
        print(datas)
        for data in datas:
            print(data)
        conn.close()
        return datas

    def getStudentsCourses(self,sid):
        conn = sqlite3.connect('MOOC.db')
        conn.row_factory = sqlite3.Row
        print("Opened database successfully")
        c = conn.cursor()
        cursor = c.execute("SELECT * from STUDY WHERE SID="+sid)
        datas = cursor.fetchall()
        # print(datas)
        for data in datas:
            for it in data:
                print(it)
            print(data[0])
        conn.close()
        return datas

    def selectCourse(self,sid,cid):
        conn = sqlite3.connect('MOOC.db')
        conn.row_factory = sqlite3.Row
        print("Opened database successfully")
        c = conn.cursor()

        #  得到该课的信息
        courses = self.select('COURSE')
        max_counts = 0
        counts = 0
        for item in courses:
            if item['cid'] == cid:
                max_counts = item['max_count']
                counts = item['count']
        if counts >= max_counts:
            return  False
        else:
            studies = self.select('STUDY')
            for item in studies:
                if item['sid'] == sid and item['cid'] == cid:
                    return  False

            cursor = c.execute("UPDATE COURSE SET COUNT ="+ str(counts+1)+" WHERE CID = "+cid)
            item = {'sid': sid,'cid': cid,'progress':0}
            data = (item['sid'], item['cid'],item['progress'])
            c.execute("INSERT INTO STUDY (SID,CID,PROGRESS) VALUES (?,?,?)", data);            conn.commit()
            conn.close()
            return True

    def studyCourse(self,sid,cid):
        conn = sqlite3.connect('MOOC.db')
        conn.row_factory = sqlite3.Row
        print("Opened database successfully")
        c = conn.cursor()

        #  得到该课的信息

        studies = self.select('STUDY')
        progress = 0
        for item in studies:
            if item['sid'] == sid and item['cid'] == cid:
                progress = item['progress']

        if progress == 1:
            return True
        else :
            progress = progress + 0.25
        cursor = c.execute("UPDATE STUDY SET PROGRESS ="+ str(progress)+" WHERE CID = "+cid + " AND SID= "+sid)
        conn.close()
        return True

class DB_options():

    #与数据库的连接

    flag = True
    NULL_PICTURE_MAGIC = "NULL_PICTURE_SOSAD"


    def getConnect(self):
        coon = pymysql.connect(
            host='localhost',
            port=3306,
            user='Young',
            password='123456',
            database='flask',
            autocommit = True  # 插入数据一开始失败就是因为这个幺儿
        )
        return coon

    def init_database(self):
        if self.flag:
            print("初始化数据库")
            self.flag = False
        else:
            print("已初始化")
            return

        conn = self.getConnect()
        cur = conn.cursor()
        sql1 = "DROP TABLE if EXISTS authors"
        sql2 = "CREATE TABLE authors (\
                username VARCHAR(255) NOT NULL,\
                password VARCHAR(255) NOT NULL,\
                PRIMARY KEY (username));"
        sql3 = "DROP TABLE if EXISTS contents"
        sql4 = "CREATE TABLE contents (\
              username VARCHAR(255) NOT NULL,\
              title VARCHAR(255) NULL,\
              content TEXT(65535) NULL,\
              date DATE NULL,\
              imgurl VARCHAR(255) NULL,\
              foreign key(username) references authors(username))"

        # 维护外键的一致性（= =竟然被这个坑到了）
        cur.execute(sql3)
        cur.execute(sql1)

        cur.execute(sql2)
        cur.execute(sql4)

        result = cur.fetchall()
        print(result)
        cur.close()
        conn.close()

    def register(self,user,psw):
        #TODO:主键会插入异常
        print("插入一条注册信息")
        conn = self.getConnect()
        cur = conn.cursor()
        cur.execute('INSERT INTO authors(username,password) VALUES ("%s", "%s")'%(user,psw))
        print("插入成功")
        cur.close()
        conn.close()

    def select(self):
        conn = self.getConnect()
        cur = conn.cursor()
        sql = "select * from authors"
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        cur.close()
        conn.close()
        return result

    def get_users(self):
        conn = self.getConnect()
        cur = conn.cursor()
        sql = "select * from authors"
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()

        authors = []
        for row in result:
            username = row[0]
            password = row[1]
            # 打印结果
            authors.append({
                'username': username,
                'password': password
            })
            print("username=%s,password=%s" % \
                  (username, password))

        return authors

    def get_contents(self,username="select_all_users"):
        conn = self.getConnect()
        cur = conn.cursor()
        if username == "select_all_users":
            sql = "select * from contents"
        else:
            sql = 'select * from contents where username = "%s"'%(username)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()

        contents = []
        for row in result:
            username = row[0]
            title = row[1]
            content = row[2]
            date = row[3]
            image = row[4]

            if image == self.NULL_PICTURE_MAGIC:
                image = '1.jpg'

            # 打印结果
            contents.append({
                'username': username,
                'title': title,
                'content':content,
                'date':date,
                'image':image
            })
            print("username=%s,title=%s,content=%s,date=%s,image=%s" % \
                  (username, title, content, date,image))

        return contents

    def delete_content(self,username,title):
        print("删除一条内容")
        conn = self.getConnect()
        cur = conn.cursor()
        cur.execute('DELETE FROM flask.contents WHERE username="%s" AND title ="%s"'%(username,title))
        print("插入成功")
        cur.close()
        conn.close()

    def insert_content(self,username,title,content,date,image= NULL_PICTURE_MAGIC):
        print("插入一条内容信息")
        conn = self.getConnect()
        cur = conn.cursor()
        cur.execute('INSERT INTO flask.contents VALUES ("%s","%s","%s","%s","%s")'%(username,title,content,date,image))
        print("插入成功")
        cur.close()
        conn.close()

if __name__ == '__main__':

    sql = SQLite_Options() #  管理前期数据库操作的类
    # sql.create_database() #  创建数据库
    # sql.create_table() #  建表
    # sql.insertCourses()
    # sql.insertUsers()
    # sql.insertList()
    # sql.select('COURSE')
    # sql.select('STUDENTS')
    # sql.select('STUDY')
    sql.getStudentsCourses('1001')

