import traceback
import re
import uuid
from datetime import datetime
import logging as log
from couchdb import Server
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode

class StoryFeedHandler(RequestHandler):

    db_stories = None
    db_posts = None

    def initialize(self):
        couch = Server()
        if "stories" not in couch:
            couch.create("stories")
        self.db_stories = couch['stories']
        if "posts" not in couch:
            couch.create("posts")
        self.db_posts = couch['posts']

    @staticmethod
    def url():
        return r'/story_feed/([^/]+)'

    def story(self):
        jstr = self.request.body
        self.story_feed(jstr)

    def get(self, story_id):
        try:
            if story_id in self.db_stories:
                story = self.db_stories[story_id]
                story['story_id'] = story['_id']
                del story['_id']
                del story['_rev']
                del story['session_id']
                if 'media_name' not in story:
                    m = re.match('https\:\/\/.+amazonaws\.com\/(.+)\/(.+)', story['media_url'])
                    if m is not None:
                        story['media_bucket'] = m.group(1)
                        story['media_name'] = m.group(2)
                posts = []
                for row in self.db_posts.view('posts/by_story_id', key=story_id, limit=100, descending="true", include_docs="true"):
                    post = row.doc
                    if post is None:
                        continue
                    post['post_id'] = post['_id']
                    del post['_rev']
                    del post['_id']
                    if 'media_name' not in post:
                        m = re.match('https\:\/\/.+amazonaws\.com\/(.+)\/(.+)', post['media_url'])
                        if m is not None:
                            post['media_bucket'] = m.group(1)
                            post['media_name'] = m.group(2)
                    posts.append(post)
                self.write(json_encode({"story_feed":{
                        "response": "true",
                        "status": "success",
                        "story": story,
                        "posts": posts 
                }}))
            else:
                self.write(json_encode({"story_feed":{
                     "response": "false",
                     "status": "story_id not found"
                }}))
        except Exception:
            self.write(json_encode({"story_feed":{
                "response": "false",
                "status": "internal error",
                "traceback": traceback.format_exc()
            }}))
