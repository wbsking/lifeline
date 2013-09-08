from views import *

UCENTER_HANDLERS = [('/', mainHandler),
                    ('/login', loginHandler),
                    ('/register', registerHandler),
                    ('/logout', logoutHandler),
                    ('/modify', modifyHandler)]
