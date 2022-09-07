import random
import json
import tkinter as tk
import tkinter.ttk as ttk
import sys
import copy

sys.path.insert(1, "Wordle-Game/")
from game import *
import mod_agent as ai
import agent_coordinator as ai_coordinator

def main():

    words_filepath = "Words/wordle-words.json"
    test_cases_filepath = "Words/wordle-202-300-nyt.json"
    game_args = [6, False, False, False, False]
    generation1 = ai_coordinator.Agent_Coordinator(1, test_cases_filepath, words_filepath, game_args, 1)

    dna_array =[]

    possible_dna_elements = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    for i in range(1):
        dna = []
        for z in range(4):
            dna.append(random.choice(possible_dna_elements))
        dna_array.append(dna)

    with open("Words/dna_202-300-exp2.json", "w+") as dna_json:
        json.dump(dna_array,dna_json)

    gen = 1
    results = generation1.run_generation(gen, dna_array)

    with open("Words/results_202-300-exp2.json", "w+") as results_json:
        json.dump(results, results_json)


    # filepath = "Words/wordle-words.json"
    # with open(filepath) as words_json:
    #     words = json.load(words_json)
    #
    # total_guesses = 0
    #
    # for word in range(1): #list(words.keys())
    #     word = "bauks"#random.choice(list(words.keys()))
    #     print("Word is ", word)
    #
    #     new_agent = ai.Agent(filepath=filepath)
    #     args = [word, 6, False, False, False, True]
    #     new_game = Game(*args)
    #
    #     result = new_agent.solve_game(new_game)
    #     total_guesses += result
    #     print("Result is ", result)
    # print(total_guesses/len(words.keys()))

if __name__ == '__main__':
    main()
