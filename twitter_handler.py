#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import os
import re
from datetime import datetime

def log(txt, end = "\n"):
    string = "[" +str(datetime.now())+"] " + txt + end
    try:print(string)
    except:print("Special character")
    if not os.path.exists("log.txt"):
        with open("log.txt", "x", encoding="utf-8") as f:
            f.write("\n")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(string)

class TwitterHandler:
    api = None; latest_tweet = None; me = None
    consumer_key = None; consumer_secret = None; access_key = None; access_secret = None


    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
        self.authorize()
        self.me = self.api.me()
        self.set_latest_tweet()

    def authorize(self):
        print("[twitter_handler.authorize] Checking credentials...")
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth)

    def update_status(self, status):
        self.api.update_status(status = status)

    # TODO: instead of passing tweet, pass controversial word
    def inform_error(self, tweet):
        text = '''
        Thanks for submitting a tweet to me.\n
        Unfortunately, the seed you sent me is not a word you have used before.
        Try another word for now, please.
        DISCLAIMER: I do not store any information about you. I also only access public information.
        '''
        user = self.api.get_user(self.screen_name)
        event = {
          "event": {
            "type": "message_create",
            "message_create": {
              "target": {
                "recipient_id": user.id
              },
              "message_data": {
                "text": text
              }
            }
          }
        }
        print("Failed to tweet to {0}. TODO: Now sending direct message to user ID {1}.".format(self.screen_name, user.id))
        print("Exiting...")
        try:self.api.send_direct_message(event)
        except:print("Not functional yet")

    def set_latest_tweet(self):
        me = self.me
        new_tweets = self.api.mentions_timeline()
        oldest = new_tweets[-1].id -1
        aggregate = new_tweets
        mentions_of_me = list(filter(lambda e: e.user.id != me.id, new_tweets))
        count = 0
        while len(new_tweets)>0 and len(mentions_of_me)==0:
            log("API call init")
            try:
                new_tweets = self.api.mentions_timeline(max_id = oldest)
            except:
                log("Failed to retrieve first new tweet from feed. Let's die now.")
                pass; #wait 15 minutes
            for tweet in new_tweets:
                log("\t{0}:\t{1}".format(str(tweet.user.screen_name),str(tweet.text)))
            oldest = new_tweets[-1].id -1
            mentions_of_me = list(filter(lambda e: e.user.id != me.id, new_tweets))
            aggregate += mentions_of_me
        self.latest_tweet = mentions_of_me[0] # tweet object
        log("Latest tweet set")
        log("\t\t\t{0}\t{1}".format(str(self.latest_tweet.user.screen_name), str(self.latest_tweet.text)))
        return [(self.latest_tweet.user.screen_name, self.latest_tweet.text)]

    def grab_latest_mentions(self):
        me = self.me
        oldest = self.latest_tweet.id
        log("API call (first try)")
        new_tweets = self.api.mentions_timeline(since_id = oldest)
        if len(new_tweets) == 0:
            return None
        if self.latest_tweet.id == new_tweets[0].id:
            return None
        aggregate = []
        while len(new_tweets)!=0:
            log("API call (looping)", end = " ")
            oldest = new_tweets[0].id
            aggregate += new_tweets
            new_tweets = self.api.mentions_timeline(since_id = oldest)
        self.latest_tweet = aggregate[0]
        return [(tweet.user.screen_name, tweet.text) for tweet in aggregate]

    def get_all_tweets(self, screen_name):
        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name = screen_name, count=200)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet (zero indexed)
        try:oldest = alltweets[-1].id - 1
        except IndexError as e:
            print("[ERROR] You are not following, or have access to the account {0}".format(screen_name))
            raise e

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))

            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, tweet_mode='extended')

            #save most recent tweets
            alltweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print( "...%s tweets downloaded so far" % (len(alltweets)))

        f = open("./{0}/{0}_tweets.txt".format(screen_name), "wb")
        for (ind,i) in enumerate(alltweets):
            tmp = ""
            try:
                if not i.text.startswith("RT",0,2):
                    tmp += "<SOS>"
                    tmp += re.sub(r"http\S+", "", str(i.text))
                    #if(len(tmp) > longestString): longestString = len(tmp)
                    tmp += "<EOS>"
            except Exception as e:
                print(e)
                log(i.text)
                pass
            tmp = tmp.encode("utf-8")
            f.write(tmp)
        f.close()
