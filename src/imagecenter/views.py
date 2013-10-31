#-*- coding:utf-8 -*-

import math

from StringIO import StringIO

import tornado
from PIL import Image

from models import ImageDB
from setting import IMAGE_DB_SETTING
from setting import IMG_PRE

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
        x1 = self.get_arguments("x1")
        y1 = self.get_arguments('y1')
        x2 = self.get_arguments('x2')
        y2 = self.get_arguments('y2')
        im_width = self.get_arguments('p_width')
        im_height = self.get_arguments('p_height')
        if not x1:
            image_id = self.db.save(content, content_type, image_name)
        else:
            im = Image.open(StringIO(content))
            im_width = int(im_width[0])
            im_height = int(im_height[0])
            im = im.resize((im_width, im_height), Image.ANTIALIAS);
            size = (100, 100)
            x1, y1, x2, y2 = int(x1[0]), int(y1[0]), int(x2[0]), int(y2[0])
            new_im = im.crop((x1, y1, x2, y2));
            new_im = new_im.resize(size, Image.ANTIALIAS)
            out_put = StringIO()
            if 'jpeg' in content_type.lower():
                new_im.save(out_put, 'JPEG')
            else:
                new_im.save(out_put, 'PNG')
            image_id = self.db.save(out_put.getvalue(), content_type, image_name);

        self.set_status(200)
        data = str(image_id)
        rst = IMG_PRE + data
        self.finish(rst)
