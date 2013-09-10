#-*- coding:utf-8 -*-

from views import *

IMAGE_HANDLERS = [
        ('/image/upload', imageUploadHandler),
        ('/image/(.*)', imageHandler)]
