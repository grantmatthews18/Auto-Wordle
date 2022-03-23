# Frameword for the wordle game
# Based off the game from powerlanguage.co.uk now owned by nytimes.com

import random
import json
import game
import copy

class Agent():
    def __init__(self, words = None, letter_weight = None, simularity_modifier = None, double_penalty = None):
        #dict containig all possible guesses
        self._words = words
        #dict, all values between 0-1
        self._letter_weight = letter_weight
        #array of floats between 0-1 len(word)
        self._simularity_modifier = simularity_modifier
        #array of floats between 0-1 len(word)-2 (for 2 letter, 3 letter and 4 letter pattern matches in the case of 5 letter words)
        self._double_penalty = double_penalty

        for word in words.keys():
            weight = 0
            for i in range(len(word)):
                weight += self._letter_weight[word[i]]

            for i in range(len(word)):
                weight += words[word][i+1] * self._simularity_modifier[i]

            for i in range(len(word)-2):
                weight += words[word][i+len(word)] * self._double_penalty[i]

            words[word] = weight

    def solve_game(self, game):
        num_guesses = 0
        while not game.game_over:
            guess = max(self._words, key=self._words.get)
            guess_arr = [char for char in guess]
            guess_result = game.make_guess(guess)

            self._words.pop(guess)

            for i in range(len(guess_result)):
                if(guess_result[i] == "g"):
                    for word in list(self._words):
                        if(guess[i] != word[i]):
                            self._words.pop(word)
                elif(guess_result[i] == "y"):
                    for word in list(self._words):
                        if (guess_arr[i] == word[i]):
                            self._words.pop(word)
                        elif not (guess[i] in word):
                            self._words.pop(word)
                elif(guess_result[i] == "e"):
                    for word in list(self._words):
                        #if the grey letter is in the same spot in the current word
                        if (guess_arr[i] == word[i]):
                            self._words.pop(word)
                        #else if the letter is in the word but not the same spot
                        elif(guess_arr[i] in word):
                            pop = True
                            for x in range(len(guess_arr)):
                                if(x != i):
                                    if (guess_arr[x] == guess_arr[i]) and ((guess_result[i] == "g") or (guess_result[i] == "y")):
                                        pop = False
                            if(pop):
                                self._words.pop(word)


            num_guesses += 1
        game.end_game()
        return(num_guesses)
