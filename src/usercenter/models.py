#! /usr/bin/env python
#-*- coding:utf-8 -*-

from utils import datetime_to_str, get_now, get_delay_time

class User():
    TB_NAME = 'user'
    def __init__(self, db):
        self.db = db
    
    def get_by_id(self, user_id):
        return self.db.get('SELECT * from %s WHERE id = %s and is_not_deleted =\
                           1' % (self.TB_NAME, int(user_id)))

    def get_by_username(self, username):
        user = self.db.get('SELECT * from %s WHERE name = "%s" or email = "%s"\
                           and is_not_deleted = 1' %(self.TB_NAME, username, username))
        return user

    def get_by_token(self, token, platform):
        token_coll = Token(self.db).get_by_token(token, platform)
        return token_coll.get('user_id', None)

class Profile():
    TB_NAME = 'profile'

    def __init__(self, db):
        self.db = db

    def get_by_userid(self, user_id):
        return self.db.get('SELECT * from %s WHERE user_id = %s;' % (self.TB_NAME,
                                                                   int(user_id)))

class Token():
    TB_NAME = 'token'

    #default expire time 14 days
    EXPIRE_TIME = 14

    def __init__(self, db):
        self.db = db

    def get_by_token(self, token, platform=0):
        return self.db.get('SELECT * from %s WHERE token = "%s" and platform = "%s"\
                           is_not_deleted = 1;' % (self.TB_NAME, token, platform))

    def create(self, user_id, token, platform=0):
        now = get_now()
        expire_time = get_delay_time(now, self.EXPIRE_TIME)

        self.db.execute('INSERT INTO %s (token, createtime, user_id, platform, \
                        expiretime) values(%s, "%s", %s, %s, %s)' % (token, 
                                                                     datetime_to_str(now),
                                                                     user_id,
                                                                     platform,
                                                                     datetime_to_str(expire_time)
                                                                     ))
    
    def update(token_id, user_id, token, platform):
        pass

    def save(self, user_id, token, platform):
        token = self.get_by_token(token, platform)
        if not token: 
            self.create(user_id, token, platform)
        else:
            self.update(token.get('id'), user_id, platform)

