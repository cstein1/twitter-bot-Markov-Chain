#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import re


def get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret):
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

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
        except:
            print("Encountered tweet with issue")
            pass
        tmp = tmp.encode("utf-8")
        f.write(tmp)
    f.close()
