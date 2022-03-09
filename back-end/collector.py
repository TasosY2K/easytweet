import os
import tweepy
import json
import pymongo
import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(
    host=os.getenv("DB_HOST"), 
    port=int(os.getenv("DB_PORT")), 
    username=os.getenv("DB_USERNAME"), 
    password=os.getenv("DB_PASSWORD"), 
    authSource=os.getenv("DB_AUTH_DB")
)

db = client[os.getenv("DB_AUTH_DB")]

class StreamListener(tweepy.StreamListener):
    def __init__(self, collection_name, datetime_end):
        self.api = tweepy.API(
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True,
            compression=True
        )
        self.collection_name = collection_name
        self.datetime_end = datetime_end

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        print(self.datetime_end)
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            datajson = json.loads(data)
            #grab the 'created_at' data from the Tweet to use for display and change it to Date object
            created_at = datajson['created_at']
            text = str(datajson['text'].encode('utf8'))
            dt=datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
            # verified = datajson['user']['verified']
            # print (verified)
            datajson['created_at_converted'] = dt
            # print (text)
            #print out a message to the screen that we have collected a tweet
            # print ("Tweet collected at " + str(dt))
            # if verified == True:
            coll=db[collection_name]
            coll.insert(datajson)
                # print ('inserted')
            #print a message that the tweet has been inserted into the Db
            #print ('tweet inserted')
        except Exception as e:
           print(e)
