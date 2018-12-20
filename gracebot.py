
import random
import sys

def generateSentence(screen_name, seedword = "my", times = 10, maxwords = 1000):
    with open("./{0}/{0}_tweets.txt".format(screen_name), "r", encoding='utf-8') as file:
        lines = file.read().lower()
    # Split by <EOS> end of string
    payload = lines.split("<eos>")
    # Get rid of <SOS> start of string
    payload = [txt[5:] for txt in payload]
    grdic = makedic(payload)
    print()
    for _ in range(times):
        makeSentence(grdic,seedword, maxwords)
        print("\n")

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

def printOptions(grdic, inp):
    print(inp)
    for ind,(key,value) in enumerate(grdic[inp].items()):
        sys.stdout.write(key + " ")

def makeSentence(grdic, startseed, numwords):
    # Makes full sentence
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

def window(iterator, window_width):
    inds = [[a for a in range(i-window_width,i)] for i in range(window_width, len(iterator)+1)]
    return [tuple([iterator[i] for i in ind]) for ind in inds]

def printNestedDic(dic):
    for key, indic in dic.items():
        try:print(key)
        except:print("*emoji*")
        for inkey, count in indic.items():
            try:print("\t" + inkey + ": " + str(count))
            except:print("\t*emoji*: " + str(count))
