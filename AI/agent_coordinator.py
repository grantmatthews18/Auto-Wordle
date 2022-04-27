#Agent coordinator class. Each agent coordinator represents a population

import json
import copy

#may or may not need these
#game gui currently somewhat broken and imcomplete. Not needed for ai agents
import tkinter as tk
import tkinter.ttk as ttk


import threading

#adds a system path for the game folder so we can import the game file
import sys
sys.path.insert(1, "Wordle-Game/")
from game
import agent as ai

#Constants
from constants import *

class Agent_Coordinator():
    def __init__(self, id = 0, test_cases_filepath = None, all_words_filepath = None, game_parameters = None, num_threads = 1, num_agents = 1):

        #population/generation id
        self.id = id

        if(test_cases_filepath = None):
            throw Exception("No Test Case List filepath given. Aborting.")
        else:
            with open(test_cases_filepath) as test_cases_json:
                self._test_cases = json.load(test_cases_json)

        if(all_words_filepath = None):
            throw Exception("No Words List filepath given. Aborting.")
        else:
            with open(all_words_filepath) as words_json:
                self._words = json.load(words_json)

        if not (len(next(iter(self._test_cases))) == len(next(iter(self._words)))):
            throw Exception("Words in Test Cases and Word List are different lengths. Aborting.")
        else:
            self._word_len = len(next(iter(self._test_cases)))

        #check to make sure game settings are the right length
        #current number of parameters is stored in constants
        if not (len(game_parameters) == NUMBER_OF_GAME_PARAMETERS):
            throw Exception("Wrong Number of Game Parameters. Aborting.")
        else:
            self._game_parameters = game_parameters

        if(dna == None):
            throw Exception("No DNA given for Agent Coordi: ", self.id, ". Aborting.")
        elif not (len(dna) == (self._word_len-1)):
            throw Exception("DNA given for Agent: ", self.id, " is the wrong length. Aborting.")
        else:
            self._dna = dna

        #set number of threads to be run
        self._num_threads = num_threads

        #number of agents in this population
        self._num_agents = num_agents

        self._results = {}

    def run_generation(self):
        #TODO: Implement threading to run the set up agent coordinator
        None

    def run_agent(self, agent_id = 0, agent_dna = None):
        #make sure agent's dna is valid
        if(agent_dna == None):
            throw Exception("No DNA given for Agent Coordi: ", self.id, ". Aborting.")
        elif not (len(agent_dna) == (self._word_len-1)):
            throw Exception("DNA given for Agent: ", self.id, " is the wrong length. Aborting.")

        #make agent
        agent = ai.Agent(id=agent_id, words=copy.deepcopy(self._words), dna=agent_dna)

        #dict to hold results for each of the test cases
        agent_results = {}

        for word in self._test_cases.keys():
            new_game = game.Game(*self._game_parameters)
            game_result = agent.solve_game(new_game)
            agent_results[word] = game_result
