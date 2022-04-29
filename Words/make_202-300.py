import json
import copy

with open("Words/wordle-first_300-nyt.json","r+") as words_json:
    words = json.load(words_json)

i = 0
for word in list(words):
    if(i < 202):
        words.pop(word)
    i += 1

with open("Words/wordle-202-300-nyt.json","w+") as words_json:
    json.dump(words, words_json)
