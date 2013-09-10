#! /usr/bin/env python
#-*- coding:utf-8 -*-

from utils import datetime_to_str, get_now, get_delay_time
from settings import TOKEN_EXPIRE_DAYS
from settings import DEFAULT_SMALL_GRAVATAR

class User(object):
    TB_NAME = 'user'
    def __init__(self, db):
        self.db = db
    
    def get_by_id(self, user_id):
        return self.db.get('SELECT * from %s WHERE id = %s and deleted =\
                           1' % (self.TB_NAME, int(user_id)))

    def get_by_name_or_mail(self, username):
        user = self.db.get('SELECT * from %s WHERE name = "%s" or email = "%s"\
                           and deleted = 0' %(self.TB_NAME, username, username))
        return user

    def get_by_token(self, token):
        token_coll = Token(self.db).get_by_token(token)
        if not token_coll:
            return None
        return token_coll.get('user_id', None)
    
    def create(self, username, password, email):
        now = get_now()
        return self.db.execute_lastrowid('INSERT INTO %s (name, email, password,\
                                         createtime) values("%s", "%s", "%s", "%s");'\
                                         % (self.TB_NAME,
                                            username, email, password, 
                                            datetime_to_str(now)))

class Profile(object):
    TB_NAME = 'profile'

    def __init__(self, db):
        self.db = db

    def get_by_userid(self, user_id):
        return self.db.get('SELECT * from %s WHERE user_id = %s and deleted = 0;'\
                           % (self.TB_NAME, int(user_id)))

    def create(self, user_id):
        profile = self.get_by_userid(user_id)
        if profile:
            raise Exception('user profile exist')

        self.db.execute('INSERT INTO %s SET user_id=%s,\
                        gravatar_small="%s", createtime="%s"' % (
                        self.TB_NAME, user_id, DEFAULT_SMALL_GRAVATAR,
                        get_now()
                    ))
    
    def modify(self, **kwargs):
        pass

class Token(object):
    TB_NAME = 'token'

    EXPIRE_TIME = TOKEN_EXPIRE_DAYS

    def __init__(self, db):
        self.db = db

    def get_by_token(self, token, platform=0):
        return self.db.get('SELECT * from %s WHERE token = "%s" and platform = %s\
                           and deleted = 0;' % (self.TB_NAME, token, platform))

    def get_by_user(self, user_id, platform=0):
        token = self.db.get('SELECT * from %s WHERE user_id=%s and platform=%s\
                           and deleted=0' % (self.TB_NAME, int(user_id),
                                                    int(platform)))
        if token:
            expire_time = token.get('expiretime')
            token_id = token.get('id')
            now = get_now()
            if now >= expire_time:
                self.db.execute('UPDATE %s SET deleted=1 where id=%s' %
                                (self.TB_NAME,
                                 int(token_id)))
                return None
            else:
                expire_time = get_delay_time(now, self.EXPIRE_TIME)
                self.db.execute('UPDATE %s SET expiretime="%s" where id=%s;' %(self.TB_NAME,
                                                datetime_to_str(expire_time),
                                                int(token_id)))
                return token
        else:
            return None

    def create(self, user_id, token, platform=0):
        now = get_now()
        expire_time = get_delay_time(now, self.EXPIRE_TIME)

        return self.db.execute_lastrowid('INSERT INTO %s (token, createtime, \
                        user_id, platform, expiretime)\
                                        values("%s", "%s", %s, %s, "%s");' %(
                                                                    self.TB_NAME,
                                                                    token, 
                                                                     datetime_to_str(now),
                                                                     user_id,
                                                                     platform,
                                                                     datetime_to_str(expire_time)
                                                                     ))
    
    def update(self, token_id, token):
        self.db.execute('UPDATE %s SET token="%s" WHERE id=%s;' %(self.TB_NAME,
                                                                  token,
                                                                  token_id
                                                                  ))
        

    def save(self, user_id, token, platform):
        token_obj = self.get_by_user(user_id, platform)
        if not token_obj: 
            self.create(user_id, token, platform)
        else:
            self.update(token_obj.get('id'), token)
