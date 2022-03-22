import tkinter as tk
import tkinter.ttk as ttk
import json
import time
import copy
#from functools import partial

keys = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]

class Game():
    def __init__(self, word, num_guesses, gui_flag = True, keyboard_flag = True, verbose_flag = False, enable_debug = False):
        self._word = word.lower()
        self._word_arr = [char for char in self._word]
        self._word_len = len(word)
        self._guesses_arr = []
        self._guesses_arr_len = len(self._guesses_arr)
        self._num_guesses = num_guesses

        #array to hold key color values
        self._keys = {}
        for i in range(26):
            self._keys[keys[i]] = "x"

        self.game_over = False

        filepath = "Words/wordle-words.json"
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
        self._verbose_board_str = "+---+---+---+---+---+\n"

        #debug flag
        self._enable_debug = enable_debug

    def _set_gui(self):

        self._gui = tk.Tk()

        window_width = 5 + (105*self._word_len)
        window_height = 5 + (105*self._num_guesses)
        if(self._enable_keyboard):
            button_size = 50
            if(self._word_len <= 5):
                button_size = ((window_width-10)/10) - 5

            window_height = window_height + ((button_size+5)*4) + 30

        window_height = int(window_height)
        str_window_size = str(window_width) + "x" + str(window_height)

        self._gui.title("Classic Mode")
        self._gui.geometry(str_window_size)
        self._gui.minsize(window_width,window_height)
        self._gui.maxsize(window_width,window_height)

        # title_banner = tk.Label(self._gui, text = "Classic Mode", font = ("Arial", 25)).place(relx=.5, y=33, anchor=tk.CENTER)
        # info_banner = tk.Label(self._gui, text = "Type Your Guess in the box below to begin").place(relx=.5, y=66, anchor=tk.CENTER)

        self._gui_letters = []
        self._gui_frames = []

        for ypos in range(self._num_guesses):
            self._gui_letters.append([])
            self._gui_frames.append([])
            for xpos in range(self._word_len):
                self._gui_frames[ypos].append(tk.Frame(self._gui, borderwidth=1, relief="solid", width=100, height=100))
                self._gui_frames[ypos][xpos].place(x=5+(xpos*105), y=5+(ypos*105))
                self._gui_letters[ypos].append(tk.Label(self._gui_frames[ypos][xpos], text="", font = ("Arial", 50)))
                self._gui_letters[ypos][xpos].place(relx = .5, rely=.5, anchor=tk.CENTER)

        if(self._enable_keyboard):
            guess_var = tk.StringVar()
            self._gui_guess_entry = tk.Entry(self._gui, textvariable = guess_var, font = ("Arial", 25))
            self._gui_guess_entry.place(x=5, y=window_height-((button_size+5)*4), height=button_size, width=((button_size+5)*8))
            self._gui_guess_button = tk.Button(self._gui, text = "Guess", command=self.make_guess)
            self._gui_guess_button.place(x=(((button_size+5)*8)+5), y=window_height-((button_size+5)*4), height=button_size, width=((button_size+5)*2))
            self._gui.bind('<Return>', self._event_enter_gui)

            self._gui_error_label = tk.Label(self._gui, text="")
            self._gui_error_label.place(relx=.5, y=window_height-((button_size+5)*4)-25, anchor=tk.N)

            self._gui_keyboard_keys = {}

            #first row
            for i in range(10):
                self._gui_keyboard_keys[keys[i]] = tk.Button(self._gui, text = keys[i].upper())
                self._gui_keyboard_keys[keys[i]].place(bordermode=tk.OUTSIDE, height=button_size, width=button_size, x=((window_width/2)-((button_size+5)*5))+(i*(button_size+5)), y=window_height-((button_size+5)*3))
            #second row
            for i in range(10,19):
                self._gui_keyboard_keys[keys[i]] = tk.Button(self._gui, text = keys[i].upper())
                self._gui_keyboard_keys[keys[i]].place(bordermode=tk.OUTSIDE, height=button_size, width=button_size, x=(((window_width/2)+(button_size/2))-((button_size+5)*5))+((i-10)*(button_size+5)), y=window_height-((button_size+5)*2))
            #third row
            self._gui_keyboard_keys["enter"] = tk.Button(self._gui, text = "ENTER")
            self._gui_keyboard_keys["enter"].place(bordermode=tk.OUTSIDE, height=button_size, width=button_size*1.5, x=((window_width/2)-((button_size+5)*5)), y=window_height-(button_size+5))

            for i in range(19,26):
                self._gui_keyboard_keys[keys[i]] = tk.Button(self._gui, text = keys[i].upper())
                self._gui_keyboard_keys[keys[i]].place(bordermode=tk.OUTSIDE, height=button_size, width=button_size, x=(((window_width/2)+(button_size/2))-((button_size+5)*3))+((i-20)*(button_size+5)), y=window_height-(button_size+5))

            self._gui_keyboard_keys["enter"] = tk.Button(self._gui, text = "BACKSPACE")
            self._gui_keyboard_keys["enter"].place(bordermode=tk.OUTSIDE, height=button_size, width=button_size*1.5, x=(((window_width/2)+(button_size/2))-((button_size+5)*3))+((i+1-20)*(button_size+5)), y=window_height-(button_size+5))

    def start_game(self):
        if(self._enable_debug):
            print("Word is: - ", self._word.upper(), " -")
        if(self._enable_verbose):
            print("+---+---+---+---+---+")
            print("|", "h"+"\u0332", "|", "E"+"\u0332", "|", "L"+"\u0332", "| l |", "o"+"\u0332", "|")
            print("+---+---+---+---+---+")
            print("Lower case letters like l are not in the word")
            print("Lower case letters underlined like", "h"+"\u0332", "and", "o"+"\u0332", "are in the word but not in the correct position")
            print("Upper case letters underlined like", "E"+"\u0332", "and", "L"+"\u0332", "are in the word and in the correct position")
            print("Game Begining...")
        if(self._enable_gui):
            self._set_gui()
            self._gui.mainloop()

    def end_game(self):
        self._gui.destroy()

    def _event_enter_gui(self, event):
        self.make_guess()

    # "not_valid" = word is not a valid word
    # "valid" = word is valid and correct length
    # "game_over_win" = game over win
    # "game_over_lose" = game over lose
    def _update_gui(self, guess = None, flag=""):
        if(flag == "not_valid"):
            self._gui_error_label.config(text = "Not a Valid Word, Try Again")
            return
        elif(flag == "valid"):
            guess_arr = [char for char in guess]

            #clearing any lingering error because current guess is valid
            self._gui_error_label.config(text = "")

            for i in range(self._word_len):
                #Adding line to board
                #green or perfect placement
                if (self._guesses_arr[self._guesses_arr_len-1][i] == "g"):
                    self._gui_frames[self._guesses_arr_len-1][i].config(background="green")
                    self._gui_letters[self._guesses_arr_len-1][i].config(text = guess_arr[i].upper())
                    self._gui_letters[self._guesses_arr_len-1][i].config(background="green")
                    #coloring the keyboard keys
                    if(self._enable_keyboard):
                        self._gui_keyboard_keys[guess_arr[i]].config(background="green")

                #yellow, or letter in word but wrong spot
                elif (self._guesses_arr[self._guesses_arr_len-1][i] == "y"):
                    self._gui_frames[self._guesses_arr_len-1][i].config(background="yellow")
                    self._gui_letters[self._guesses_arr_len-1][i].config(text = guess_arr[i].upper())
                    self._gui_letters[self._guesses_arr_len-1][i].config(background="yellow")
                    #coloring the keyboard keys
                    if(self._enable_keyboard):
                        if(self._keys[guess_arr[i]] != "g"):
                            self._gui_keyboard_keys[guess_arr[i]].config(background="yellow")

                #coloring any keyboard keys are not in the word
                else:
                    self._gui_letters[self._guesses_arr_len-1][i].config(text = guess_arr[i].upper())
                    #coloring the keyboard keys
                    if(self._enable_keyboard):
                        if (self._keys[guess_arr[i]] != "g") and (self._keys[guess_arr[i]] != "y"):
                            self._gui_keyboard_keys[guess_arr[i]].config(background="grey")
        elif(flag == "game_over_win"):
            self._gui_guess_entry.config(state='disable')
            self._gui_guess_button.config(state='disable')
            self._gui_error_label.config(text = "Congratulations! You Win!")
        elif(flag == "game_over_lose"):
            self._gui_guess_entry.config(state='disable')
            self._gui_guess_button.config(state='disable')
            self._gui_error_label.config(text = "Game Over, Word Was: " + self._word.upper())
        else:
            self._gui_error_label.config(text = "Unspecified gui update flag. See debug log for more information")

    def _update_verbose(self, guess = None, flag=""):
        if(flag == "not_valid"):
            print(guess.upper(), " not a Valid Word, Try Again")
            return

        elif(flag == "valid"):
            guess_arr = [char for char in guess]

            #clearing any lingering error because current guess is valid
            self._gui_error_label.config(text = "")

            for i in range(self._word_len):
                #Adding line to board
                #green or perfect placement
                if (self._guesses_arr[self._guesses_arr_len-1][i] == "g"):
                    self._verbose_board_str += "| " + (guess_arr[i].upper()+"\u0332") + " "

                #yellow, or letter in word but wrong spot
                elif (self._guesses_arr[self._guesses_arr_len-1][i] == "y"):
                    self._verbose_board_str += "| " + (guess_arr[i]+"\u0332") + " "

                #coloring any keyboard keys are not in the word
                else:
                    self._verbose_board_str += "| " + guess_arr[i] + " "

            self._verbose_board_str += "|\n"
            self._verbose_board_str += "+---+---+---+---+---+\n"

            print(self._verbose_board_str)

        elif(flag == "game_over_win"):
            print("Congratulations, You Win!")

        elif(flag == "game_over_lose"):
            print("Game Over, Word Was: " + self._word.upper())

        else:
            print("Unspecified gui update flag: ", flag, " . See debug log for more information")

    def make_guess(self, guess=None):

        # Set Guess to the string in the guess entry box
        if (guess == None):
            guess = self._gui_guess_entry.get()
            self._gui_guess_entry.delete(0,tk.END)

        guess = guess.lower() #need to lowercase to compare with words list

        #check if guess is in list of words
        if not(guess in self._words) or (len(guess) != self._word_len):
            if(self._enable_gui):
                self._update_gui(guess, "not_valid")
            if(self._enable_verbose):
                self._update_verbose(guess, "not_valid")
            return(False)

        #Setting guess_arr and keys
        guess_arr = [char for char in guess]
        temp_word_arr = copy.deepcopy(self._word_arr)

        self._guesses_arr.append([])
        self._guesses_arr_len = len(self._guesses_arr)

        #setting green in private board array
        for i in range(self._word_len):
            self._guesses_arr[self._guesses_arr_len-1].append("e")
            if (guess_arr[i] == temp_word_arr[i]):
                self._guesses_arr[self._guesses_arr_len-1][i] = "g"
                temp_word_arr[i] = None

        #setting yellow in private board array
        for i in range(self._word_len):
            if (guess_arr[i] in temp_word_arr):
                if not(self._guesses_arr[self._guesses_arr_len-1][i] == "g"):
                    self._guesses_arr[self._guesses_arr_len-1][i] = "y"
                    temp_word_arr[temp_word_arr.index(guess[i])] = None

        for i in range(self._word_len):
            if(self._guesses_arr[self._guesses_arr_len-1][i] == "g"):
                self._keys[guess_arr[i]] = "g"
            elif (self._keys[guess_arr[i]] != "g") and (self._guesses_arr[self._guesses_arr_len-1][i] == "y"):
                self._keys[guess_arr[i]] = "y"
            elif (self._keys[guess_arr[i]] != "g") and (self._keys[guess_arr[i]] != "y"):
                self._keys[guess_arr[i]] = "e"

        #update gui
        if(self._enable_gui):
            self._update_gui(guess, "valid")
        #update verbose
        if(self._enable_verbose):
            self._update_verbose(guess, "valid")

        #end game conditions
        #game won
        if(guess == self._word):
            if(self._enable_gui):
                self._update_gui(flag="game_over_win")
            if(self._enable_verbose):
                self._update_verbose(guess, "game_over_win")
            self.game_over = True

        #max guess reached, game lost
        elif(len(self._guesses_arr) == self._num_guesses):
            if(self._enable_gui):
                self._update_gui(flag="game_over_lose")
            if(self._enable_verbose):
                self._update_verbose(guess, "game_over_lose")
            self.game_over = True

        #handle information returns
        return(self._guesses_arr)
