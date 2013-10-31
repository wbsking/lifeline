#! /usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime
from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import BigInteger
from sqlalchemy.types import SmallInteger
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import Boolean
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from utils import gen_uid
from settings import TOKEN_EXPIRE_DAYS

CONN_STR = "mysql://root:lifeline@localhost/usercenter?charset=utf8"
engine = create_engine(CONN_STR, echo=True)
session_obj = sessionmaker(bind=engine)
SESSION = session_obj()

baseModel = declarative_base()

def init_db():
    baseModel.metadata.create_all(engine)

def drop_db():
    baseModel.metadata.drop_all(engine)

class User(baseModel):
    __tablename__ = 'user'
    __table_args__ = {"mysql_engine":'InnoDB', "mysql_charset":'utf8'}

    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger)
    name = Column(VARCHAR(32))
    email = Column(VARCHAR(320))
    passwd = Column(VARCHAR(64))
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False)

    def __init__(self, name, email, passwd):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.uid = 0

    def __repr__(self):
        return u"<User('%s')>" % self.name

    def update_uid(self):
        self.uid = gen_uid(self.id)

    @staticmethod
    def get(**kwargs):
        kwargs['deleted']  = 0
        try:
            return SESSION.query(User).filter_by(email="wbsking@gmail.com").one()
        except NoResultFound:
            return None

    @staticmethod
    def create(**kwargs):
        user = User(**kwargs)
        SESSION.add(user)
        SESSION.flush()
        SESSION.refresh(user)
        user.update_uid()
        SESSION.commit()
        return user.uid

class Token(baseModel):
    __tablename__ = 'token'
    __table_args__ = {"mysql_engine":'InnoDB', "mysql_charset":'utf8'}
    
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger)
    token = Column(VARCHAR(64))
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, onupdate=datetime.utcnow)
    expire_time = Column(DateTime)
    deleted = Column(Boolean, default=False)
    
    def __init__(self, uid, token, expire_time):
        self.uid = uid
        self.token = token
        self.expire_time = expire_time

    @staticmethod
    def get_by_uid(**kwargs):
        kwargs['deleted'] = False
        try:
            query = SESSION.query(Token).filter_by(**kwargs).one()
            if query.expire_time <= datetime.utcnow():
                query.deleted = True
                SESSION.commit()
                return None
            return query
        except NoResultFound:
            return None

    @staticmethod
    def create(uid, token):
        expire_time = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
        token = Token(uid, token, expire_time)
        SESSION.add(token)
        SESSION.commit()

class Profile(baseModel):
    __tablename__ = 'profile'
    __table_args__ = {"mysql_engine":'InnoDB', "mysql_charset":'utf8'}
    
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger)
    gravatar = Column(VARCHAR(64))
    birthday = Column(DateTime)
    real_name = Column(VARCHAR(32))
    nickname = Column(VARCHAR(32))
    gender = Column(SmallInteger)
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False)

    def __init__(self, **kwargs):
        if 'uid' in kwargs: self.uid = kwargs.get('uid')
        if 'gravatar' in kwargs: self.gravatar = kwargs.get('gravatar')
        if  'birthday' in kwargs: self.birthday = kwargs.get('birthday')
        if 'real_name' in kwargs: self.real_name = kwargs.get('real_name')
        if 'nickname' in kwargs: self.nickname = kwargs.get('nickname')
        if 'gender' in kwargs: self.gender = kwargs.get('gender')
    
    @staticmethod
    def create(**kwargs):
        profile = Profile(**kwargs)
        SESSION.add(profile)
        SESSION.commit()

    @staticmethod
    def get(**kwargs):
        kwargs['deleted'] = 0
        try:
            query = SESSION.query(Profile).filter_by(**kwargs).one()
            return query
        except NoResultFound:
            return None

if __name__ == '__main__':
    init_db()
