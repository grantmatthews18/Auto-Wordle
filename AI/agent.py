# Frameword for the wordle game
# Based off the game from powerlanguage.co.uk now owned by nytimes.com

import random
import json
import game
import copy

class Agent():
    def __init__(self, words = None, filepath = None, letter_weight = None, simularity_modifier = None, double_penalty = None):
        #dict containig all possible guesses
        if(words == None):
            with open(filepath) as words_json:
                self._words = json.load(words_json)
        else:
            self._words = words
        #dict, all values between 0-1
        self._letter_weight = letter_weight
        #array of floats between 0-1 len(word)
        self._simularity_modifier = simularity_modifier
        #array of floats between 0-1 len(word)-2 (for 2 letter, 3 letter and 4 letter pattern matches in the case of 5 letter words)
        self._double_penalty = double_penalty

        for word in self._words.keys():
            weight = 0
            for i in range(len(word)):
                weight += self._letter_weight[word[i]]

            for i in range(len(word)):
                weight += self._words[word][i+1] * self._simularity_modifier[i]

            for i in range(len(word)-2):
                weight += self._words[word][i+len(word)] * self._double_penalty[i]

            self._words[word] = weight

    def _rule_out(self, guess_arr, result_arr, word):
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


    def solve_game(self, game):
        num_guesses = 0
        while not game.game_over:
            guess = max(self._words, key=self._words.get)
            guess_arr = [char for char in guess]
            result = game.make_guess(guess)

            self._words.pop(guess)

            for word in list(self._words):
                if(self._rule_out(guess_arr, result, word)):
                    self._words.pop(word)
            num_guesses += 1
        game.end_game()
        return(num_guesses)
