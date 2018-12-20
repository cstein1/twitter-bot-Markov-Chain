import os

import tweetdump
import gracebot


def main():
    screen_name = # ENTER SCREEN_NAME TO DUMP AND COPY HERE

    # FILL THESE OUT
    consumer_key =
    consumer_secret =
    access_key =
    access_secret =

    if not os.path.exists("%s_tweets.txt" % screen_name):
        tweetdump.get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret)
    gracebot.generateSentence(screen_name = screen_name, seedword = "my")


if __name__ == "__main__":
    main()
