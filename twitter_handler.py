#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import re

class TwitterHandler:
    api = None;screen_name = None;consumer_key = None;
    consumer_secret = None;access_key = None;access_secret = None

    def __init__(self, screen_name, consumer_key, consumer_secret, access_key, access_secret):
        self.screen_name = screen_name
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
        self.authorize()

    def authorize(self):
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(auth)

    def update_status(self, status):
        self.api.update_status(status = status)

    def get_all_tweets(self):
        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name = self.screen_name, count=200)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet (zero indexed)
        try:oldest = alltweets[-1].id - 1
        except IndexError as e:
            print("[ERROR] You are not following, or have access to the account {0}".format(self.screen_name))
            raise e

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))

            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name = self.screen_name,count=200,max_id=oldest)

            #save most recent tweets
            alltweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print( "...%s tweets downloaded so far" % (len(alltweets)))

        f = open("./{0}/{0}_tweets.txt".format(self.screen_name), "wb")
        for (ind,i) in enumerate(alltweets):
            tmp = ""
            try:
                if not i.text.startswith("RT",0,2):
                    tmp += "<SOS>"
                    tmp += re.sub(r"http\S+", "", str(i.text))
                    #if(len(tmp) > longestString): longestString = len(tmp)
                    tmp += "<EOS>"
            except:
                print("Encountered tweet with issue")
                pass
            tmp = tmp.encode("utf-8")
            f.write(tmp)
        f.close()
