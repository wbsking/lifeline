#-*- coding:utf-8 -*-

import json
from md5 import md5

import tornado
import models
from models import User, Token
from models import Profile
from utils import gen_token, platform_hash
from utils import date_to_datetime
from settings import MD5_LENGTH, TOKEN_EXPIRE_DAYS
from settings import LOGIN_URL
from settings import LOGOUT_URL
from settings import REGISTER_URL
from settings import PROFILE_URL

class baseHandler(tornado.web.RequestHandler):
    @property
    def session(self):
        return models.SESSION
    
    def get_current_user(self):
        token = self.get_secure_cookie('token')
        if not token:
            return None
        token = Token.get_by_uid(token=token)
        if not token:
            return None
        return token.uid

    def json_response(self, data='', status=200):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        data = json.dumps(data)
        self.set_status(status)
        self.finish(data)

class mainHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.redirect(LOGIN_URL)
        else:
            profile = Profile.get(uid=self.current_user)
            user_info = {"uid":profile.uid,
                        "gravatar":profile.gravatar,
                         "dot_num":0,
                         "friend_num":0}
            self.render('home.html', user_info=user_info)

class registerHandler(baseHandler):
    def get(self):
        return self.json_response({'message':'method not allowed'}, status=405)

    def post(self):
        try:
            data = json.loads(self.request.body)
        except Exception, ex:
            print ex
            return self.json_response(status=400)
        username = data.get('name', None)
        password = data.get('password', None)
        email = data.get('email', None)
        is_remember = data.get('is_remember', None)
        user = User.get(email=email)
        if user:
            return self.json_response({'message':'User existed!'}, status=200)
        if len(password) != MD5_LENGTH:
            return self.json_response({'message':'password length not correct'}, status=200)
        user_id = User.create(name=username, passwd=password, email=email)

        new_token = gen_token(user_id)
        Token.create(user_id, new_token)
        Profile.create(uid=user_id)
        if is_remember == '0':
            self.set_secure_cookie('token', new_token)
        else:
            self.set_secure_cookie('token', new_token,
                                   expires_days=TOKEN_EXPIRE_DAYS)
        
        return self.json_response({'code':1}, status=200)

class loginHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.render('login.html')
        else:
            self.redirect('/')

    @tornado.web.asynchronous
    def post(self):
        try:
            data = json.loads(self.request.body)
        except:
            return json_response(status=400)
        username = data.get('name', None)
        passwd = data.get('password', None)
        is_remember = data.get('is_remember', None)
        if not username or not passwd:
            return self.json_response({'message':'user name or password is empty'},
                               status=200)
        user = User.get(email=username)
        if not user:
            return self.json_response({'code':2, 'message':'cannot find the user'}, status=200)
        if passwd != user.passwd:
            return self.json_response({'code':2, 'message':'password is wrong'}, status=200)

        token = Token.get_by_uid(uid=user.uid)
        if not token:
            token = gen_token(user.uid)
            Token.create(uid=user.uid, token=token)
        else:
            token.update_expiretime()
            token = token.token
        if is_remember == '0':
            self.set_secure_cookie('token', token)
        else:
            self.set_secure_cookie('token', token,
                                   expires_days=TOKEN_EXPIRE_DAYS)
        return self.json_response({'code':1}, status=200)

class logoutHandler(baseHandler):
    def get(self):
        if self.current_user:
            self.set_secure_cookie('token', '')
            return self.redirect('/')
        else:
            return self.redirect('/')

    def post(self):
        pass

class modifyHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.redirect(LOGIN_URL)
        else:
            profile = Profile.get(uid=self.current_user)
            user = User.get(uid=self.current_user)
            user_info = {"user_name":user.name,
                         "dot_num":0,
                         "friend_num":0,
                         "gravatar":profile.gravatar,
                         "real_name":profile.real_name if profile.real_name else '',
                         "gender":profile.gender,
                         "birthday":profile.birthday}
            self.render('profile.html', user_info=user_info)

    def post(self):
        pass


class profileBaseHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.redirect(LOGIN_URL)
        else:
            self.render('profile_base.html')
    
    def post(self):
        if not self.current_user:
            self.redirect(LOGIN_URL)
        try:
            data = json.loads(self.request.body)
        except:
            self.json_response(status=400)
        print data
        gravatar = data.get('gravatar')
        gender = data.get('gender')
        username = data.get('username')
        realname = data.get('realname')
        birth_year = data.get('birth_year')
        birth_month = data.get('birth_month')
        birth_day = data.get('birth_day')
        birthday = date_to_datetime(birth_year, birth_month, birth_day)
        profile = Profile.get(uid=self.current_user)
        user = User.get(uid=self.current_user)
        if not user:
            return self.json_response({"code":1, "message":"permission denied"})
        else:
            user.update(name=username)
        if not profile:
            Profile.create(uid=self.current_user,
                           gravatar=gravatar,
                           birthday=birthday,
                           username=username,
                           gender=gender,
                           real_name=realname)
        else:
            profile.update(gravatar=gravatar,
                           birthday=birthday,
                           gender=gender,
                           username=username,
                           real_name=realname)
            return self.json_response({"code":0, 'message':'save success'},
                                      status=200)

class profilePasswdHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.redirect(LOGIN_URL)
        else:
            self.render('profile_passwd.html')
    
    def post(self):
        if not self.current_user:
            self.redirect(LOGIN_URL)
        try:
            data = json.loads(self.request.body)
        except:
            self.json_response(status=400)
        old_passwd = data.get('old_passwd')
        new_passwd = data.get('new_passwd')
        if not old_passwd or not new_passwd:
            return self.json_response({"code":1, 'message':'password empty'},
                                 status=200)
        user = User.get(uid=self.current_user)
        if user.passwd != old_passwd:
            return self.json_response({"code":2, 'message':'password error'},
                                 status=200)
        if len(new_passwd) != MD5_LENGTH:
            return self.json_response({"code":3, 'message':'unknown new password'},
                                 status=200)
        user.update(passwd=new_passwd)
        return self.json_response({'code':0, 'message':'save success'},
                             status=200)

