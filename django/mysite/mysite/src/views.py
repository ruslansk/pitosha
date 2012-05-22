# -*- coding: utf-8 -*-
from django.http import HttpResponse
import datetime

#byteString = "����������, ���!"
#unicodeString = u"����������, ���!"

def hello(request):
    import logging
    logging.debug("A log message")
    return HttpResponse("Здравствуй, Мир!")
#    return HttpResponse("Hello, World!")
#    return HttpResponse(unicodeString.encode( "utf-8" ))
#    return HttpResponse(unicodeString)

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def my_homepage_view(request):
    return HttpResponse("<B>It's working!!!</B>")
