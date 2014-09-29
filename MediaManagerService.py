#!/usr/bin/python

import traceback
import uuid
from datetime import datetime
import logging as log
from couchdb import Server
import tornado.ioloop
import tornado.web
from tornado.escape import json_decode
from tornado.escape import json_encode

log.basicConfig(filename='mms.log',level=log.DEBUG)
couch = Server()

if "users" not in couch:
    couch.create("users")
db = couch['users']

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class SignInHandler(tornado.web.RequestHandler):
    js = None
    def post(self):
        jstr = self.request.body
        self.signin(jstr)

    def get(self):
        jstr = self.get_argument("js")
        self.signin(jstr)

    def signin(self, jstr):
        js = json_decode(jstr)
        if js is None:
            self.write(json_encode({"signin":{
                "response": "false",
                "status": "empty json"
            }}))
        try:
            if "signin" in js:
                if "email" in js["signin"] and "password" in js["signin"]:
                    email = js["signin"]["email"]
                    password = js["signin"]["password"]
                    if email in db:
                        if password == db[email].get("password", None):
                            user = db[email]
                            session_id = str(uuid.uuid4())
                            tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            user["session_id"] = session_id
                            user["last_login"] = tstamp
                            log.debug('USER:' + user.id)
                            db[user.id] = user
                            self.write(json_encode({"signin":{
                                "response": "true",
                                "status": "success",
                                "session_id": session_id,
                                "last_login": tstamp
                            }}))
                        else:
                            self.write(json_encode({"signin":{
                                "response": "false",
                                "status": "bad user or password",
                            }}))
                    else:
                        self.write(json_encode({"signin":{
                            "response": "false",
                            "status": "bad user or password"
                        }}))
            else:
                self.write(json_encode({"signin":{
                     "response": "false",
                     "status": "bad method"
                }}))
        except Exception:
            self.write(json_encode({"signin":{
                "response": "false",
                "status": "internal error",
                "traceback": traceback.format_exc()
            }}))


class SignUpHandler(tornado.web.RequestHandler):
    js = None
    def post(self):
        jstr = self.request.body
        self.signup(jstr)

    def get(self):
        jstr = self.get_argument("js")
        self.signup(jstr)

    def signup(self, jstr):
        js = json_decode(jstr)
        if js is None:
            self.write(json_encode({"signup":{
                "response": "false", 
                "status": "empty json"
            }})) 
        try:
            if "signup" in js:
                if "email" in js["signup"] and "password" in js["signup"]:
                    email = js["signup"]["email"]
                    password = js["signup"]["password"]
                    if js["signup"]["email"] in db:
                        self.write(json_encode({"signup":{
                            "response": "false",
                            "status": "user exists"
                        }})) 
                    else:
                        db[email] = {
                            "email": email,
                            "password": password
                        }
                        self.write(json_encode({"signup":{
                            "response": "true",
                            "status": "success"
                        }}))
            else:
                self.write(json_encode({"signup":{
                     "response": "false",
                     "status": "bad method"
                }}))
        except Exception:
            self.write(json_encode({"signup":{
                "response": "false",
                "status": "internal error",
                "traceback": traceback.format_exc()
            }}))
                

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/signin/", SignInHandler),
    (r"/signup/", SignUpHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
