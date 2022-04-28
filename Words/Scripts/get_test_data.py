#Calculates Support for every 1,2,3, and 4 letter itemset
#Each letter is also assigned its position in the word
#i.e. the E in hello would be e1 and the e in evict would be e0


import json
import copy

dna = [1,1,1,1]

with open("Words/wordle-answers.json","r+") as words_json:
    words = json.load(words_json)

words_lst = list(words)

test_data = {}
for i in range(310):
    test_data[words_lst[i]] = []

with open("Words/wordle-first_300.json","w+") as words_json:
    json.dump(test_data,words_json)
