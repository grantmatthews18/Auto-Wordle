
import json
import copy

with open("Words/wordle-words.json","r+") as words_json:
    words = json.load(words_json)
    for word in words.keys():

        words[word] = [len(word),0,0,0,0,0]

        temp_words = copy.deepcopy(words.keys())
        for temp_word in temp_words:
            temp_word_arr = [char for char in temp_word]
            matching_ct = 0
            for char in word:
                if char in temp_word_arr:
                    matching_ct += 1
                    temp_word_arr[temp_word_arr.index(char)] = None

            #update word dict value depemdng on matching_ct
