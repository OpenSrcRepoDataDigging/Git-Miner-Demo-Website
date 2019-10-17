from flask import Flask, g, current_app, render_template
import os
import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from BlogForms import LoginForm, RegisterForm, UploadForm, BlogForm, DeleteForm,Search_Form
import uuid
import time
from DB_options import  DB_options,SQLite_Options


app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.before_request
def before_request():
    g.conn = sqlite3.connect('library.db')
    g.conn.row_factory = sqlite3.Row
    g.cur = g.conn.cursor()

@app.teardown_request
def teardown(error):
    if hasattr(g,'conn'):
        g.conn.close()



# 主页
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('input_url.html')
    else:
        return redirect(url_for('mooc'))

# Github
@app.route('/input_url')
def input_url():
    return render_template('study_basic.html')

# 博客
@app.route('/study')
def study():
    if not session.get('logged_in'):
        return render_template('study_basic.html')
    else:
        username = session.get('username')
        sql = SQLite_Options()
        contents = sql.getStudentsCourses(username)
        return render_template(
            'study.html',
            username = username,
            contents = contents
        )
    
# 图书馆
def get_real_list(librarys, cname='', key='', teacher=''):

    res = librarys
    '''
        这里有个注意点，就是返回值是Row 对象，而不是字典。 Row 对象是 namedtuple
    '''
    if cname != '' or key != '' or teacher != '':
        print('key:', key,' author:', teacher)
        outList = []
        for rows in librarys:
            flag = False
            if cname != '':  # 有课程名，优先课程名
                if rows['cname'] == cname:
                    flag = True
            else:
                if key != '' and  teacher != '':
                    if rows['cname'].__contains__(key) and rows['teacher'].__contains__(teacher):
                        flag = True
                elif key != '' and rows['cname'].__contains__(key):
                    print("key != None",key != None,"筛选key：",rows['cname'])
                    flag = True
                elif teacher != '' and rows['teacher'].__contains__(teacher):
                    print("teacher != None", teacher != None, "筛选teacher：", rows['cname'])
                    flag = True
                else:
                    flag = False

            if flag:
                print("筛选课程：",rows['cname'])
                outList.append(rows)
        res = outList

    return res

@app.route('/mooc',methods=['GET','POST'])
def mooc():
    if not session.get('logged_in'):
        return render_template('study_basic.html')
    else:
        username = session.get('username')
        sql = SQLite_Options()  # 管理前期数据库操作的类
        librarys = sql.select('COURSE')
        form = Search_Form()

        skey = ''
        sauthor = ''
        scname = ''
        if form.validate_on_submit():
            scname = form.cname.data
            skey = form.key.data
            sauthor = form.author.data

        searches =get_real_list(librarys, cname = scname, key=skey, teacher=sauthor)

        return render_template(
            'mooc.html',
            librarys = librarys,
            searches = searches,
            form = form,
            username=username,
        )

@app.route('/study-content/<blog_title>')
def get_blog_content(blog_title):
    username = session.get('username')
    db = DB_options()
    print("查询%s发布过的内容" % (username))
    contents = db.get_contents(username=username)
    content = ''
    for items in contents:
        if items['title'] == blog_title:
            content = items

    return render_template(
        'study_content.html',
        username=username,
        content=content
    )

@app.route('/study-content')
def study_content():
    if not session.get('logged_in'):
        return render_template('study_basic.html')
    else:
        return render_template(
            'study_content.html',
            username = session.get('username')
        )

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template(
        'login.html',
        form=form
    )

@app.route('/action_login', methods=['POST'])
def action_login():
    form = LoginForm()
    if form.validate_on_submit():
        sql = SQLite_Options()
        users = sql.select('STUDENTS')

        for user in users:
            if user['sid'] == (form.username.data) and user['password'] == (form.password.data):
                flash('登陆成功')
                # flash(form.username.data)
                # flash(form.password.data)
                session['logged_in'] = True
                session['username'] = form.username.data
                return redirect(url_for('mooc'))
        flash('密码错误或账号不存在')

    return render_template(
        'login.html',
        form=form
    )


# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template(
        'register.html',
        form=form
    )


@app.route('/action_register', methods=['POST'])
def action_register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.register.data:
            sql = SQLite_Options()
            users = sql.select('STUDENTS')
            primary_key_flag = False # 是否数据库里已经有该账号
            for user in users:
                if user['sid'] == (form.username.data):
                    primary_key_flag = True
                    break

            print("账户是否存在",primary_key_flag)


            if primary_key_flag == True:
                flash('该用户已经被注册过')
                #TODO:这里应该有用户名重复的问题,应该用Alert会好一些
                return render_template(
                    'register.html',
                    form=form
                )
            else:
                sql.insertUsers(form.username.data,form.password.data)
                flash('注册成功')
                return redirect(url_for('login'))


    return render_template(
        'register.html',
        form=form
    )

# 用户注销
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return home()

# 快捷登录 便于测试
@app.route('/quick_login',methods=['GET', 'POST'])
def quick_login():
    session['logged_in'] = True
    session['username'] = '1001'
    return home()

# MySQL数据展示
@app.route('/sql_test')
def sql_display():
    sql = SQLite_Options() #  管理前期数据库操作的类
    authors = sql.select('STUDENTS')
    librarys = sql.select('COURSE')
    list = sql.select('STUDY')
    return render_template(
        "sql_test.html",
        authors=authors,
        librarys = librarys,
        list = list
    )

@app.route('/upload/<path:filename>')
def get_file(filename):
    print('get_file:',filename)
    return send_from_directory(app.root_path+'\\uploads',filename)

@app.route('/study/<path:cid>')
def choose_course(cid):
    print('choose',cid)
    username = session.get('username')
    sql = SQLite_Options()
    sql.selectCourse(sid=username,cid=cid)
    return redirect(url_for('mooc'))

@app.route('/study/study_course/<path:cid>')
def study_course(cid):
    flash('学习'+cid)
    username = session.get('username')
    sql = SQLite_Options()
    sql.studyCourse(sid=username,cid=cid)
    return redirect(url_for('study'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()
