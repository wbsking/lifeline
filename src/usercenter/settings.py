#-*- coding:utf-8 -*-

TOKEN_EXPIRE_DAYS = 14
MD5_LENGTH = 32

DEFAULT_SMALL_GRAVATAR = '522f2c8179ed330e6473bc5f'

UCENTER_DB = {'host':'127.0.0.1:3306',
              'database':'usercenter',
              'user':'root',
              'passwd':'lifeline'
            }

LOGIN_URL = '/user/login'
REGISTER_URL = '/user/register'
LOGOUT_URL = '/user/logout'
PROFILE_URL = '/user/profile'
