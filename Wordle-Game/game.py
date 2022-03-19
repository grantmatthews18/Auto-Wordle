import tkinter as tk
import tkinter.ttk as ttk
import json
import time
import copy
#from functools import partial

class Game():
    def __init__(self, word, num_guesses, gui_flag = True, keyboard_flag = True, verbose_flag = False, enable_debug = False):
        self._word = word.lower()
        self._word_arr = [char for char in self._word]
        self._word_len = len(word)
        self._guesses_arr = []
        self._guesses_arr_len = len(self._guesses_arr)
        self._num_guesses = num_guesses

        self.game_over = False

        filepath = "words/words-" + str(self._word_len) + ".json"
        with open(filepath) as words_json:
            self._words = json.load(words_json)

        #gui flags
        #gui has to be enabled to enable keyboard
        #gui can run without keyboard
        self._enable_gui = gui_flag
        self._enable_keyboard = keyboard_flag
        if not(self._enable_gui):
            self._enable_keyboard = False

        #verbose flags
        self._enable_verbose = verbose_flag

        #debug flag
        self._enable_debug = enable_debug

    def _set_gui(self):

        self._gui = tk.Tk()

        window_width = 5 + (105*self._word_len)
        window_height = 250 + (105*self._num_guesses)
        str_window_size = str(window_width) + "x" + str(window_height)

        self._gui.title("Classic Mode")
        self._gui.geometry(str_window_size)
        self._gui.minsize(window_width,window_height)
        self._gui.maxsize(window_width,window_height)

        title_banner = tk.Label(self._gui, text = "Classic Mode", font = ("Arial", 25)).place(relx=.5, y=33, anchor=tk.CENTER)
        info_banner = tk.Label(self._gui, text = "Type Your Guess in the box below to begin").place(relx=.5, y=66, anchor=tk.CENTER)

        self._gui_letters = []
        self._gui_frames = []

        for ypos in range(self._num_guesses):
            self._gui_letters.append([])
            self._gui_frames.append([])
            for xpos in range(self._word_len):
                self._gui_frames[ypos].append(tk.Frame(self._gui, borderwidth=1, relief="solid", width=100, height=100))
                self._gui_frames[ypos][xpos].place(x=5+(xpos*105), y=100+(ypos*105))
                self._gui_letters[ypos].append(tk.Label(self._gui_frames[ypos][xpos], text="", font = ("Arial", 50)))
                self._gui_letters[ypos][xpos].place(relx = .5, rely=.5, anchor=tk.CENTER)

        if(self._enable_keyboard):

            self._keyboard = tk.Tk()
            self._keyboard.title("Keyboard")

        guess_var = tk.StringVar()
        self._gui_guess_entry = tk.Entry(self._gui, textvariable = guess_var, font = ("Arial", 25))
        self._gui_guess_entry.place(relx=.5, y=window_height-100, anchor=tk.CENTER)
        self._gui_guess_button = tk.Button(self._gui, text = "Guess", command=self.make_guess)
        self._gui_guess_button.place(relx=.5, y = window_height-50, anchor=tk.CENTER)
        self._gui.bind('<Return>', self._event_enter_gui)

        self._gui_error_label = tk.Label(self._gui, text="")
        self._gui_error_label.place(relx=.5, y = window_height-25, anchor=tk.CENTER)


    def start_game(self):
        if(self._enable_debug):
            print("Word is: - ", self._word.upper(), " -")
        if(self._enable_verbose):
            print("+---+---+---+---+---+")
            print("|", "h"+"\u0332", "| E | L | l |", "o"+"\u0332", "|")
            print("+---+---+---+---+---+")
            print("Lower case letters like l are not in the word")
            print("Lower case letters underlined like", "h"+"\u0332", "and", "o"+"\u0332", "are in the word but not in the correct position")
            print("Upper case letters like E and L are in the word and in the correct position")
            print("Game Begining...")
        if(self._enable_gui):
            self._set_gui()
            self._gui.mainloop()

    def end_game(self):
        self._gui.destroy()

    def _event_enter_gui(self, event):
        self.make_guess()

    def make_guess(self, guess=None):

        # Set Guess to the string in the guess entry box
        if (guess == None):
            guess = self._gui_guess_entry.get()
            self._gui_guess_entry.delete(0,tk.END)

        guess = guess.lower() #need to lowercase to compare with words list

        if(not guess in self._words):
            if(self._enable_gui):
                self._gui_error_label.config(text = "Not a Valid Word, Try Again")
            if(self._enable_verbose):
                print("- ", guess.upper(), "- Not a Valid Word, Try Again")
            return
        else:
            if(self._enable_gui):
                self._gui_error_label.config(text = "")
            if(self._enable_verbose):
                temp = None
                #do something verbose if needed

        if(len(guess) != self._word_len):
            if(self._enable_gui):
                self._gui_error_label.config(text = "Not the Correct Word Length, Try Again")
            if(self._enable_verbose):
                print("- ", guess.upper(), "- Not the Correct Word Length, Try Again")
            return
        else:
            if(self._enable_gui):
                self._gui_error_label.config(text = "")
            if(self._enable_verbose):
                temp = None
                #do something verbose if needed

        guess_arr = [char for char in guess]
        temp_word_arr = copy.deepcopy(self._word_arr)

        self._guesses_arr.append([])
        self._guesses_arr_len = len(self._guesses_arr)

        print(temp_word_arr)

        for i in range(self._word_len):
            self._guesses_arr[self._guesses_arr_len-1].append("e")
            if (guess_arr[i] == temp_word_arr[i]):
                self._guesses_arr[self._guesses_arr_len-1][i] = "g"
                temp_word_arr[i] = None

        for i in range(self._word_len):
            if (guess_arr[i] in temp_word_arr):
                if not(self._guesses_arr[self._guesses_arr_len-1][i] == "g"):
                    self._guesses_arr[self._guesses_arr_len-1][i] = "y"
                    temp_word_arr[temp_word_arr.index(guess[i])] = None

        print(temp_word_arr)
        print(self._guesses_arr[self._guesses_arr_len-1])

        #loop to print each letter
        i = 0
        for i in range(self._word_len):
            #Adding line to board
            #green or perfect placement
            if (self._guesses_arr[self._guesses_arr_len-1][i] == "g"):
                if(self._enable_gui):
                    self._gui_frames[self._guesses_arr_len-1][i].config(background="green")
                    self._gui_letters[self._guesses_arr_len-1][i].config(text = guess_arr[i].upper())
                    self._gui_letters[self._guesses_arr_len-1][i].config(background="green")
                #do something verbose

            #yellow, or letter in word but wrong spot
            elif (self._guesses_arr[self._guesses_arr_len-1][i] == "y"):
                if(self._enable_gui):
                    self._gui_frames[self._guesses_arr_len-1][i].config(background="yellow")
                    self._gui_letters[self._guesses_arr_len-1][i].config(text = guess_arr[i].upper())
                    self._gui_letters[self._guesses_arr_len-1][i].config(background="yellow")
                #do something verbose
            else:
                if(self._enable_gui):
                    self._gui_letters[self._guesses_arr_len-1][i].config(text = guess_arr[i].upper())
                #do something verbose
            i += 1


        #end game conditions
        #game won
        if(guess == self._word):
            if(self._enable_gui):
                self._gui_guess_entry.config(state='disable')
                self._gui_guess_button.config(state='disable')
                self._gui_error_label.config(text = "Congratulations! You Win!")
            #do something verbose
            self.game_over = True

        #max guess reached, game lost
        elif(len(self._guesses_arr) == self._num_guesses):
            if(self._enable_gui):
                self._gui_guess_entry.config(state='disable')
                self._gui_guess_button.config(state='disable')
                self._gui_error_label.config(text = "Game Over")
            if(self._enable_verbose):
                print("Game Over. Maximum Guess Reached.")
                print("Word was - ", self._word.upper(), " -")
            self.game_over = True

        return()
