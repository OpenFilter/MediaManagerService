MediaManagerService
===================

The Media Manager API is an HTTP, JSON-based API. 
<pre>
1. Signup
URL: /signup
Method: POST 
Request:
{“signup”:
     {
    “email”: XYZ,
    “password”: XYZ
     }
}
Response:
{“signup”:
    {
    “response”: “true” | “false”,
    “status”: XYZ,
    “user_id”: ABC
    }
}

2. Signin
URL: /signin
Method: POST 
Request:
{“signin”:
    {
    “email”: XYZ,
    “password”: XYZ
    {
}

Response:
{“signin”:
    {
    “response”: “true” | “false”,
    “status”: XYZ,
    “session_id”: XYZ,
    “user_id”: ABC
    }
}

2. Facebook Signin
URL: /fb_signin
Method: POST 
Request:
{“fb_signin”:
    {
    “fb_id”: <string>,
    “fb_name”: <string>,
    “fb_birthdate”: <string>,
    “fb_locale”: <string>,
    “fb_location”: <string>,
    “fb_language”: <string>,
    “fb_gender”: <string>
    {
}

Response:
{“fb_signin”:
    {
    “response”: “true” | “false”,
    “status”: XYZ,
    “session_id”: XYZ,
    “user_id”: ABC
    }
}

3. Submit Post
URL: /submit_post
Method: POST 
File Naming Convention (same as post_id): post:<user_id><media_type><uuid>
Request:
{“submit_post”:
    {
           “post_id”: <user_id><media_type><uuid>,
    “session_id”: XYZ,
    “user_id”: ABC,
    “story_id”: <string>,
    “media_type”: “audio|video|photo|text”,
    “media_url”: <S3 URL>,
    “description”: “ABC”
“title” : “titulo”,
“body”: “cuerpo”
    {
}

Response:
{“submit_post”:
    {
    “response”: “true” | “false”,
    “status”: XYZ,
    “session_id”: XYZ
    }
}


4. News Feed
URL: /news_feed/session_id/<all|audio|image|text>
Method: GET 
Response:
{“news_feed”:{
    “status”: <string>,
    “session_id”: <string>,
    “feed”: [
        {
            “story_id”: <string>,
            “position”: <integer>,
            “story_image”: <url_string>,
            “URL”: <string>,
            “contributions”: <string>,
            “reads”: <string>,
            “shares”: <string>,
            “creator”: {
                “user_id”: <string>,
                “user_image_url”: <string>
            },
        },
        {
            “story_id”: <string>,
            “position”: <integer>,
            “URL”: <string>,
            “contributions”: <string>,
            “reads”: <string>,
            “shares”: <string>,
            “creator”: {
                “user_id”: <string>,
                “user_image_url”: <string>
            },
        }
    ]
}

5. Story Feed
URL: /story_feed/<story_id>
Method: GET 
Response:
{“story_feed”:{
    “story_id”: <string>,
    “position”: <integer>,
    “URL”: <string>,
    “contributions”: <string>,
    “reads”: <string>,
    “shares”: <string>,
    “creator”: {
        “user_id”: <string>,
        “user_image_url”: <string>
    },
“posts”:[
        {
            “post_id”: <string>,
            “media_type”: “audio|video|photo|text”,
            “URL”: <string>,
            “user_id”: <string>,
“title” : <string>,
“body”: <string>
},
{
            “post_id”: <string>,
            “media_type”: “audio|video|photo|text”,
            “URL”: <string>,
            “user_id”: <string>,
“title” : <string>,
“body”: <string>
}
    ]
}
</pre>
