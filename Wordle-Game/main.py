# Frameword for the wordle game
# Based off the game from powerlanguage.co.uk now owned by nytimes.com

import random
import json
import tkinter as tk
import tkinter.ttk as ttk

from game import *

def classic():

    #finding word
    filepath = "Words/wordle-words.json"
    with open(filepath) as words_json:
        words = json.load(words_json)
        word = random.choice(list(words.keys()))

    game = Game(word, 6, True, True, True);
    game.start_game()


def main():
    gui = tk.Tk()
    gui.title("Auto-Wordle")
    gui.geometry("600x200")
    gui.minsize(600,200)
    gui.maxsize(600,200)

    title_banner = tk.Label(gui, text = "Welcome to Auto Wordle", font = ("Arial", 25)).place(x=115, y=25)
    info_banner = tk.Label(gui, text = "To begin, please select an option below. For more information, select help.").place(x=100, y=75)

    classic_button = tk.Button(gui, text = "Classic Mode", command = classic).place(bordermode=tk.OUTSIDE, height=50, width=100, x=25, y=100)
    random_button = tk.Button(gui, text = "Random Mode").place(bordermode=tk.OUTSIDE, height=50, width=100, x=150, y=100)
    Custom_button = tk.Button(gui, text = "Custom Mode").place(bordermode=tk.OUTSIDE, height=50, width=100, x=275, y=100)

    help_button = tk.Button(gui, text = "Help").place(bordermode=tk.OUTSIDE, height=25, width=50, x=275, y=175)

    gui.mainloop()

def main2():
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
