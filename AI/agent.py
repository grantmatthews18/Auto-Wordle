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

        self._words_letters = copy.deepcopy(self._words)
        #removing all words that contain duplicate letters, since this list is all about removing as many letters as possible from the board
        for word in list(self._words_letters):
            for char in word:
                if word.count(char) > 1:
                    self._words_letters.pop(word)
                    break

        #setting initial costs for each game
        self._update_costs(self._words, self._words_letters)

        self._num_guesses = 0
        self._max_guesses = 0


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

    def _get_guess(self, words, words_letters, possible_letters):

        #checking if it is the first guess, we have no info at this point and we know it is possible to lose to there is no point in evaluating the tree
        if(self._num_guesses > 1):
            tree = dt.Node()
            self._evaluate_decision_tree(tree, self._num_guesses, words, words_letters, possible_letters)

            #if least optimal path still guarentees win, we use the word guessing strategy
            if(tree.get_cost() == "win"):
                best_word = self._get_guess_from_words(words)
                return(best_word)
            elif(tree.get_cost() == "lose"):
                #check to confirm it is still possible to make a word guess
                if(len(words_letters) == 0):
                    best_word = self._get_guess_from_words(words)
                else:
                    best_word = self._get_guess_from_words(words_letters)
                return(best_word)

        #for second guess we use letters, if possible
        elif(self._num_guesses == 1):
            if(len(words_letters) > 0):
                best_word = self._get_guess_from_words(words_letters)
            else:
                best_word = self._get_guess_from_words(words)
            return(best_word)
        #for first guess we just use all possible words
        elif(self._num_guesses == 0):
            best_word = self._get_guess_from_words(words)
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

    def _update_costs(self, words, words_letters):
        #Key is the string word and value is list of itemset tuples
        words_itemsets = {}

        #used to store the frequency values of all possible itemsets in words
        itemsets = {}

        ##Key is the string word and value is list of itemset tuples
        #this is for words_letters. These itemsets are not neccisarily present in itemsets
        #we deal with this later
        words_letters_itemsets = {}

        #splitting words
        #AND
        #calculating frequency of itemsets
        #AND
        #merging
        #doing all at once to save CPU cycles

        #creating itemsets for all words in wirds
        for word in words.keys():
            words_itemsets[word] = []
            #split word, add letter position to letter
            word_arr = []
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

        #creating itemsets for all words in words_letter
        for word in words_letters.keys():
            words_letters_itemsets[word] = []
            #split word, add letter position to letter
            word_arr = []
            pos = 0
            for char in word:
                word_arr.append(char+str(pos))
                pos +=1

            #add all possible itemsets to word_letters_itemsets
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
                    #add itemset to list of itemsets for the word
                    words_letters_itemsets[word].append(itemset)

        #updating words support counts and costs
        for word in words.keys():
            words[word] = [0] * (len(word)-1)
            for itemset in words_itemsets[word]:
                support = itemsets[itemset]
                words[word][len(itemset)-1] += support
            #modifying support values according to agent dna
            for i in range(len(words[word])):
                words[word][i] = float(words[word][i]/(self._dna[i]/pow(10,i)))

        #updaing words_letters support counts based on support from words
        for word in words_letters.keys():
            words_letters[word] = [0] * (len(word)-1)
            for itemset in words_letters_itemsets[word]:
                #checks if the itemset is in the master list
                #master list developed based on words itemsets, so its possible it is not
                #if its not there the support for that itemset is 0
                if(itemset in itemsets):
                    support = itemsets[itemset]
                else:
                    support = 0
                words_letters[word][len(itemset)-1] += support
            #modifying support values according to agent dna
            for i in range(len(words_letters[word])):
                words_letters[word][i] = float(words_letters[word][i]/(self._dna[i]/pow(10,i)))

    def _modify_word_lists(self, guess, guess_arr, result, words, words_letters, possible_letters):
        #remove guess from both word sets
        if(guess in words):
            words.pop(guess)
        if (guess in words_letters.keys()):
            words_letters.pop(guess)

        #remove all letters in current guess from possible letters
        for letter in guess_arr:
            possible_letters[letter] = False

        #remove all words from words that do not match the info given by the result of the guess
        #mark all letters that could still possibly be in the final word
        letters_in_words = copy.deepcopy(POSSIBLE_LETTERS_DICT_FALSE)
        for word in list(words):
            if(self._rule_out_wordbased(guess_arr, result, word)):
                words.pop(word)
            else:
                for i in range(len(word)):
                    letters_in_words[word[i]] = True

        for letter in list(letters_in_words):
            if(letters_in_words[letter]==False):
                possible_letters[letter] = False

        #remove all words from words_letters that have the guessed letters
        for word in list(words_letters):
            if(self._rule_out_letterbased(word, possible_letters)):
                words_letters.pop(word)

        #update support counts and recalculate word value
        self._update_costs(words, words_letters)

    def solve_game(self, game):
        #copy word lists to preserve them for future computation
        game_words = copy.deepcopy(self._words)
        game_words_letters = copy.deepcopy(self._words_letters)
        possible_letters = copy.deepcopy(POSSIBLE_LETTERS_DICT_TRUE)

        #set globals to proper values
        self._num_guesses = 0
        self._max_guesses = game.get_max_guesses()

        guesses = []
        results = []
        while not game.game_over:

            #get guess, add it to guesses
            guess = self._get_guess(game_words, game_words_letters, possible_letters)
            guesses.append(guess)
            guess_arr = [char for char in guess]

            result_arr = game.make_guess(guess)
            results.append(result_arr)

            self._modify_word_lists(guess, guess_arr, result_arr, game_words, game_words_letters, possible_letters)
            self._num_guesses += 1
        game_result = game.end_game()
        return((game_result, self._num_guesses))
