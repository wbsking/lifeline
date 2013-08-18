from views import mainHandler, loginHandler, logoutHandler

UCENTER_DB = {'host':'127.0.0.1:3306',
              'database':'usercenter',
              'user':'root',
              'passwd':'wangbo'
              }
UCENTER_HANDLERS = [('/', mainHandler),
                    ('/login', loginHandler),
                    ('/logout', logoutHandler)
                    ]


