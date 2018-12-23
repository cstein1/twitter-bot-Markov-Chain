import os
import argparse
import sys

import twitter_handler
import gracebot

# THIS NEEDS TO BE FILLED IN
# CREATE AN APP AT developer.twitter.com AND PUT TOKENS HERE
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def main(screen_name, renew_tweet_dump, num_times, seed_word, max_words_per_sentence, print_to_CL, show_dic):
    handler = twitter_handler.TwitterHandler(screen_name, consumer_key, consumer_secret, access_key, access_secret)
    preProcess(handler, renew_tweet_dump)
    tweet = gracebot.generateSentence(screen_name = screen_name, seedword = seed_word, max_words_per_sentence = max_words_per_sentence, max_chars = 280, show_dic = show_dic)
    if print_to_CL:
        print(tweet)
    else:
        handler.update_status(status = tweet)
    print("Tweeted Successfully. Exiting...")
    sys.exit(0)

# Makes appropriate folders and files
def preProcess(handler, renew_tweet_dump):
    if not os.path.exists("./{0}".format(handler.screen_name)):
        os.mkdir("./{0}".format(handler.screen_name))
    if not os.path.exists("{0}/{0}_tweets.txt".format(handler.screen_name)) or renew_tweet_dump:
        handler.get_all_tweets()

# Do not tweet: download the tweets only
def justDownload(screen_name):
    handler = twitter_handler.TwitterHandler(screen_name, consumer_key, consumer_secret, access_key, access_secret)
    if not os.path.exists("./{0}".format(screen_name)):
        os.mkdir("./{0}".format(screen_name))
    handler.get_all_tweets()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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

    main(screen_name = screen_name, renew_tweet_dump = renew_tweet_dump, num_times = num_times, seed_word = seed_word, max_words_per_sentence= max_words_per_sentence, print_to_CL = local_print, show_dic = show_dic)
