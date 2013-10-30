#! /usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import BigInteger
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import Boolean
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from utils import gen_uid

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
        kwargs['deleted']  = False
        try:
            query = SESSION.query(User).filter_by(**kwargs).one()
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

class Token(baseModel):
    __tablename__ = 'token'
    __table_args__ = {"mysql_engine":'InnoDB', "mysql_charset":'utf8'}
    
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger)
    token = Column(VARCHAR(64))
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    
    @staticmethod
    def get_uid(**kwargs):
        kwargs['deleted'] = False
        try:
            query = SESSION.query(Token).filter_by(**kwargs).one()
            return query.uid
        except NoResultFound:
            return None

class Profile(baseModel):
    __tablename__ = 'profile'
    __table_args__ = {"mysql_engine":'InnoDB', "mysql_charset":'utf8'}
    
    id = Column(BigInteger, primary_key=True)

if __name__ == '__main__':
    init_db()
