#!/usr/bin/python

import logging as log
import tornado.ioloop
import tornado.web
from WebService import WebService

log.basicConfig(filename='mms2.log',level=log.DEBUG)

handler_urls = WebService.loadHandlers('.')

application = tornado.web.Application(handler_urls)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
