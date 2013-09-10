#-*- coding:utf-8 -*-

import pymongo
import gridfs
from PIL import Image
from bson.objectid import ObjectId
import StringIO

class ImageDB(object):
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.db = self.connect()
    
    def connect(self):
        conn = pymongo.Connection(host=self.host, port=self.port)
        fs = gridfs.GridFS(conn[self.name])
        return fs

    def get(self, image_id):
        gf = self.db.get(ObjectId(image_id))
        im = gf.read()
        content_type = gf.content_type
        file_name = gf.file_name
        return im, content_type, file_name

    def save(self, content, content_type, image_name):
        return self.db.put(content, content_type=content_type, file_name=image_name)

if __name__ == '__main__':
    im = ImageDB('localhost', 27017, 'images')
    print im.get('522ddb9e79ed330ff139a0cb')
