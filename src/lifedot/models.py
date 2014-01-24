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
from sqlalchemy.types import UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound


CONN_STR = "mysql://root:lifeline@localhost/lifedot?charset=utf8"
engine = create_engine(CONN_STR, echo=True)
session_obj = sessionmaker(bind=engine)
SESSION = session_obj()

baseModel = declarative_base()

def init_db():
    baseModel.metadata.create_all(engine)

def drop_db():
    baseModel.metadata.drop_all(engine)

class LifeDot(baseModel):
    __tablename__ = 'lifedot'
    __table_args__ = {"mysql_engine":'InnoDB', "mysql_charset":'utf8'}

    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger)
    privacy = Column(SmallInteger, default=0)
    images = Column(VARCHAR(length=4096L), default='')
    content = Column(UnicodeText, default='')
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, onupdate=datetime.utcnow)
    publish_time = Column(DateTime)
    deleted = Colum(Boolean, default=False)

    def __init__(self, uid, content, **kwargs):
        self.uid = uid
        self.content = content

    @staticmethod
    def create(uid, content, **kwargs):
        dot = LifeDot(uid, content, **kwargs)
        SESSION.add(dot)
        SESSION.commit()

if __name__ == "__main__":
    init_db()
