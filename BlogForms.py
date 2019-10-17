from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_wtf.file import  FileField,FileRequired,FileAllowed

#登陆，注册表单
class BaseLR_Form(FlaskForm):
    username = StringField('用户名', render_kw={'placeholder': '账户'}, validators=[DataRequired(message=u'请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])

class LoginForm(BaseLR_Form):
    remember = BooleanField('记住密码')
    login = SubmitField('登陆')

class RegisterForm(BaseLR_Form):
    email = StringField('E-Mail', validators=[DataRequired(message=u'请输入邮箱')])
    register = SubmitField('注册')

# 文件上传
class UploadForm(FlaskForm):
    photo = FileField('Upload Image',validators=[FileRequired(),FileAllowed(['jpeg','jpg','png','gif'])])   # 不需要点
    submit = SubmitField()

# 博客内容编辑
class BlogForm(FlaskForm):
    # username = StringField('Username', render_kw={'placeholder': 'Please input the username'}, validators=[DataRequired(message=u'请输入用户名')])
    # 上面那个是为了测试
    title = StringField('标题', render_kw={'placeholder': 'Please input the title'}, validators=[DataRequired(message=u'请输入帖子名')])
    content = TextAreaField('内容', render_kw={'placeholder': 'Please input the content'}, validators=[DataRequired(message=u'请输入帖子内容')])
    photo = FileField('上传图片',validators=[FileRequired(),FileAllowed(['jpeg','jpg','png','gif'])])   # 不需要点
    publish = SubmitField('发布博客')

class DeleteForm(FlaskForm):
    title = StringField('删除帖子标题', render_kw={'placeholder': 'Please input the title'}, validators=[DataRequired(message=u'请输入要删除的帖子名')])
    delete = SubmitField('确定删除')

class Search_Form(FlaskForm):
    cname = StringField('课程名', render_kw={'placeholder': '课程名（精确搜索）'})
    key = StringField('关键字', render_kw={'placeholder': '关键字（模糊搜索）'})
    author = StringField('授课教师', render_kw={'placeholder': '授课教师'})
    search = SubmitField('搜索')