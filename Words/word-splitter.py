# A Simple Python Script to split and organize the words.json file
# Words provided by https://github.com/dwyl/english-words

import json

word_dicts = [{}] * 32 #longest word is 31 letters long

with open("words.json") as words_json:
    words = json.load(words_json)
    for word in words.keys():

        if not(word_dicts[len(word)]):
            word_dicts[len(word)] = {}
        word_dicts[len(word)][word] = 0

x = 0
for i in word_dicts:
    print(x)
    if(i):
        filepath = "words-" + str(x) + ".json"
        file = open(filepath, "w+")
        json.dump(i, file)
    x += 1
