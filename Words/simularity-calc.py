
import json

with open("Words/wordle-words.json","r+") as words_json:
    words = json.load(words_json)
    for word in words.keys():

        #normalized hamming distance
        for i in range(len(word)):
            if(word[i])

        words[word] = [len(word),0,0,0]
