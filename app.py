from flask import Flask, g, current_app, render_template
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from BlogForms import LoginForm, RegisterForm, UploadForm, BlogForm, DeleteForm, Search_Form, GitCloneForm
import uuid
import time
from DB_options import DB_options, SQLite_Options
from JavaGitMiner import GitMiner
from repoDB_Options import repoDB_Options

app = Flask(__name__)
app.secret_key = os.urandom(12)
git_miner = GitMiner()
repoDB = repoDB_Options()
executor = ThreadPoolExecutor(5)


@app.before_request
def before_request():
	g.conn = sqlite3.connect('library.db')
	g.conn.row_factory = sqlite3.Row
	g.cur = g.conn.cursor()


@app.teardown_request
def teardown(error):
	if hasattr(g, 'conn'):
		g.conn.close()


# 主页
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('repositories_basic.html')
	else:
		return redirect(url_for('mooc'))


# Github
@app.route('/input_url')
def input_url():
	return render_template('input_url.html')


# 展示目前已经有的git项目
@app.route('/repositories')
def repositories():
	if not session.get('logged_in'):
		return render_template('repositories_basic.html')
	else:
		username = session.get('username')
		repo_status = repoDB.get_repo_status()
		return render_template(
			'repositories.html',
			username=username,
			repo_status=repo_status
		)


# 输入一个url,然后git clone
@app.route('/gitclone', methods=['GET', 'POST'])
def mooc():
	if not session.get('logged_in'):
		return render_template('repositories_basic.html')
	else:
		username = session.get('username')
		form = GitCloneForm()

		return render_template(
			'gitclone.html',
			username=username,
			form=form,
		)


# 实际对git clone进行处理
@app.route('/action_clone', methods=['POST'])
def action_clone():
	if not session.get('logged_in'):
		return render_template('repositories_basic.html')
	else:
		username = session.get('username')
		form = GitCloneForm()
		url = ''
		if form.validate_on_submit():
			url = form.url.data
			# 保证都有数据
			git_miner.git_clone("https://github.com/MirageLyu/test.git")
			if len(url) == 0:
				flash("未输入URL，直接进入")
				return redirect(url_for('repositories'))
			else:
				# 异步执行任务
				executor.submit(git_miner.git_clone, url)
				return redirect(url_for('repositories'))

		return render_template(
			'gitclone.html',
			username=username,
			form=form,
		)


# 废弃
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
		'repositories_content.html',
		username=username,
		content=content
	)


@app.route('/repositories_content')
def repositories_content():
	if not session.get('logged_in'):
		return render_template('repositories_basic.html')
	else:
		return render_template(
			'repositories_content.html',
			username=session.get('username')
		)


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	return render_template(
		'login.html',
		form=form
	)


# 用户登录
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


# 用户注册（Git项目暂不需要）
@app.route('/action_register', methods=['POST'])
def action_register():
	form = RegisterForm()
	if form.validate_on_submit():
		if form.register.data:
			sql = SQLite_Options()
			users = sql.select('STUDENTS')
			primary_key_flag = False  # 是否数据库里已经有该账号
			for user in users:
				if user['sid'] == (form.username.data):
					primary_key_flag = True
					break

			print("账户是否存在", primary_key_flag)

			if primary_key_flag == True:
				flash('该用户已经被注册过')
				# TODO:这里应该有用户名重复的问题,应该用Alert会好一些
				return render_template(
					'register.html',
					form=form
				)
			else:
				sql.insertUsers(form.username.data, form.password.data)
				flash('注册成功')
				return redirect(url_for('login'))

	return render_template(
		'register.html',
		form=form
	)


# 用户注销（Git项目暂不需要）
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['logged_in'] = False
	return home()


# 快捷登录 便于测试
@app.route('/quick_login', methods=['GET', 'POST'])
def quick_login():
	session['logged_in'] = True
	session['username'] = '测试用户'
	return home()


# 数据库数据展示
@app.route('/sql_test')
def sql_display():
	repoDB = repoDB_Options()
	repo_status = repoDB.get_repo_status()
	return render_template(
		"sql_test.html",
		repo_status=repo_status,
	)


# 获取图片地址
@app.route('/upload/<path:filename>')
def get_file(filename):
	print('get_file:', filename)
	file_url = send_from_directory(app.root_path + '\\uploads', filename)
	print('file_url', file_url)
	return file_url


# 废弃（Git项目暂不需要）
@app.route('/repositories/<path:cid>')
def choose_repository(cid):
	print('choose', cid)
	username = session.get('username')
	sql = SQLite_Options()
	sql.selectCourse(sid=username, cid=cid)
	return redirect(url_for('mooc'))

@app.route('/repositories/how_file_contributor_matrix/<repo_name>')
def show_file_contributor_matrix(repo_name):
	index = repoDB.get_repo_index(repo_name)
	# 文件贡献图
	file_contributor_matrix = repoDB.get_FileContributorMatrix('FileContributorMatrix' + index)
	print('file_contributor_matrix', file_contributor_matrix)
	return render_template(
		"repositories_graph.html",
		file_contributor_matrix=file_contributor_matrix,
		repo_name = repo_name
	)


# 查看项目具体信息
@app.route('/repositories/show_repositories/<repo_name>')
def show_repositories(repo_name):
	username = session.get('username')
	# TODO: 这里需要从数据库读取数据
	index = repoDB.get_repo_index(repo_name)
	# commit次数，贡献者，日期
	commit_times_list_by_day = repoDB.get_CommitTimesListByDay('CommitTimesListByDay' + index)
	print('commit_times_list_by_day', commit_times_list_by_day)
	# 协作关系图
	contributor_network_matrix = repoDB.get_ContributorNetworkMatrix('ContributorNetworkMatrix' + index)
	print('contributor_network_matrix', contributor_network_matrix)
	# 文件贡献图
	file_contributor_matrix = repoDB.get_FileContributorMatrix('FileContributorMatrix' + index)
	print('file_contributor_matrix', file_contributor_matrix)
	# 仓库基本信息
	repo_base_information = repoDB.get_repo_base_information(repo_name)
	print('repo_base_information', repo_base_information)

	return render_template(
		"repositories_content.html",
		username=username,
		repo_name = repo_name,
		commit_times_list_by_day=commit_times_list_by_day,
		contributor_network_matrix=contributor_network_matrix,
		file_contributor_matrix=file_contributor_matrix,
		repo_base_information = repo_base_information
	)


if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run()
