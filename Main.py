import os
import argparse
import sys

import tweetdump
import gracebot

def main(screen_name, renew_tweet_dump, num_times, seed_word, max_words_per_sentence):
    consumer_key =
    consumer_secret =
    access_key =
    access_secret =

    if not os.path.exists("./{0}".format(screen_name)):
        os.mkdir("./{0}".format(screen_name))
    if not os.path.exists("{0}/{0}_tweets.txt".format(screen_name)) or renew_tweet_dump:
        tweetdump.get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret)
    gracebot.generateSentence(screen_name = screen_name, seedword = seed_word, times = num_times, max_words_per_sentence = max_words_per_sentence)

def justDownload(screen_name):
    consumer_key = "EQYbbYqLmS8kjIP3CJe4VZxPk"
    consumer_secret = "BT9hvi1SUo2LRhR1JePDcT7AwxeAEbyHWtL7bzDcYkXHvocury"
    access_key = "836023087263010816-7zafi3zuLSamduYhCacKfzQoucl1N9q"
    access_secret = "4cCMrnBhFLjlKHZu7ODXAdnm5euzmyPvzWB37N4eZwHG0"
    if not os.path.exists("./{0}".format(screen_name)):
        os.mkdir("./{0}".format(screen_name))
    tweetdump.get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--renew_tweet_dump", help="Re[d]ownloads all tweets from given username, then proceeds to generate new tweets", action="store_true")
    parser.add_argument("-n", "--screen_name", help="The screen [n]ame of the user to imitate.", type=str)
    parser.add_argument("-r", "--number_generations", help="The number of times to [r]epeat the sentence generation", type=int, default=5)
    parser.add_argument("-m", "--max_words_per_sentence", help="The [m]aximum number of words per sentence generation", type=int, default=1000)
    parser.add_argument("-s", "--seed_word", help="The [s]eed word to generate sentence from", type=str)
    parser.add_argument("-j", "--just_download", help="[J]ust download the entire feed of username specified with -s flag", action="store_true")
    args = parser.parse_args()

    if args.screen_name:
        screen_name = args.screen_name
    else:
        print("Enter a screen name using the -n, --screen_name flag")
        sys.exit(1)

    if args.just_download:
        justDownload(screen_name)
        sys.exit(0)

    if args.renew_tweet_dump:
        renew_tweet_dump = args.renew_tweet_dump
    else:
        renew_tweet_dump = False

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

    main(screen_name = screen_name, renew_tweet_dump = renew_tweet_dump, num_times = num_times, seed_word = seed_word, max_words_per_sentence= max_words_per_sentence)
