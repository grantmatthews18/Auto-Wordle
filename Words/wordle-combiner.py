import json

words_lst = []

with open("Words/wordle-answers.json", "r+") as words_ans_json:
    words = json.load(words_ans_json)
    for word in words:
        words_lst.append(word)

with open("Words/wordle-words.json","r+") as words_json:
    words = json.load(words_json)
    for word in words:
        words_lst.append(word)
    words_json.truncate(0)

words_lst.sort()

for i in range(len(words_lst)):
    words[words_lst[i]] = 0

with open("Words/wordle-words.json","w+") as words_json:
    json.dump(words, words_json)
