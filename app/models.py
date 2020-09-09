# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 15:34
# @Author  : WANGXIAO

# 会员模型

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:123456@localhost:3306/d_movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 会员id  主键
    name = db.Column(db.String(100), unique=True)  # 会员名 唯一值
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(100), unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255))  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 日期
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识

    # 增加外键,会员与会员日志建立关系
    userlogs = db.relationship('UserLog', backref='user')
    comments = db.relationship('Comment', backref='user')
    moviecols = db.relationship('MovieCol', backref='user')

    def __repr__(self):
        return "<User %r>" % self.name


# 会晕登录日志
class UserLog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录日期

    def __repr__(self):
        return "<UserLog %r>" % self.user_id


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标签名 唯一值
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录日期
    # 增加movie外键
    movies = db.relationship('Movie', backref='movie')

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 电影标题
    url = db.Column(db.String(255), unique=True)  # 电影地址
    info = db.Column(db.Text)  # 电影简介
    logo = db.Column(db.String(255), unique=True)  # 电影标题
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论数
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属tagid
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.DateTime)  # 上映时间
    length = db.Column(db.String(255))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加日期

    # 添加外键
    comments = db.relationship('Comment', backref='movie')
    moviecol = db.relationship('MovieCol', backref='movie')

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 电影标题
    logo = db.Column(db.String(255), unique=True)  # 电影标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加日期

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 外键链接movie.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外键user.id
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加日期

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class MovieCol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 外键链接movie.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外键user.id
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加日期

    def __repr__(self):
        return "<MovieCol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255), unique=True)  # 用户
    url = db.Column(db.String(255), unique=True)  # url
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加日期

    def __repr__(self):
        return "<Auth %r>" % self.id


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255), unique=True)  # 角色名
    auths = db.Column(db.String(255))  # 权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加日期

    # 添加外键
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(255), unique=True)  # 管理员
    pwd = db.Column(db.String(255))
    is_super = db.Column(db.SmallInteger)  # 是否继承
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 外键role.id
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加日期

    # 添加外键
    adminlogs = db.relationship('AdminLog', backref='admin')
    operatelogs = db.relationship('OperateLog', backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name


# 管理员日志
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录日期

    def __repr__(self):
        return "<AdminLog %r>" % self.admin_id


# 操作日志
class OperateLog(db.Model):
    __tablename__ = 'operatelog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录ip
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录日期

    def __repr__(self):
        return "<OperateLog %r>" % self.id


if __name__ == '__main__':
    # db.create_all()
    role = Role(
        name="超级管理员",
        auths=""
    )
    db.session.add(role)
    db.session.commit()

    from werkzeug.security import generate_password_hash

    admin = Admin(
        name="wangxiao",
        pwd=generate_password_hash('wangxiao'),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
