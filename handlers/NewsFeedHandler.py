import traceback
import re
import uuid
from datetime import datetime
import logging as log
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class NewsFeedHandler(RequestHandler):

    db_stories = None

    def initialize(self):
        couch = Server()
        if "stories" not in couch:
            couch.create("stories")
        self.db_stories = couch['stories']

    @staticmethod
    def url():
        return r'/news_feed/([^/]+)'

    def post(self):
        jstr = self.request.body
        self.news_feed(jstr)

    def get(self, user_id):
        try:
            user_id = user_id.replace('.json', '')
            news_feed = []
            for row in self.db_stories.view('stories/by_user_id', key=user_id, include_docs="true", descending="true", limit=10):
                story = row.doc
                story['story_id'] = story['_id']
                del story['_id']
                del story['_rev']
                del story['session_id']
                if 'media_name' not in story:
                    m = re.match('https\:\/\/.+amazonaws\.com\/(.+)\/(.+)', story['media_url'])
                    if m is not None:
                        story['media_bucket'] = m.group(1)
                        story['media_name'] = m.group(2)
                news_feed.append(story)
            self.write(json_encode({"news_feed":{
                        "response": "true",
                        "status": "success",
                        "news_feed": news_feed,
            }}))
        except Exception:
            self.write(json_encode({"news_feed":{
                "response": "false",
                "status": "internal error",
                "traceback": traceback.format_exc()
            }}))
