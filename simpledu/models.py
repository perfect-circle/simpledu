from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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
class User(Base):
    __tablename__ = 'user'

    # 用数值表示角色,方便判断是否
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    publish_courses = db.relationship('Course')

# 改为继承Base类
class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author= db.relationship('User', uselist=False)
