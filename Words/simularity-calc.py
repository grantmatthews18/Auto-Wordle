#ADD measure for how many words a guess would remove from the board


import json
import copy

def word_to_phrase(word, phrase_len):
    phrase_arr = []
    for i in range(len(word)-(phrase_len-1)):
        phrase = ""
        for x in range(phrase_len):
            phrase += word[x+i]
        phrase_arr.append(phrase)
    return(phrase_arr)

def phrase_match_ct(word1, word2, phrase_len):
    if(word1 == word2):
        return(0)
    word1_arr = word_to_phrase(word1, phrase_len)
    word2_arr = word_to_phrase(word2, phrase_len)
    matching_ct = 0
    for i in range(len(word2_arr)):
        if word1_arr[i] in word2_arr:
            matching_ct += 1
            word2_arr[word2_arr.index(word1_arr[i])] = None
    return(matching_ct)

def process_words(filename = "Words/wordle-words.json"):
    with open(filename,"r+") as words_json:
        words = json.load(words_json)
        for word in words.keys():

            #for 5 letter words ->
            #[len, 1 letter match, 2 letter match, 3 letter match, 4 letter match, 5 letter match, 2 letter phrase match, 3 letter phrase match, 4 letter phrase match] <-
            words[word] = [len(word)]

            #getting letter matches
            #adding list rows corrosponding to number of letters in word + (2 through n) letter phrase matches
            for i in range(len(word)+(len(word)-2)):
                words[word].append(0)

            for temp_word in words:
                matching_ct = phrase_match_ct(word, temp_word,1)
                if(matching_ct > 0):
                    words[word][matching_ct] += 1

                for x in range(2,len(word)):
                    matching_ct = phrase_match_ct(word, temp_word,x)
                    if(matching_ct > 0):
                        words[word][len(word)+1+x-2] += 1
            for i in range(1,len(words[word])):
                words[word][i] = words[word][i]/len(list(words.keys()))
            print("Processed: ", word)

    with open(filename, "w+") as words_json:
        json.dump(words, words_json)
