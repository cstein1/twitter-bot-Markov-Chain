
import random
import sys

# Helper function that creates the main dictionary, then generates a sentence in style of screen_name
# param seedword: Seedword is inspiring word that must exist in user's vocabulary
# param max_words_per_sentence: Most words allowed in output
# param max_chars: Most characters allowed
def generateSentence(screen_name, seedword = "my", max_words_per_sentence = 1000,  max_chars = 280, show_dic = False):
    with open("./{0}/{0}_tweets.txt".format(screen_name), "r", encoding='utf-8') as file:
        lines = file.read().lower()
    # Split by <EOS> end of string
    payload = lines.split("<eos>")
    # Get rid of <SOS> start of string
    payload = [txt[5:] for txt in payload]
    grdic = makedic(payload)
    if show_dic:
        printOptions(grdic, seedword)
        sys.exit(2)
    return makeSentence(screen_name, grdic, seedword, max_words_per_sentence, max_chars)

# Creates a dictionary of {`word`: dictionary of {`next_word` following `word` : number times found after `word`}}
# param payload: List of tweets
# param key_length: TODO... Improve accuracy of markov chain
def makedic(payload, key_length = 2):
    grdic = {}
    for line in payload:
        for word,nxtword in window(line.split(), key_length):
            if word in grdic:
                if nxtword in grdic[word]:
                    grdic[word][nxtword]+=1
                else:
                    grdic[word][nxtword]=1
            else:
                grdic[word] = {nxtword:1}
    return grdic

# Creates a sentence by looping def takeLastWordAndPredict
# Return <WNF> if word has not been used in any tweet by user
# Return sentence_out: sentence returned
# param screen_name: Screen name of style of subject
# param grdic: Dictionary from def makedic
# param startseed: Seed word
# param numwords: Max number of words in sentence
# param  max_chars: Max number of characters allowed
def makeSentence(screen_name, grdic, startseed, numwords, max_chars):
    sentence_out = ".@{0} ".format(screen_name) + startseed
    newseedword = takeLastWordAndPredict(grdic,startseed)
    sentence_out += " " + newseedword
    climb = 0
    while(climb < numwords and len(sentence_out) < max_chars-1):
        newseedword = takeLastWordAndPredict(grdic,newseedword)
        if newseedword == "<WNF>" or len(sentence_out) + len(newseedword) >= max_chars:
            break;
        else:
            sentence_out += " "
            try:sentence_out += newseedword
            except:sentence_out += "<EMJ>"
            # On failure, probably emoji... so <EMJ>
        climb += 1
    if sentence_out[-1] not in ["!",".","?"]:
        sentence_out += "."
    return sentence_out

# Creates a probability list to sample from. For each instance of a `nxtword` following input `word` that is found,
#  create an entry in `probdic`. Then sample the whole list for the chosen next word.
# param dic: grdic; vocabulary dictionary
# param word: Word to find the next word from
def takeLastWordAndPredict(dic,word):
    #Finds next word
    if word.lower() not in dic:
        return "<WNF>"
    probdic = []
    for nxtword, uses in dic[word].items():
        for _ in range(uses):
            probdic.append(nxtword)
    nxtwordind = random.randint(0,len(probdic)-1)
    return probdic[nxtwordind]

#Iterator for looking through sliding window
# window([0,1,2,3], 2) => [[0,1],[1,2],[2,3]]
def window(iterator, window_width):
    inds = [[a for a in range(i-window_width,i)] for i in range(window_width, len(iterator)+1)]
    return [tuple([iterator[i] for i in ind]) for ind in inds]

def printOptions(grdic, inp):
    print(inp)
    for ind,(key,value) in enumerate(grdic[inp].items()):
        sys.stdout.write(key + ": " + str(value) + " | ")

def printNestedDic(dic):
    for key, indic in dic.items():
        try:print(key)
        except:print("*emoji*")
        for inkey, count in indic.items():
            try:print("\t" + inkey + ": " + str(count))
            except:print("\t*emoji*: " + str(count))
