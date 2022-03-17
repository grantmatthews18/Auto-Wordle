# Frameword for the wordle game
# Based off the game from powerlanguage.co.uk now owned by nytimes.com

import random
import json

class game():
    def __init__(self, word, num_guesses):
        self.word = word
        self.num_guesses = num_guesses

    def guess(self, guess):
        # return something to indicate guess
        return()


def classic():
    filepath = "words/words-5.json"
    with open(filepath) as words_json:
        words = json.load(words_json)
        word = random.choice(list(words.keys()))
        print(word)
    return(game(word, 6))


def main():
    print("Select Mode: \nClassic Wordle - 1\nRandom Wordle - 2\nSet Parameters - 3")
    mode = int(input("Input:"))
    if(mode == 1):
        game = classic()
        print(game.word)
        print(game.num_guesses)
    elif(mode == 2):
        print("Not implemented yet")
    elif(mode == 3):
        print("Not implemented yet")
    else:
        print("bad selection, reselect not implemented yet")




if __name__ == '__main__':
    main()
