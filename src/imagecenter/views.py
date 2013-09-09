#-*- coding:utf-8 -*-

import tornado

from models import ImageDB
from setting import IMAGE_DB_SETTING

class baseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return ImageDB(host=IMAGE_DB_SETTING['host'],
                          port=IMAGE_DB_SETTING['port'],
                          name=IMAGE_DB_SETTING['name'])

class imageHandler(baseHandler):
    def get(self, image_id):
        content = self.db.get(image_id)
        self.set_header('Content-Type', 'image/png;charset=utf-8')
        self.write(content)
