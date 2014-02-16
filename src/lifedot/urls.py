# -*- coding:utf-8 -*-

import views

from settings import CREATE_DOT_URL
from settings import GET_NEW_DOTS_URL


DOT_HANDLER = [(
    CREATE_DOT_URL, views.createDotHandler)
]
