import traceback
import uuid
from datetime import datetime
import logging as log
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class SubmitStoryHandler(RequestHandler):

    db_stories = None

    def initialize(self):
        couch = Server()
        if "stories" not in couch:
            couch.create("stories")
        self.db_stories = couch['stories']

    @staticmethod
    def url():
        return r'/submit_story'

    def post(self):
        jstr = self.request.body
        self.submit_story(jstr)

    def get(self):
        jstr = self.get_argument("js")
        self.submit_story(jstr)

    def submit_story(self, jstr):
        js = json_decode(jstr)
        if js is None:
            self.write(json_encode({"submit_story":{
                "response": "false",
                "status": "empty json"
            }}))
        try:
            if "submit_story" in js and type(js["submit_story"]) is dict:
                req = js["submit_story"]
                session_id = req.get("session_id", None)
                user_id= req.get("user_id", None)
                media_type = req.get("media_type", None)
                media_url = req.get("media_url", None)
                media_name = req.get("media_name", None)
                media_bucket = req.get("media_bucket", None)
                story_id = req.get("story_id", None)
                intro = req.get("intro", None)
                title = req.get("title", None)
                tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if session_id and story_id and user_id:
                    if story_id in self.db_stories:
                        self.write(json_encode({"submit_story":{
                            "response": "false",
                            "status": "story_id already exists",
                        }}))
                        return
                    self.db_stories[story_id] = {
                        "user_id": user_id,
                        "session_id": session_id,
                        "media_type": media_type,
                        "media_url": media_url,
                        "media_name": media_name,
                        "media_bucket": media_bucket,
                        "intro": intro,
                        "title": title,
                        "timestamp": tstamp,
                    }          
                    self.write(json_encode({"submit_story":{
                        "response": "true",
                        "status": "success",
                        "story_id": story_id,
                        "timestamp": tstamp
                    }}))
                else:
                    self.write(json_encode({"submit_story":{ 
                        "response": "false",
                        "status": "missing required param: session_id, story_id, user_id"
                    }})) 
            else:
                self.write(json_encode({"submit_story":{
                     "response": "false",
                     "status": "bad method"
                }}))
        except Exception:
            self.write(json_encode({"submit_story":{
                "response": "false",
                "status": "internal error",
                "traceback": traceback.format_exc()
            }}))
