#-*- coding:utf-8 -*-

from datetime import datetime


def datetime_to_str(datetime_obj):
    return datetime.strftime(datetime_obj, "%Y-%m-%dT%H:%M:%SZ")
