#-*- coding:utf-8 -*-

import json

import tornado

from src.usercenter.models import Token

class baseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        token = self.get_secure_cookie('token')
        if not token:
            return None
        token = Token.get_by_uid(token=token)
        if not token:
            return None
        return token.uid

    def json_response(self, data='', status=200):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        data = json.dumps(data)
        self.set_status(status)
        self.finish(data)