#! /usr/bin/env python
#-*- coding:utf-8 -*-
import random
import time
import md5
from datetime import datetime, timedelta

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def gen_token(user_id):
    md5_id = md5.md5(str(user_id)).hexdigest()
    md5_time = md5.md5(str(time.time())).hexdigest()
    return md5.md5(md5_id+md5_time).hexdigest()

def get_now():
    return datetime.now()

def get_delay_time(curr_time, delay_days):
    return curr_time + timedelta(delay_days)

def datetime_to_str(time):
    return datetime.strftime(now, TIME_FORMAT)
