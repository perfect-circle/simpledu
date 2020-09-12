from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms import ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired
from simpledu.models import db, User

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(),
        Length(3,24,message="字符要在3～24个")])
    email = StringField("邮箱",validators=[DataRequired(), Email
        ("请输入合法的email地址")])
    password = PasswordField('密码',validators=[DataRequired(),
        Length(6,24,message="密码位数在6～24")])
    repeat_password = PasswordField('重复密码',validators=
            [DataRequired(),EqualTo('password')])
    submit = SubmitField("提交")

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if not field.data.isalnum():
            raise ValidationError("用户名只能用数字和字母组合")
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已经存在")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已经存在")

class LoginForm(FlaskForm):
    username = StringField("用户名",validators=[DataRequired(),
        Length(3,24)])
    password = PasswordField("密码", validators=[DataRequired(),
        Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField("提交")

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名未注册")

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
                raise ValidationError("密码错误")
