#Calculates Support for every 1,2,3, and 4 letter itemset
#Each letter is also assigned its position in the word
#i.e. the E in hello would be e1 and the e in evict would be e0


import json
import copy

dna = [1,1,1,1]

with open("Words/wordle-words.json","r+") as words_json:
    words = json.load(words_json)

words_letters = copy.deepcopy(words)

#Key is the string word and value is list of itemset tuples
words_itemsets = {}

#used to store the frequency values of all possible itemsets
itemsets = {}

#splitting words
#AND
#calculating frequency of itemsets
#AND
#merging
#doing all at once to save CPU cycles

for word in words.keys():
    words_itemsets[word] = []
    #split word, add letter position to letter
    word_arr = []#ADDED-----------------------------------------------------------
    pos = 0
    for char in word:
        word_arr.append(char+str(pos))
        pos +=1

    #add all possible itemsets to both word_temsets and itemsets
    for letter_pos in range(len(word_arr)):
        itemset = ()
        #setting upper range for itemset creation
        upper_range = letter_pos+(len(word_arr)-1)
        if(upper_range > len(word_arr)):
            upper_range = len(word_arr)
        #creating all itemsets that start with the letter at letter_pos
        for i in range(letter_pos,upper_range):
            #add to existing itemset for this letter
            itemset = itemset + (word_arr[i],)

            #check if itemset is already in itemsets
            if(itemset in itemsets):
                itemsets[itemset] += 1
            else:
                itemsets[itemset] = 1
            words_itemsets[word].append(itemset)

    if(word == "cooks"):
        print(words_itemsets[word])


#updating words support counts and costs
for word in words.keys():
    words[word] = [0] * (len(word)-1)
    for itemset in words_itemsets[word]:
        support = itemsets[itemset]
        words[word][len(itemset)-1] += support
    #modifying support values according to agent dna
    for i in range(len(words[word])):
        words[word][i] = float(words[word][i]/dna[i])

#updaing words_letters support counts based on support from words
for word in words_letters.keys():
    words_letters[word] = [0] * (len(word)-1)
    for itemset in words_itemsets[word]:
        support = itemsets[itemset]
        words_letters[word][len(itemset)-1] += support
    #modifying support values according to agent dna
    for i in range(len(words_letters[word])):
        words_letters[word][i] = float(words_letters[word][i]/dna[i])

#------------------------------------------------------------------------------------------

# #Key is the string word and value is list of itemset tuples
# words_itemsets = {}
#
# #used to store the frequency values of all possible itemsets
# itemsets = {}
#
# #splitting words
# #AND
# #calculating frequency of itemsets
# #AND
# #merging
# #doing all at once to save CPU cycles
#
# for word in words.keys():
#     words_itemsets[word] = []
#     #split word, add letter position to letter
#     word_arr = []#ADDED
#     pos = 0
#     for char in word:
#         word_arr.append(char+str(pos))
#         pos +=1
#
#     #add all possible itemsets to both word_temsets and itemsets
#     for letter_pos in range(len(word_arr)):
#         itemset = ()
#         for i in range(letter_pos,(len(word_arr)-1)):
#             #add to existing itemset for this letter
#             itemset = itemset + (word_arr[i],)
#
#             #check if itemset is already in itemsets
#             if(itemset in itemsets):
#                 itemsets[itemset] += 1
#             else:
#                 itemsets[itemset] = 1
#             words_itemsets[word].append(itemset)
#
# #updating words support counts and costs
# for word in words.keys():
#     words[word] = [0] * (len(word)-1)
#     for itemset in words_itemsets[word]:
#         support = itemsets[itemset]
#         words[word][len(itemset)-1] += support
#     #modifying support values according to agent dna
#     for i in range(len(words[word])):
#         words[word][i] = float(words[word][i]/dna[i])
#
# #updaing words_letters support counts based on support from words
# for word in words_letters.keys():
#     words_letters[word] = [0] * (len(word)-1)
#     for itemset in words_itemsets[word]:
#         support = itemsets[itemset]
#         words_letters[word][len(itemset)-1] += support
#     #modifying support values according to agent dna
#     for i in range(len(words_letters[word])):
#         words_letters[word][i] = float(words_letters[word][i]/dna[i])

#------------------------------------------------------------------------------------------

# #Key is the string word and value is list of itemset tuples
# words_itemsets = {}
#
# #used to store the frequency values of all possible itemsets
# itemsets = {}
#
# #splitting words
# #AND
# #calculating frequency of itemsets
# #AND
# #merging
# #doing all at once to save CPU cycles
# for word in words.keys():
#     words_itemsets[word] = []
#     word_arr = [char for char in word]
#     word_2arr = []
#     for i in range(len(word_arr)):
#         #split word
#         word_arr[i] = word_arr[i]+str(i)
#
#     #add itemsets to master itemsets list
#     for i in range(len(word_arr)):
#         #single letter itemsets
#         if((word_arr[i],) in itemsets):
#             itemsets[(word_arr[i],)] += 1
#         else:
#             itemsets[(word_arr[i],)] = 1
#         words_itemsets[word].append((word_arr[i],))
#
#         #2 letter itemsets
#         if(i < len(word_arr)-1):
#             itemset2 = (word_arr[i], word_arr[i+1])
#             if(itemset2 in itemsets):
#                 itemsets[itemset2] += 1
#             else:
#                 itemsets[itemset2] = 1
#             words_itemsets[word].append(itemset2)
#
#         #3 letter itemsets
#         if(i < len(word_arr)-2):
#             itemset3 = (word_arr[i], word_arr[i+1], word_arr[i+2])
#             if(itemset3 in itemsets):
#                 itemsets[itemset3] += 1
#             else:
#                 itemsets[itemset3] = 1
#             words_itemsets[word].append(itemset3)
#
#         #4 letter itemsets
#         if(i < len(word_arr)-3):
#             itemset4 = (word_arr[i], word_arr[i+1], word_arr[i+2], word_arr[i+3])
#             if(itemset4 in itemsets):
#                 itemsets[itemset4] += 1
#             else:
#                 itemsets[itemset4] = 1
#             words_itemsets[word].append(itemset4)
#
# for word in words_itemsets.keys():
#     words[word] = [0] * (len(word)-1)
#     for itemset in words_itemsets[word]:
#         support = itemsets[itemset]
#         words[word][len(itemset)-1] += support

with open("Words/wordle-words-test.json","w+") as words_json:
    json.dump(words, words_json)
