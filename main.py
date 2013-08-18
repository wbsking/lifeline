import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import torndb

from tornado.options import define, options

from src.usercenter.settings import UCENTER_HANDLERS, UCENTER_DB

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [] + UCENTER_HANDLERS
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
            login_url = '/login'
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.ucenter_db = torndb.Connection(
            host=UCENTER_DB['host'], database=UCENTER_DB['database'],
            user=UCENTER_DB['user'], password=UCENTER_DB['passwd'])

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == '__main__':
    main()
