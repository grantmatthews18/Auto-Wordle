# A Simple Python Script to split and organize the words.json file
# Words provided by https://github.com/dwyl/english-words

import json

with open("Words/wordle-words.json","r+") as words_json:
    words = json.load(words_json)
    for word in words.keys():
        words[word] = [len(word),0,0,0]
    words_json.truncate(0)



with open("Words/wordle-words.json","w+") as words_json:
    json.dump(words, words_json)
