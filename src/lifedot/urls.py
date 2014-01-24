# -*- coding:utf-8 -*-

import views

from settings import CREATE_DOT_URL
from settings import GET_NEW_DOTS_URL

    
URL_HANDLER = [(
		CREATE_DOT_URL, views.createDotHandler)
	),]