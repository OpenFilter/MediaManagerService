import traceback
import uuid
from datetime import datetime
import logging as log
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class SubmitPostHandler(RequestHandler):

    db_posts = None

    def initialize(self):
        couch = Server()
        if "posts" not in couch:
            couch.create("posts")
        self.db_posts = couch['posts']

    @staticmethod
    def url():
        return r'/submit_post'

    def post(self):
        jstr = self.request.body
        self.submit_post(jstr)

    def get(self):
        jstr = self.get_argument("js")
        self.submit_post(jstr)

    def submit_post(self, jstr):
        js = json_decode(jstr)
        if js is None:
            self.write(json_encode({"submit_post":{
                "response": "false",
                "status": "empty json"
            }}))
        try:
            if "submit_post" in js and type(js["submit_post"]) is dict:
                req = js["submit_post"]
                session_id = req.get("session_id", None)
                user_id= req.get("user_id", None)
                media_type = req.get("media_type", None)
                media_url = req.get("media_url", None)
                media_bucket = req.get("media_bucket", None)
                media_name = req.get("media_name", None)
                story_id = req.get("story_id", None)
                post_id = req.get("post_id", None)
                description = req.get("description", None)
                title = req.get("title", None)
                body = req.get("body", None)
                tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if session_id and post_id and media_type and user_id:
                    if post_id in self.db_posts:
                        self.write(json_encode({"submit_post":{
                            "response": "false",
                            "status": "post_id already exists",
                        }}))
                        return
                    self.db_posts[post_id] = {
                        "user_id": user_id,
                        "session_id": session_id,
                        "media_type": media_type,
                        "media_url": media_url,
                        "media_name": media_name,
                        "media_bucket": media_name,
                        "story_id": story_id,
                        "description": description,
                        "title": title,
                        "body": body,
                        "timestamp": tstamp,
                    }          
                    self.write(json_encode({"submit_post":{
                        "response": "true",
                        "status": "success",
                        "post_id": post_id,
                        "timestamp": tstamp
                    }}))
                else:
                    self.write(json_encode({"submit_post":{ 
                        "response": "false",
                        "status": "missing required param: session_id, post_id, media_type, user_id"
                    }})) 
            else:
                self.write(json_encode({"submit_post":{
                     "response": "false",
                     "status": "bad method"
                }}))
        except Exception:
            self.write(json_encode({"submit_post":{
                "response": "false",
                "status": "internal error",
                "traceback": traceback.format_exc()
            }}))
