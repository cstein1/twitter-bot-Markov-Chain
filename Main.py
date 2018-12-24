import os
import argparse
import sys
import time

import twitter_handler
import gracebot

# THIS NEEDS TO BE FILLED IN
# CREATE AN APP AT developer.twitter.com AND PUT TOKENS HERE
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def tweet_once(screen_name, seed_word, renew_tweet_dump = True, num_times = 1, max_words_per_sentence = 1000, print_to_CL = False, show_dic = False):
    handler = twitter_handler.TwitterHandler(consumer_key, consumer_secret, access_key, access_secret)
    preProcess(handler, screen_name, renew_tweet_dump)
    tweet = gracebot.generateSentence(screen_name = screen_name, seedword = seed_word, max_words_per_sentence = max_words_per_sentence, max_chars = 280, show_dic = show_dic)
    if print_to_CL:
        print(tweet)
    else:
        handler.update_status(status = tweet)
    print("Tweeted Successfully")

# Makes appropriate folders and files
def preProcess(handler, screen_name, renew_tweet_dump):
    if not os.path.exists("./{0}".format(screen_name)):
        os.mkdir("./{0}".format(screen_name))
    if not os.path.exists("{0}/{0}_tweets.txt".format(screen_name)) or renew_tweet_dump:
        handler.get_all_tweets(screen_name)

# Do not tweet: download the tweets only
def justDownload(screen_name):
    handler = twitter_handler.TwitterHandler(consumer_key, consumer_secret, access_key, access_secret)
    if not os.path.exists("./{0}".format(screen_name)):
        os.mkdir("./{0}".format(screen_name))
    handler.get_all_tweets(screen_name)

def listen():
    handler = twitter_handler.TwitterHandler(consumer_key, consumer_secret, access_key, access_secret)
    cnt = 0
    while True:
        payload = handler.grab_latest_mentions()
        if not payload:
            print("no new tweets")
            pass;
        else:
            for name, tweet in payload:
                split_data = tweet.lower().split()
                cursor = 0
                while("ubot" not in split_data[cursor]):
                    cursor += 1
                if cursor < len(split_data):
                    try:print("Name: {0}\nTweet: {1}".formate(name,split_data))
                    except:print("tweeted with emoji")
                    tweet_once(screen_name = name, seed_word = split_data[cursor])
        time.sleep(60)
        # cnt += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stream", help="Listen to updates and respond in Twitter!",
                        action="store_true", default=False)
    parser.add_argument("-d", "--renew_tweet_dump",
                        help="Re[d]ownloads all tweets from given username, then proceeds to generate new tweets",
                        action="store_true", default=False)
    parser.add_argument("-n", "--screen_name",
                        help="The screen [n]ame of the user to imitate.", type=str)
    parser.add_argument("-r", "--number_generations",
                        help="The number of times to [r]epeat the sentence generation", type=int, default=5)
    parser.add_argument("-m", "--max_words_per_sentence",
                        help="The [m]aximum number of words per sentence generation",
                        type=int, default=1000)
    parser.add_argument("-w", "--seed_word",
                        help="The [s]eed word to generate sentence from", type=str)
    parser.add_argument("-j", "--just_download",
                        help="[J]ust download the entire feed of username specified with -s flag",
                        action="store_true", default=False)
    parser.add_argument("-l", "--local_print",
                        help="Print to the [l]ocal command line. USE THIS IF YOU DO NOT WANT TO TWEET.",
                        action="store_true", default=False)
    parser.add_argument("--show_dic", help="Print the dictionary and exit.", action="store_true", default=False)
    args = parser.parse_args()

    if args.stream:
        sys.stdout.write("Setting up stream\n")
        listen()
        sys.exit(0)

    if args.screen_name:
        screen_name = args.screen_name
    else:
        print("Enter a screen name using the -n, --screen_name flag")
        sys.exit(1)

    if args.just_download:
        justDownload(screen_name)

        sys.exit(2)

    if args.number_generations:
        num_times = args.number_generations
    else:
        print("Error with -r,--number_generations flag. See -h for usage.")
        sys.exit(1)

    if args.seed_word:
        seed_word = args.seed_word
    else:
        print("Error with -s, --seed_word flag. See -h for usage.")
        sys.exit(1)

    if args.max_words_per_sentence:
        max_words_per_sentence = args.max_words_per_sentence
    else:
        print("Error with -m, --max_words_per_sentence flag. See -h for usage.")
        sys.exit(1)

    local_print = args.local_print
    renew_tweet_dump = args.renew_tweet_dump
    show_dic = args.show_dic



    tweet_once(screen_name = screen_name, renew_tweet_dump = renew_tweet_dump, num_times = num_times, seed_word = seed_word, max_words_per_sentence= max_words_per_sentence, print_to_CL = local_print, show_dic = show_dic)
