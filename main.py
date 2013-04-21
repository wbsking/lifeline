import os
import tornado.ioloop
import tornado.web

settings = {"static_path":os.path.join(os.path.dirname(__file__), 'static'),
            "template_path":os.path.join(os.path.dirname(__file__), 'templates')
            }

class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

app = tornado.web.Application([
                               (r'/', loginHandler)
                               ], **settings)

if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()