import random
import json
import tkinter as tk
import tkinter.ttk as ttk
import sys
import copy

sys.path.insert(1, "Wordle-Game/")
from game import *
import agent as ai

def main():
    filepath = "Words/wordle-words.json"
    with open(filepath) as words_json:
        words = json.load(words_json)

    total_guesses = 0

    for word in range(1): #list(words.keys())
        word = "bauks"#random.choice(list(words.keys()))
        print("Word is ", word)

        new_agent = ai.Agent(filepath=filepath)
        args = [word, 6, False, False, False, True]
        new_game = Game(*args)

        result = new_agent.solve_game(new_game)
        total_guesses += result
        print("Result is ", result)
    print(total_guesses/len(words.keys()))

if __name__ == '__main__':
    main()
