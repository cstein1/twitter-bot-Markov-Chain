
import random
import sys

# Helper function that creates the main dictionary, then generates a sentence in style of screen_name
# param seedword: Seedword is inspiring word that must exist in user's vocabulary
# param max_words_per_sentence: Most words allowed in output
def generateSentence(screen_name, seedword = "my", max_words_per_sentence = 1000):
    with open("./{0}/{0}_tweets.txt".format(screen_name), "r", encoding='utf-8') as file:
        lines = file.read().lower()
    # Split by <EOS> end of string
    payload = lines.split("<eos>")
    # Get rid of <SOS> start of string
    payload = [txt[5:] for txt in payload]
    grdic = makedic(payload)
    makeSentence(grdic,seedword, max_words_per_sentence)

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
# param grdic: Dictionary from def makedic
# param startseed: Seed word
# param numwords: Max number of words in sentence
def makeSentence(grdic, startseed, numwords):
    sys.stdout.write(startseed)
    newseedword = takeLastWordAndPredict(grdic,startseed)
    sys.stdout.write(" " + newseedword)
    climb = 0
    while(climb < numwords):
        newseedword = takeLastWordAndPredict(grdic,newseedword)
        if newseedword == "<WNF>":
            sys.stdout.write(".")
            break;
        else:
            sys.stdout.write(" ")
            try:sys.stdout.write(newseedword)
            except:sys.stdout.write("*emoji*")
        climb += 1
    else: #If `break;` isn't hit
        sys.stdout.write(".")

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
        sys.stdout.write(key + " ")

def printNestedDic(dic):
    for key, indic in dic.items():
        try:print(key)
        except:print("*emoji*")
        for inkey, count in indic.items():
            try:print("\t" + inkey + ": " + str(count))
            except:print("\t*emoji*: " + str(count))
