#-*- coding:utf-8 -*-

import json
import tornado

from src.lib.handler import baseHandler
from src.usercenter.settings import LOGIN_URL
from models import LifeDot

class createDotHandler(baseHandler):

    def post(self):
        if not self.current_user:
            self.redirect(LOGIN_URL)
        try:
            data = json.loads(self.request.body)
        except Exception, ex:
            print ex
            return self.json_response(status=400)
        content = data.get('content')
        if content:
            LifeDot.create(uid=self.current_user, content=content)
        else:
            pass
