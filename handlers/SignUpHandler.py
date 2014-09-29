import traceback
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class SignUpHandler(RequestHandler):

    db_users = None

    def initialize(self):
        couch = Server()
        if "users" not in couch:
            couch.create("users")
        self.db_users = couch['users']

    @staticmethod
    def url():
        return r'/signup'

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
                    if js["signup"]["email"] in self.db_users:
                        self.write(json_encode({"signup":{
                            "response": "false",
                            "status": "user exists"
                        }}))
                    else:
                        self.db_users[email] = {
                            "email": email,
                            "password": password
                        }
                        self.write(json_encode({"signup":{
                            "response": "true",
                            "user_id": email,
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


