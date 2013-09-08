import tornado
import json
from md5 import md5

from models import User, Token
from utils import gen_token, platform_hash
from settings import MD5_LENGTH, TOKEN_EXPIRE_DAYS

class baseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.ucenter_db
    
    def get_current_user(self):
        token = self.get_secure_cookie('token')
        if not token:
            return None
        return User(self.db).get_by_token(token)

    def json_response(self, data='', status=200):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        data = json.dumps(data)
        self.set_status(status)
        self.finish(data)

class mainHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/login')
        else:
            self.render('userhome.html')

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
        platform = data.get('platform', None)
        is_remember = data.get('is_remember', None)
        user = User(self.db).get_by_name_or_mail(email)
        if user:
            return self.json_response({'message':'User existed!'}, status=200)
        if len(password) != MD5_LENGTH:
            return self.json_response({'message':'password length not correct'}, status=200)
        user_id = User(self.db).create(username, password, email)
        new_token = gen_token(user_id)
        Token(self.db).create(user_id, new_token, platform_hash.get(platform, 0)) 
        if is_remember == '0':
            self.set_secure_cookie('token', new_token)
        else:
            self.set_secure_cookie('token', new_token,
                                   expires_days=TOKEN_EXPIRE_DAYS)
        
        return self.render('userhome.html')

class loginHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.render('login.html')
        else:
            #TODO
            self.render('userhome.html')

    @tornado.web.asynchronous
    def post(self):
        try:
            data = json.loads(self.request.body)
        except:
            return json_response(status=400)
        username = data.get('name', None)
        passwd = data.get('password', None)
        platform = data.get('platform', None)
        is_remember = data.get('is_remember', None)
        if not username or not passwd:
            return self.json_response({'message':'user name or password is empty'},
                               status=200)
        user = User(self.db).get_by_name_or_mail(username)
        if not user:
            return self.json_response({'code':2, 'message':'cannot find the user'}, status=200)
        if passwd != user.get('password'):
            return self.json_response({'code':2, 'message':'password is wrong'}, status=200)

        platform = platform_hash.get(platform)
        token = Token(self.db).get_by_user(user.get('id', 0), platform)
        if not token:
            token = gen_token(user.get('id'))
            Token(self.db).save(user.get('id'), token, platform)
        else:
            token = token.get('token')
        if is_remember == '0':
            self.set_secure_cookie('token', token)
        else:
            self.set_secure_cookie('token', token,
                                   expires_days=TOKEN_EXPIRE_DAYS)
        return self.render('userhome.html')

class logoutHandler(baseHandler):
    def get(self):
        pass

    def post(self):
        pass

class modifyHandler(baseHandler):
    def get(self):
        pass

    def post(self):
        pass
