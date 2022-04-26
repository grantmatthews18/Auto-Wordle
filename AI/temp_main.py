import random
import json
import tkinter as tk
import tkinter.ttk as ttk
import sys
import copy

sys.path.insert(1, "Wordle-Game/")
from game import *
import agent as ai

keys = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]

def main():
    filepath = "Words/wordle-words.json"
    with open(filepath) as words_json:
        words = json.load(words_json)

    total_guesses = 0

    for word in list(words.keys()):
        #word = random.choice(list(words.keys()))
        print("Word is ", word)

        letter_weight = {}
        for i in range(len(keys)):
            letter_weight[keys[i]] = 1

        simularity_modifier = []
        for i in range(len(word)):
            simularity_modifier.append(1)

        double_penalty = []
        for i in range(len(word)-2):
            double_penalty.append(1)

        new_agent = ai.Agent(filepath=filepath)
        new_game = Game(word, 6, debug_flag =True)

        result = new_agent.solve_game(new_game)
        total_guesses += result
        print("Result is ", result)
    print(total_guesses/len(words.keys()))

if __name__ == '__main__':
    main()
