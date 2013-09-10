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
        content, content_type, file_name = self.db.get(image_id)
        self.set_header('Content-Type', '%s;charset=utf-8' % (content_type))
        self.write(content)

class imageUploadHandler(baseHandler):
    def post(self):
        image = self.request.files['image'][0]
        content = image.get('body', '')
        content_type = image.get('content_type', '')
        image_name = image.get('filename', '')
        image_id = self.db.save(content, content_type, image_name)
        self.set_status(200)
        data = str(image_id)
        self.finish(data)
