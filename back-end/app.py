import os
import tweepy
import json
import uuid
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from collector import StreamListener, RunnningThreads

load_dotenv()

ThreadController = RunnningThreads()

app = Flask(__name__)

cors = CORS(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per hour"],
)

client = MongoClient(
    host=os.getenv("DB_HOST"), 
    port=int(os.getenv("DB_PORT")), 
    # username=os.getenv("DB_USERNAME"), 
    # password=os.getenv("DB_PASSWORD"), 
    authSource=os.getenv("DB_AUTH_DB")
)

db = client[os.getenv("DB_AUTH_DB")]

def start_stream(access_token, access_token_secret, identity, collection_name, hashtags, datetime_end):
    while True:
        try:
            auth = tweepy.OAuthHandler(os.getenv("OAUTH_TOKEN"), os.getenv("OAUTH_TOKEN_SECRET"))
            auth.set_access_token(access_token, access_token_secret)
            
            listener = StreamListener(
                identity=identity,
                collection_name=collection_name,
                datetime_end=datetime_end,
                thread_conrtroller=ThreadController
            )
            
            streamer = tweepy.Stream(auth=auth, listener=listener)
            streamer.filter(track=hashtags)
        
        except Exception as e:
            print(e)
            continue


@app.before_request
def middlware():
    if not "Token" in request.headers:
        return "Token header is required", 401

    server_token = os.getenv("HEADER_SECRET")
    client_token = request.headers.get("Token")
    
    if client_token == server_token:
        pass
    else:
        return "Invalid token", 401


@app.route("/", methods=["GET"])
def index():
    return "Works"


@app.route("/req4req", methods=["GET"])
def req4req():
    request_token = OAuth1Session(
        client_key=os.getenv("OAUTH_TOKEN"), 
        client_secret=os.getenv("OAUTH_TOKEN_SECRET")
    )
    
    data = request_token.get("https://api.twitter.com/oauth/request_token")
    oauth_token = str.split(str.split(data.text, "&")[0], "=")[1]
    oauth_token_secret = str.split(str.split(data.text, "&")[1], "=")[1]
    
    return {
        "ok": True, 
        "oauth_token": oauth_token, 
        "oauth_token_secret": oauth_token_secret
    }


@app.route("/req2acc", methods=["POST"])
def req2acc():
    payload = request.get_json(force=True)
    oauth_token = OAuth1Session(
        client_key=os.getenv("OAUTH_TOKEN"), 
        client_secret=os.getenv("OAUTH_TOKEN_SECRET"),
        resource_owner_key=payload["oauth_token"],
        resource_owner_secret=payload["oauth_token_secret"]
    )
    
    data = oauth_token.post("https://api.twitter.com/oauth/access_token", data={"oauth_verifier": payload["oauth_verifier"]})
    oauth_token = str.split(str.split(data.text, "&")[0], "=")[1]
    oauth_token_secret = str.split(str.split(data.text, "&")[1], "=")[1]
    user_id = str.split(str.split(data.text, "&")[2], "=")[1]
    screen_name = str.split(str.split(data.text, "&")[3], "=")[1]
    
    return {
        "ok": True,
        "oauth_token": oauth_token,
        "oauth_token_secret": oauth_token_secret,
        "user_id": user_id,
        "screen_name": screen_name
    }


@app.route("/collect", methods=["POST"])
def collect():
    body = request.get_json()
    
    if not "access_token" in body or not "access_token_secret" in body or not "collection_name" in body or not "hashtags" in body or not "datetime_end" in body:
        return "Not enough or wrong arguments", 401

    if body["collection_name"] in db.list_collection_names():
        return "Collection already exists", 203

    identity = str(uuid.uuid4())[:8]

    thread = threading.Thread(
        target=start_stream,
        daemon=True,
        args=(
            body["access_token"],
            body["access_token_secret"],
            identity,
            body["collection_name"], 
            body["hashtags"], 
            body["datetime_end"],
        )
    )
    
    thread.start()

    ThreadController.AddThread({
        "id": identity,
        "collection_name": body["collection_name"],
        "hashtags": body["hashtags"],
        "datetime_end": body["datetime_end"]
    })

    return "Started collecting..."


@app.route("/monitor", methods=["GET"])
def monitor():
    runnning_threads = ThreadController.GetThreads()
    if len(runnning_threads) > 0:
        return json.dumps(runnning_threads)
    else:
        return "No runnning threads", 401


@app.route("/logs", methods=["GET"])
def logs():
    f = open(os.getenv("LOG_FILE"), "r")
    contents = f.read()
    f.close()
    return contents


if __name__ == "__main__":
    app.run(threaded=False, port=os.getenv("API_PORT"), host="0.0.0.0", debug=os.getenv("DEBUG"))