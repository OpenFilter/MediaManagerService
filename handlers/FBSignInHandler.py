import traceback
import uuid
from datetime import datetime
import logging as log
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class FBSignInHandler(RequestHandler):

    db_users = None

    def initialize(self):
        couch = Server()
        if "users" not in couch:
            couch.create("users")
        self.db_users = couch['users']

    @staticmethod
    def url():
        return r'/fb_signin'

    def post(self):
        jstr = self.request.body
        self.fb_signin(jstr)

    def get(self):
        jstr = self.get_argument("js")
        self.fb_signin(jstr)

    def fb_signin(self, jstr):
        js = json_decode(jstr)
        if js is None:
            self.write(json_encode({"fb_signin":{
                "response": "false",
                "status": "empty json"
            }}))
        try:
            if "fb_signin" in js:
                if "fb_email" in js["fb_signin"] and "fb_id" in js["fb_signin"]:
                    user = {}
                    email = js["fb_signin"]["fb_email"]
                    if email in self.db_users:
                        user = self.db_users[email]
                    session_id = str(uuid.uuid4())
                    tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user["session_id"] = session_id
                    user["last_login"] = tstamp
                    user["fb_signin"] = js["fb_signin"]
                    self.db_users[email] = user
                    self.write(json_encode({"fb_signin":{
                        "response": "true",
                        "status": "success",
                        "session_id": session_id,
                        "last_login": tstamp,
                        "user_id": email,
                    }}))
                else:
                    self.write(json_encode({"fb_signin":{ 
                        "response": "false",
                        "status": "no fb id"
                    }})) 
            else:
                self.write(json_encode({"fb_signin":{
                     "response": "false",
                     "status": "bad method"
                }}))
        except Exception:
            self.write(json_encode({"fb_signin":{
                "response": "false",
                "status": "internal error",
                "traceback": traceback.format_exc()
            }}))
