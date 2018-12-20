import os

import tweetdump
import gracebot


def main():
    screen_name =

    consumer_key =
    consumer_secret =
    access_key =
    access_secret =

    if not os.path.exists("./{0}".format(screen_name)):
        os.mkdir("./{0}".format(screen_name))
    if not os.path.exists("{0}/{0}_tweets.txt".format(screen_name)):
        tweetdump.get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret)
    gracebot.generateSentence(screen_name = screen_name, seedword = "my", times = 5)


if __name__ == "__main__":
    main()
