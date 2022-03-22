# Frameword for the wordle game
# Based off the game from powerlanguage.co.uk now owned by nytimes.com

import random
import json
import game

class Agent():
    def __init__(self, letter_composition = None, double_penalty = 0, simularity_modifier = 0, word_popularity = 0):
        
