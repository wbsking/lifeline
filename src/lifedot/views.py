#-*- coding:utf-8 -*-

import json
import tornado

from src.lib.handler import baseHandler
from src.usercenter.settings import LOGIN_URL
from models import LifeDot
from src.lib.datetime_utils import datetime_to_str

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
            dot = LifeDot.create(uid=self.current_user, content=content)
            self.json_response({'msg':'ok', "code":0, "id":dot.id,
                                "create_time":datetime_to_str(dot.create_time)},
                               status=201)
        else:
            self.json_response({"msg":"content empty", "code":1}, status=201)
