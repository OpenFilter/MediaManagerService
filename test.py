#!/usr/bin/python
# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

import httplib
import json
import pprint
import uuid

connection = httplib.HTTPConnection(
    '%s:%d' % (
        'api.beekyn.com',
        8888,
    )
)

email = 'maq@beekyn.com'
password = '1.5billion'

# Signup Test
body_content = {'signup':{
    'password': '1.5billion',
    'email': 'maq@beekyn.com',
}}
body_content = json.dumps(body_content)
connection.request('POST', '/signup', body_content)
result = connection.getresponse()
pprint.pprint(json.loads(result.read()))

# Signin Test
body_content = {'signin':{
    'password': '1.5billion',
    'email': 'maq@beekyn.com',
}}
body_content = json.dumps(body_content)
connection.request('POST', '/signin', body_content)
result = connection.getresponse()
response = json.loads(result.read())
pprint.pprint(response)
session_id = response['signin']['session_id']

body_content = {'fb_signin':{
    'fb_id': 'XYZ',
    'fb_email': 'maq@beekyn.com',
    'fb_name': 'msq',
    'fb_birthdate': '1/1/2011',
    'fb_locale': 'en-us',
    'fb_location': 'Palo Alto, CA',
    'fb_language':'english',
    'fb_gender': 'male'

}}
body_content = json.dumps(body_content)
connection.request('POST', '/fb_signin', body_content)
result = connection.getresponse()
response = json.loads(result.read())
pprint.pprint(response)


# Submit Story
intro = "This is an intro"
title = "Title of the Story"
user_id = email
media_type = "photo"
media_url = "https://s3-us-west-2.amazonaws.com/movie-bucket-03yzfxj8r1whmpxsr7g2/my_movie"
story_id = user_id + '_' + str(uuid.uuid4())

content = {'submit_story':{
    "story_id": story_id,
    "user_id": user_id,
    "session_id": session_id,
    "media_type": media_type,
    "media_url": media_url,
    "intro": intro,
    "title": title,
}}

body_content = json.dumps(content)
connection.request('POST', '/submit_story', body_content)
result = connection.getresponse()
pprint.pprint(json.loads(result.read()))

# Submit Post
description = "This is a Description of a Post"
media_type = "video"
media_url = "https://s3-us-west-2.amazonaws.com/movie-bucket-03yzfxj8r1whmpxsr7g2/my_movie"
title = "Title of a post"
user_id = email
post_id = story_id + '_' + str(uuid.uuid4())

content = {'submit_post':{
    "story_id": story_id,
    "post_id": post_id,
    "user_id": user_id,
    "session_id": session_id,
    "media_type": media_type,
    "media_url": media_url,
    "description": description,
    "title": title,
}}

body_content = json.dumps(content)
connection.request('POST', '/submit_post', body_content)
result = connection.getresponse()
pprint.pprint(json.loads(result.read()))

# Get News Feed

connection.request('GET', '/news_feed/' + user_id)
result = connection.getresponse()
res_dic = json.loads(result.read())
pprint.pprint(res_dic['news_feed'])
for story in res_dic['news_feed']['news_feed']:
    connection.request('GET', '/story_feed/' + story['story_id'])
    result = connection.getresponse()
    pprint.pprint(json.loads(result.read()))
