import tornado
import json
from md5 import md5

from models import User
from utils import gen_token

class baseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.ucenter_db
    
    def get_current_user(self):
        token = self.get_secure_cookie('token')
        if not token:
            return None
        return User.get_by_token(token)

    def json_response(self, data, status=200):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        data = json.dumps(data)
        self.set_status(status)
        self.finish(data)

class mainHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/login')
        else:
            self.redirect('/%s' % self.current_user.id)

class loginHandler(baseHandler):
    def get(self):
        self.render('login.html')

    @tornado.web.asynchronous
    def post(self):
        username = self.get_argument('name', None)
        passwd = self.get_argument('passwd', None)
        platform = self.get_argument('platform', None)
        is_remember = self.get_argument('is_remember', None)
        if not username or not passwd:
            self.json_response({'message':'user name or password is empty'},
                               status=400)
        user = User(self.db).get_by_username(username)
        if not user:
            self.json_response({'message':'cannot find the user'}, status=404)
        passwd = md5(passwd).hexdigest()
        if passwd != user.get('password'):
            self.json_response({'message':'password is wrong'}, status=403)
        new_token = gen_token(user.get('id'))
        Token(self.db).save(user.get('id'), new_token, platform)
        if not is_remember:
            self.set_secure_cookie('token', new_token)
        else:
            self.set_secure_cookie('token', new_token, expires_days=14)
        
        self.write('login success')
        self.finish()

class logoutHandler(baseHandler):
    def post(self):
        pass

