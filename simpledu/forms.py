from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired
from simpledu.models import db, User

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(),Length(3,24)])
    email = StringField("邮箱",validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired(),
        Length(6,24)])
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

class LoginForm(FlaskForm):
    email = StringField("邮箱",validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired(),
        Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField("提交")
