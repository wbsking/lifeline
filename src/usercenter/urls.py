from views import *
from settings import LOGIN_URL
from settings import LOGOUT_URL
from settings import REGISTER_URL
from settings import PROFILE_URL

UCENTER_HANDLERS = [('/', mainHandler),
                    (LOGIN_URL, loginHandler),
                    (REGISTER_URL, registerHandler),
                    (LOGOUT_URL, logoutHandler),
                    (PROFILE_URL, modifyHandler)]
