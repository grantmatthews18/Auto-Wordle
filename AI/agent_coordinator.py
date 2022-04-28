#Agent coordinator class. Each agent coordinator represents a population

import json
import copy

#may or may not need these
#game gui currently somewhat broken and imcomplete. Not needed for ai agents
import tkinter as tk
import tkinter.ttk as ttk

import multiprocessing as mp
# import threading

#adds a system path for the game folder so we can import the game file
import sys
sys.path.insert(1, "Wordle-Game/")
import game
import agent as ai

#Constants
from constants import *

#for testing
import time

class Agent_Coordinator():
    def __init__(self, id = 0, test_cases_filepath = None, all_words_filepath = None, game_parameters = None, num_threads = 1):

        #population id
        self.id = id

        if(test_cases_filepath == None):
            raise Exception("No Test Case List filepath given. Aborting.")
        else:
            with open(test_cases_filepath, "r+") as test_cases_json:
                self._test_cases = json.load(test_cases_json)

        if(all_words_filepath == None):
            raise Exception("No Words List filepath given. Aborting.")
        else:
            with open(all_words_filepath) as words_json:
                self._words = json.load(words_json)

        if not (len(next(iter(self._test_cases))) == len(next(iter(self._words)))):
            raise Exception("Words in Test Cases and Word List are different lengths. Aborting.")
        else:
            self._word_len = len(next(iter(self._test_cases)))

        #check to make sure game settings are the right length
        #current number of parameters is stored in constants
        if not (len(game_parameters) == NUMBER_OF_GAME_PARAMETERS):
            raise Exception("Wrong Number of Game Parameters. Aborting.")
        else:
            self._game_parameters = game_parameters

        #set number of threads to be run
        self._num_threads = num_threads

        #dict to hold all results, still not sure how I will implement this
        self._results = {}

    def run_generation(self, generation_id = 1, dna_array = None):
        #check if dna is not empty
        if(dna_array == None):
            raise Exception("No DNA given for Agents. Aborting.")
        elif not (len(dna_array[0]) == self._word_len-1):
            raise Exception("DNA Strands wrong length. Aborting.")

        num_agents = len(dna_array)
        print("Number of Agents Given: ", num_agents)
        print("Number of Threads to be created: ", self._num_threads)

        #make threads
        threads = []
        #lock needed to make sure only one result is written to the result array at a time
        #OR only one copy is being performed at the same time
        thread_lock = mp.Lock()

        q = mp.Queue()

        #create threads
        for i in range(num_agents):
            threads.append(mp.Process(target=self.run_agent, args=(i,dna_array[i],q,thread_lock,)))

        #run threads, only running specified number at a time
        for i in range(num_agents):
            while(len(mp.active_children()) >= self._num_threads):
                #idle until thread finishes
                None
            threads[i].start()

        #join threads
        for i in range(num_agents):
            while(len(mp.active_children()) >= self._num_threads):
                #idle until thread finishes
                None
            threads[i].join()

        #pull generation results from queue
        generation_results = {}
        while not (q.empty()):
            result = q.get()
            generation_results[int(result[0])] = result[1]

        #add generation results to results array
        self._results[generation_id] = generation_results

        return(generation_results)

    def run_agent(self, agent_id = 0, agent_dna = None, q = None, thread_lock = None):
        #make sure agent's dna is valid
        if(agent_dna == None):
            raise Exception("No DNA given for Agent: ", agent_id, ". Aborting.")
        elif not (len(agent_dna) == (self._word_len-1)):
            raise Exception("DNA given for Agent: ", agent_id, " is the wrong length. Aborting.")

        #checking queue is passed properly
        if(q == None):
            raise Exception("Invalid Queue Passed. Aborting.")

        #make sure agent has access to lock
        if(thread_lock == None):
            raise Exception("Invalid Lock Passed. Aborting.")

        thread_lock.acquire()
        #make agent
        agent = ai.Agent(id=agent_id, words=copy.deepcopy(self._words), dna=agent_dna)
        thread_lock.release()

        #dict to hold results for each of the test cases
        agent_results = {}

        for word in self._test_cases.keys():
            #copying game parameters and adding word to front
            thread_lock.acquire()
            game_parameters = copy.deepcopy(self._game_parameters)
            thread_lock.release()
            game_parameters.insert(0, word)
            new_game = game.Game(*game_parameters)
            game_result = agent.solve_game(new_game)
            agent_results[word] = game_result
            thread_lock.acquire()
            print("Agent: ", agent_id, " solved word: ", word)
            thread_lock.release()

        q.put((agent_id, agent_results))
