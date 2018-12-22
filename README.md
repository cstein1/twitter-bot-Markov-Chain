https://developer.twitter.com/
Go there to get access to tweepy

# How it Works
## Prep
The process begins in [twitter_handler.py](https://github.com/cstein1/twitter-bot-Markov-Chain/blob/master/twitter_handler.py).
The class TwitterHandler deals with all of the Twitter API interactions via python package [tweepy](https://github.com/tweepy/tweepy).
The only thing that is required from the user to interact with Twitter is consumer tokens and accessor tokens for a [Twitter app](https://developer.twitter.com/).
The function *TwitterHandler.get_all_tweets()* will grab all tweets from a given user under *TwitterHandler.screen_name*, and compile them into a single text file. Each tweet begins with "<SOS>" (start of string) and ends with "<EOS>" (end of string).
  
## Guiding Structure
[gracebot.py](https://github.com/cstein1/twitter-bot-Markov-Chain/blob/master/gracebot.py) holds the guiding structure of the string generation algorithm.
An outer-dictionary *grdic* holds, as a key, every non-terminating word in every tweet from the given username.
Outer-keys in *grdic* each map to dictionaries with, as inner-keys, words following the outer keys.
The inner-keys then map respectively to how frequently the inner-key follows the outer key.

Example Tweets:
 1) I enjoyed our walk today
 2) I thought our walk was good
 3) I enjoyed today
 
Corresponding Example Dictionary:

{

 "I" : {"enjoyed : 2, "thought" : 1},

 "enjoyed" : {"our" : 1, "today" : 1},

 "our" : {"walk" : 2},

 "walk" : {"today" : 1, "was" : 1},

 "thought" : {"our" : 1},

 "was" : {"good" : 1}
 
 }
 
 Example Inspection:
 "enjoyed" followed "I" twice, so *grdic["I"]["enjoyed"]=2*.

## Execution
To generate a tweet, we take a walk through the dictionary defined in the previous section.
The user will provide a "seed word" as an input to *gracebot.generateSentence(_)*.
The first word is used to determine the starting point of the walk, and the following words are sampled from the inner-dictionary.

Example Walk: INPUT: "walk"

 - We begin at *grdic["walk"]* and see that there are two possible directions, "today" and "was."
There is a 50/50 chance for one to be chosen over the other, since they bot follow "walk" the same amount of times.
We sample *grdic["walk"]* and find "was."

 - We are now at *grdic["was"]* and see that there is one possibility "good."
*grdic["good"]* does not exist, so our output will be "walk was good."

Sampling the inner-dictionary, found in *gracebot.takeLastWordAndPredict(_)* will create a distribution of the inner-keys and choose an inner-key with probability *inner-key's value/sum of inner-keys' values*
