#! /usr/bin/env python
#-*- coding:utf-8 -*-

import random
import time
import hashlib
from datetime import datetime, timedelta

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

platform_hash = {'web':0, 'ios':1, 'android':2}

def gen_random_str(length=10):
    key_list = [chr(i) for i in range(48, 123)]
    random.shuffle(key_list)
    random.shuffle(key_list)
    return ''.join(key_list)[:length]

def gen_token(user_id):
    md5_id = hashlib.md5(gen_random_str(5)+str(user_id)).hexdigest()
    md5_time = hashlib.md5(str(time.time())).hexdigest()
    return hashlib.md5(md5_time).hexdigest() + hashlib.md5(md5_id).hexdigest()

def get_now():
    return datetime.utcnow()

def get_delay_time(curr_time, delay_days):
    return curr_time + timedelta(delay_days)

def datetime_to_str(time):
    return time.strftime(TIME_FORMAT)

def gen_uid(uid):
    uid = str(uid)
    time_str = time.time().__repr__().replace('.', '')[-5:]
    return int(uid+time_str)
