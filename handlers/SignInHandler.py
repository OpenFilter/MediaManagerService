import traceback
import uuid
from datetime import datetime
import logging as log
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class SignInHandler(RequestHandler):

    db_users = None

    def initialize(self):
        couch = Server()
        if "users" not in couch:
            couch.create("users")
        self.db_users = couch['users']

    @staticmethod
    def url():
        return r'/signin'

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
                    if email in self.db_users:
                        if password == self.db_users[email].get("password", None):
                            user = self.db_users[email]
                            session_id = str(uuid.uuid4())
                            tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            user["session_id"] = session_id
                            user["last_login"] = tstamp
                            log.debug('USER:' + user.id)
                            self.db_users[user.id] = user
                            self.write(json_encode({"signin":{
                                "response": "true",
                                "status": "success",
                                "session_id": session_id,
                                "last_login": tstamp,
                                "user_id": email,
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
