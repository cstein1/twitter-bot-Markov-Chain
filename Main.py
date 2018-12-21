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
    if not os.path.exists("{0}/{0}_tweets.txt".format(screen_name)):
        tweetdump.get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret)
    gracebot.generateSentence(screen_name = screen_name, seedword = seed_word, times = num_times, max_words_per_sentence = max_words_per_sentence)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--renew_tweet_dump", help="Redownloads all tweets from given username", action="store_true")
    parser.add_argument("-n", "--screen_name", help="The screen name of the user to imitate.", type=str)
    parser.add_argument("-r", "--number_generations", help="The number of times to repeat the sentence generation", type=int, default=5)
    parser.add_argument("-m", "--max_words_per_sentence", help="The number of words per sentence generation", type=int, default=1000)
    parser.add_argument("-s", "--seed_word", help="The seed word to generate sentence from", type=str, default="the")
    args = parser.parse_args()


    if args.renew_tweet_dump:
        renew_tweet_dump = False
    if args.screen_name:
        screen_name = args.screen_name
    else:
        print("Enter a screen name using the -n, --screen_name flag")
        sys.exit(1)
    if args.number_generations:
        num_times = args.number_generations
    if args.seed_word:
        seed_word = args.seed_word
    if args.max_words_per_sentence:
        max_words_per_sentence = 1000

    main(screen_name = screen_name, renew_tweet_dump = renew_tweet_dump, num_times = num_times, seed_word = seed_word)
