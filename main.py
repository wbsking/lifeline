import os
import tornado.ioloop
import tornado.web
import torndb

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="lifeline")
define("mysql_database", default="lifeline", help="")
define("mysql_user", default="lifeline", help="")
define("mysql_password", default="lifeline", help="")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", mainHandler),
            (r"/login", loginHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

class baseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))
    
class mainHandler(baseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        else:
            self.write("hello")
        
class loginHandler(baseHandler):
    def get(self):
        self.render("login.html")
    
    def post(self):
        username = self.get_argument('user')
        passwd = self.get_argument('password')
        sessionid = self.get_argument('sessionid')

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == '__main__':
    main()
