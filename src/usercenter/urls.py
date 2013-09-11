from views import *

UCENTER_HANDLERS = [('/', mainHandler),
                    ('/user/login', loginHandler),
                    ('/user/register', registerHandler),
                    ('/user/logout', logoutHandler),
                    ('/user/modify', modifyHandler)]
