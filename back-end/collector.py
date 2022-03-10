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
    # username=os.getenv("DB_USERNAME"), 
    # password=os.getenv("DB_PASSWORD"), 
    authSource=os.getenv("DB_AUTH_DB")
)

db = client[os.getenv("DB_AUTH_DB")]

class RunnningThreads():
    def __init__(self):
        self.runnning_threads = []

    def GetThreads(self):
        return self.runnning_threads

    def AddThread(self, thread):
        self.runnning_threads.append(thread)

    def RemoveThread(self, identity):
        for i in range(len(self.runnning_threads)):
            if self.runnning_threads[i]["id"] == identity:
                del self.runnning_threads[i]
                break


class StreamListener(tweepy.StreamListener):
    def __init__(self, identity, collection_name, datetime_end, thread_conrtroller):
        self.api = tweepy.API(
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True,
            compression=True
        )
        self.identity = identity
        self.collection_name = collection_name
        self.datetime_end = datetime_end.replace(" ", "-").replace(":", "-")
        self.thread_conrtroller = thread_conrtroller
        self.index_status = False

    def log_to_file(self, content):
        datetm = datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
        path = os.getenv("LOG_FILE")
        f = open(path, "a")
        f.write(f"[{datetm}] - {self.identity} - {content}\n")
        f.close()

    def on_connect(self):
        # Called initially to connect to the Streaming API
        self.log_to_file("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        self.log_to_file('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        nowdatetm = list(map(int, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S").split("-")))
        now_comparable = datetime.datetime(nowdatetm[0], nowdatetm[1], nowdatetm[2], nowdatetm[3], nowdatetm[4], nowdatetm[5])
        
        enddatetm = list(map(int, self.datetime_end.split("-")))
        end_comparable = datetime.datetime(enddatetm[0], enddatetm[1], enddatetm[2], enddatetm[3], enddatetm[4], enddatetm[5])

        if now_comparable > end_comparable:
            self.thread_conrtroller.RemoveThread(self.identity)
            exit()
        
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
            coll=db[self.collection_name]
            
            coll.insert_one(datajson)

            if not self.index_status:
                coll.create_index([('text', pymongo.TEXT)], name='text_index', default_language='english')
                coll.create_index([('created_at_converted', pymongo.ASCENDING)], name='created_at_index', default_language='english')
                coll.create_index([('user.id_str', pymongo.ASCENDING)], name='user_index', default_language='english')
                coll.create_index([('lang', pymongo.ASCENDING)], name='lang_index', default_language='english')
                self.index_status = True

                # print ('inserted')
            #print a message that the tweet has been inserted into the Db
            #print ('tweet inserted')
        except Exception as e:
           self.log_to_file(e)
