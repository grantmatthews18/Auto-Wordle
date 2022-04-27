# Frameword for the wordle game
# Based off the game from powerlanguage.co.uk now owned by nytimes.com

import random
import json
import game
import copy
import decision_tree as dt
import itertools as it

from constants import *

class Agent():
    def __init__(self,id = 0, words = None, filepath = None, dna = None):
        self.id = id
        #dict contaiing all possible guesses
        if(words == None):
            if(filepath == None):
                raise Exception("Word list and filepath empty for Agent: ", self.id, ". Terminating Agent.")
            else:
                with open(filepath) as words_json:
                    self._words = json.load(words_json)
        else:
            self._words = words

        self._word_len = len(next(iter(self._words)))

        if(dna == None):
            print("No DNA given for Agent: ", self.id, ". Proceeding with default DNA.")
            self._dna = [1] * (self._word_len-1)
        elif not (len(dna) == (self._word_len-1)):
            print("DNA given for Agent: ", self.id, " is the wrong length. Proceeding with default DNA.")
            self._dna = [1] * (self._word_len-1)
        else:
            self._dna = dna

        for word in self._words.keys():
            for i in range(len(self._words[word])):
                self._words[word][i] = float(self._words[word][i]/self._dna[i])

        self._words_letters = copy.deepcopy(self._words)
        #removing all words that contain duplicate letters, since this list is all about removing as many letters as possible from the board
        for word in list(self._words_letters):
            for char in word:
                if word.count(char) > 1:
                    self._words_letters.pop(word)
                    break
        self._possible_letters = copy.deepcopy(POSSIBLE_LETTERS_DICT_TRUE)

        self._num_guesses = 0
        self._max_guesses = 0

        self._guesses = []
        self._results = []
        self._possible_result_arrays = copy.deepcopy(POSSIBLE_RESULT_ARRAY)

    def _evaluate_decision_tree(self, head, depth, words, words_letters, possible_letters):
        if(depth <= self._max_guesses):

            #word based guess
            head.add_node()
            new_head = head.get_node(0)
            new_head.set_cost("win")

            #Checking that a word guess is still possible
            #there are no more possible guesses, set node to lose and return, there are no more possible words
            if(len(words) == 0):
                head.set_cost("lose")
                return
            #else check word guess
            else:
                word_guess = self._get_guess_from_words(words)
                word_guess_arr = [char for char in word_guess]
                for x in range(pow(3,self._word_len)):
                    #get array of all possible results of guess
                    result_arr = POSSIBLE_RESULT_ARRAY[x]

                    #copy the current lists so we can modify them without affecting main game
                    words_cpy = copy.deepcopy(words)
                    words_letters_cpy = copy.deepcopy(words_letters)
                    possible_letters_cpy = copy.deepcopy(possible_letters)

                    #possible remaining letters modification
                    for letter in word_guess_arr:
                        possible_letters_cpy[letter] = False

                    #rule out words in both lists
                    for word in list(words_cpy):
                        if(self._rule_out_wordbased(word_guess_arr, result_arr, word)):
                            words_cpy.pop(word)

                    for word in list(words_letters_cpy):
                        if(self._rule_out_letterbased(word, possible_letters)):
                            words_letters_cpy.pop(word)

                    if(len(words_cpy) == 0):
                        #Not a possible result array, skip it
                        None
                    elif(len(words_cpy)+1 <= (self._max_guesses - depth)):
                        #Result array is possible AND guarenteed to win
                        #Skip exploring because game doesn't want us to win
                        None
                    else:
                        #Result array is possible but not guarenteed to win
                        new_head.set_cost("lose")
                        new_head.add_node()

                        #testing all children if we still have guesses left
                        if(depth < self._max_guesses):
                            self._evaluate_decision_tree(new_head.get_node(new_head.num_nodes()-1), depth+1, words_cpy, words_letters_cpy, possible_letters_cpy)
                            #if this node is a win, it will not be choosen but current node needs to be set back to a win
                            if(new_head.get_node(new_head.num_nodes()-1) == "win"):
                                new_head.set_cost("win")
                        #else this node is a loss, so the game will choose it. We can safely break and ignore all other paths
                        else:
                            break

            #check if word based guess is a win. If it is, we can set head node to win, since we will always choose the guarenteed win strategy
            if(head.get_node(0).get_cost() == "win"):
                head.add_to_best_path("word")
                head.set_cost("win")
                return

            #letter based guess (if needed)
            head.add_node()
            new_head = head.get_node(1)
            new_head.set_cost("win")

            #Checking that a letter guess is still possible
            #there are no more possible guesses, set node to lose and move on
            if(len(words_letters) == 0):
                new_head.set_cost("lose")
            #else check the guess
            else:
                letter_guess = self._get_guess_from_words(words_letters)
                letter_guess_arr = [char for char in letter_guess]
                for y in range(pow(3,self._word_len)):
                    #get array of all possible results of guess
                    result_arr = POSSIBLE_RESULT_ARRAY[y]

                    #copy the current lists so we can modify them without affecting main game
                    words_cpy = copy.deepcopy(words)
                    words_letters_cpy = copy.deepcopy(words_letters)
                    possible_letters_cpy = copy.deepcopy(possible_letters)

                    #possible remaining letters modification
                    for letter in letter_guess_arr:
                        possible_letters_cpy[letter] = False

                    #rule out words in both lists
                    for word in list(words_cpy):
                        if(self._rule_out_wordbased(letter_guess_arr, result_arr, word)):
                            words_cpy.pop(word)

                    for word in list(words_letters_cpy):
                        if(self._rule_out_letterbased(word, possible_letters)):
                            words_letters_cpy.pop(word)


                    if(len(words_cpy) == 0):
                        #Not a possible result array, skip it
                        None
                    elif(len(words_cpy)+1 <= (self._max_guesses - depth)):
                        #Result array is possible AND guarenteed to win
                        #Skip exploring because game doesn't want us to win
                        None
                    else:
                        #Result array is possible but not guarenteed to win
                        new_head.set_cost("lose")
                        new_head.add_node()

                        #testing all children if we still have guesses left
                        if(depth < self._max_guesses):
                            self._evaluate_decision_tree(new_head.get_node(new_head.num_nodes()-1), depth+1, words_cpy, words_letters_cpy, possible_letters_cpy)
                            #if this node is a win, it will not be choosen but current node needs to be set back to a win
                            if(new_head.get_node(new_head.num_nodes()-1) == "win"):
                                new_head.set_cost("win")
                        #else this node is a loss, so the game will choose it. We can safely break and ignore all other paths
                        else:
                            break

            #check if letter based guess is a win. If it is, we can set head node to win, since we will always choose the guarenteed win strategy
            if(head.get_node(1).get_cost() == "win"):
                head.add_to_best_path("letter")
                head.set_cost("win")
            #else neither strategy guarentees a win, so node is set to lose
            else:
                head.set_cost("lose")

            return

    def _get_guess_from_words(self, words):
        best_words = []
        max_count = -1
        for word in words.keys():
            count = 0
            for i in range(len(words[word])):
                count += words[word][i]
            if(count > max_count):
                best_words = [(word, count)]
            elif(count == max_count):
                best_words.append((word, count))

        #handling multiple words with the same cost
        #currently, just picking the first one
        #considering adding a tiebreaker based on popularity but the data for that is $200
        # if(len(best_words) > 1):
        best_word = best_words[0][0]
        return(best_word)

    def _get_guess(self):

        #checking if it is the first guess, we have no info at this point and we know it is possible to lose to there is no point in evaluating the tree
        if(self._num_guesses > 1):
            tree = dt.Node()
            self._evaluate_decision_tree(tree, self._num_guesses, self._words, self._words_letters, self._possible_letters)

            #if least optimal path still guarentees win, we use the word guessing strategy
            if(tree.get_cost() == "win"):
                best_word = self._get_guess_from_words(self._words)
                return(best_word)
            elif(tree.get_cost() == "lose"):
                #check to confirm it is still possible to make a word guess
                if(len(self._words_letters) == 0):
                    best_word = self._get_guess_from_words(self._words)
                else:
                    best_word = self._get_guess_from_words(self._words_letters)
                return(best_word)
        #for first guess we just use all possible words
        elif(self._num_guesses == 1):
            best_word = self._get_guess_from_words(self._words_letters)
            return(best_word)
        elif(self._num_guesses == 0):
            best_word = self._get_guess_from_words(self._words)
            return(best_word)
        else:
            raise Exeception("Agent's number of guesses is negative.")


    def _rule_out_wordbased(self, guess_arr, result_arr, word):
        word_arr = [char for char in word]
        for i in range(len(result_arr)):
            if(result_arr[i] == "g"):
                if(word[i] != guess_arr[i]):
                    return(True)
            elif(result_arr[i] == "y"):
                if(word[i] == guess_arr[i]):
                    return(True)
                elif not (guess_arr[i] in word):
                    return(True)
            elif(result_arr[i] == "e"):
                if(guess_arr.count(guess_arr[i]) > 1): #if guess_arr[i] in guess_arr more then once
                    if(guess_arr.count(guess_arr[i]) <= word_arr.count(guess_arr[i])): #if guess has less or the same number of guess_arr[i] as word
                        return(True)
                    else: #else check every letter in guess_arr, if another guess_arr[i] is y or g keep word.
                        not_e_ct = 0
                        for ii in range(len(guess_arr)):
                            if (guess_arr[i] == guess_arr[ii]) and (result_arr[ii] == "g" or result_arr[ii] == "y"):
                                not_e_ct += 1
                        if(word_arr.count(guess_arr[i]) != not_e_ct):
                            return(True)
                else: #if guess_arr[i] in guess_arr once
                    if(guess_arr[i] in word):
                        return(True)
        return(False)

    def _rule_out_letterbased(self, word, possible_letters):
        #leaves only words possible with remaining unguessed letters
        for letter in list(possible_letters):
            if(possible_letters[letter] == False):
                if letter in word:
                    return(True)
        return(False)

    def _calculate_frequency(self, words_dict):
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
        for word in words_dict.keys():
            words_itemsets[word] = []
            word_arr = [char for char in word]
            word_2arr = []
            for i in range(len(word_arr)):
                #split word
                word_arr[i] = word_arr[i]+str(i)

            #add itemsets to master itemsets list
            for i in range(len(word_arr)):
                #single letter itemsets
                if((word_arr[i],) in itemsets):
                    itemsets[(word_arr[i],)] += 1
                else:
                    itemsets[(word_arr[i],)] = 1
                words_itemsets[word].append((word_arr[i],))

                #2 letter itemsets
                if(i < len(word_arr)-1):
                    itemset2 = (word_arr[i], word_arr[i+1])
                    if(itemset2 in itemsets):
                        itemsets[itemset2] += 1
                    else:
                        itemsets[itemset2] = 1
                    words_itemsets[word].append(itemset2)

                #3 letter itemsets
                if(i < len(word_arr)-2):
                    itemset3 = (word_arr[i], word_arr[i+1], word_arr[i+2])
                    if(itemset3 in itemsets):
                        itemsets[itemset3] += 1
                    else:
                        itemsets[itemset3] = 1
                    words_itemsets[word].append(itemset3)

                #4 letter itemsets
                if(i < len(word_arr)-3):
                    itemset4 = (word_arr[i], word_arr[i+1], word_arr[i+2], word_arr[i+3])
                    if(itemset4 in itemsets):
                        itemsets[itemset4] += 1
                    else:
                        itemsets[itemset4] = 1
                    words_itemsets[word].append(itemset4)

        for word in words_itemsets.keys():
            words_dict[word] = [0] * (len(word)-1)
            for itemset in words_itemsets[word]:
                support = itemsets[itemset]
                words_dict[word][len(itemset)-1] += support

        return(words_dict)

    def _modify_word_lists(self, guess, guess_arr, result):
        #remove guess from both word sets
        if(guess in self._words):
            self._words.pop(guess)
        if (guess in self._words_letters.keys()):
            self._words_letters.pop(guess)

        #remove all letters in current guess from possible letters
        for letter in guess_arr:
            self._possible_letters[letter] = False

        #remove all words from words that do not match the info given by the result of the guess
        #mark all letters that could still possibly be in the final word
        letters_in_words = copy.deepcopy(POSSIBLE_LETTERS_DICT_FALSE)
        for word in list(self._words):
            if(self._rule_out_wordbased(guess_arr, result, word)):
                self._words.pop(word)
            else:
                for i in range(len(word)):
                    letters_in_words[word[i]] = True

        for letter in list(letters_in_words):
            if(letters_in_words[letter]==False):
                self._possible_letters[letter] = False

        #remove all words from words_letters that have the guessed letters
        for word in list(self._words_letters):
            if(self._rule_out_letterbased(word, self._possible_letters)):
                self._words_letters.pop(word)



    def solve_game(self, game):
        self._num_guesses = 0
        self._max_guesses = game.get_max_guesses()
        while not game.game_over:
            self._guesses.append(self._get_guess())
            guess_arr = [char for char in self._guesses[self._num_guesses]]
            self._results.append(game.make_guess(self._guesses[self._num_guesses]))

            self._modify_word_lists(self._guesses[self._num_guesses], guess_arr, self._results[self._num_guesses])
            self._num_guesses += 1
        game.end_game()
        return(self._num_guesses)
