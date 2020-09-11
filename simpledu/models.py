from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, \
        check_password_hash

# 注意这里不再传入 app 了
db = SQLAlchemy()

class Base(db.Model):
    #  所有的 model 的一个基类，默认添加类时间戳
    __abstract__ = True
    # 设置了defaul和onupdate这俩个时间戳都不需要我们去维护
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow)

# 改为继承Base类
class User(Base, UserMixin):
    __tablename__ = 'user'

    # 用数值表示角色,方便判断是否有权限，比如有一个操作需要角色为员工
    # 级以上的用户才可以做，那么只要判断user.role >= ROLE_STAFF
    # 就可以的，数值之间设置了10为间隔是为了防止方便以后加入其他角色
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    # 默认情况下，sqlalchemy会以字段名来定义列名，但这里是_password,所以明确指定数据库列名为ppassword
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    job = db.Column(db.String(64))
    publish_courses = db.relationship('Course')

    def __repr__(self):
        return "<User:{}>".format(self.username)

    @property
    def password(self):
        """Python风格的getter"""
        return self._password

    @password.setter
    def password(self,orig_password):
        """ Python风格的setter,这样设置user.password就会
        自动为password生成哈希值_password字段"""
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """判断用户输入的密码和存储的哈希值是否相等"""
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

# 改为继承Base类
class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author= db.relationship('User', uselist=False)
