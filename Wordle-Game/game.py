import tkinter as tk
import tkinter.ttk as ttk
import json
#from functools import partial

class Game():
    def __init__(self, word, num_guesses, gui_flag = True):
        self._word = word.lower()
        self._word_arr = [char for char in self._word]
        self._word_len = len(word)
        self._guesses_arr = []
        self._num_guesses = num_guesses

        filepath = "words/words-" + str(self._word_len) + ".json"
        with open(filepath) as words_json:
            self._words = json.load(words_json)

        self._enable_gui = gui_flag

        self._gui = tk.Tk()

    def _set_gui(self):

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


        guess_var = tk.StringVar()
        self._gui_guess_entry = tk.Entry(self._gui, textvariable = guess_var, font = ("Arial", 25))
        self._gui_guess_entry.place(relx=.5, y=window_height-100, anchor=tk.CENTER)
        guess_button = tk.Button(self._gui, text = "Guess", command=self.make_guess).place(relx=.5, y = window_height-50, anchor=tk.CENTER)
        self._gui.bind('<Return>', self._event_enter_gui)

        self._gui_error_label = tk.Label(self._gui, text="")
        self._gui_error_label.place(relx=.5, y = window_height-25, anchor=tk.CENTER)



    def start_game_verbose(self):
        #do something, set verbose flag
        return()

    def start_game_no_gui(self):
        #do something, set verbose flag, set no gui flag
        return()

    def start_game(self):
        print(self._word)
        self._set_gui()
        self._gui.mainloop()

    def end_game(self):
        self._gui.destroy()

    def _event_enter_gui(self, event):
        self.make_guess()

    def make_guess(self, guess=None):

        if (guess == None):
            guess = self._gui_guess_entry.get()
            self._gui_guess_entry.delete(0,tk.END)

        guess = guess.lower() #need to lowercase to compare with words list

        if(not guess in self._words):
            if(self._enable_gui):
                self._gui_error_label.config(text = "Not a Valid Word, Try Again")
            #do something verbose
            return
        else:
            if(self._enable_gui):
                self._gui_error_label.config(text = "")
            #do something verbose

        if(len(guess) != self._word_len):
            if(self._enable_gui):
                self._gui_error_label.config(text = "Not the Correct Word Length, Try Again")
            #do something verbose
            return
        else:
            if(self._enable_gui):
                self._gui_error_label.config(text = "")
            #do something verbos

        guess_arr = [char for char in guess]

        self._guesses_arr.append([])
        if(len(self._guesses_arr) > self._num_guesses):
            self._gui_error_label.config(text = "Game Over")
            #do something verbose
        else:
            self._guesses_arr[len(self._guesses_arr)-1] = guess_arr
            for i in range(self._word_len):
                if(self._enable_gui):
                    self._gui_letters[len(self._guesses_arr)-1][i].config(text = guess_arr[i].upper())
                #do something verbose

                #green or perfect placement
                if (guess_arr[i] == self._word_arr[i]):
                    if(self._enable_gui):
                        self._gui_frames[len(self._guesses_arr)-1][i].config(background="green")
                        self._gui_letters[len(self._guesses_arr)-1][i].config(background="green")
                    #do something verbose

                #yellow, or letter in word but wrong spot
                elif (guess_arr[i] in self._word_arr):
                    if(self._enable_gui):
                        self._gui_frames[len(self._guesses_arr)-1][i].config(background="yellow")
                        self._gui_letters[len(self._guesses_arr)-1][i].config(background="yellow")
                    #do something verbose




        # return something to indicate guess
        print("Guessed ", guess)
        return()
