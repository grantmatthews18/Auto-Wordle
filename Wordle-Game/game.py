from tkinter import *
from tkinter.ttk import *
#from functools import partial

class Game():
    def __init__(self, word, num_guesses):
        self._word = word
        self._word_len = len(word)
        self._num_guesses = num_guesses

        self._gui = Tk()

    def _set_gui(self):

        window_width = 5 + (105*self._word_len)
        window_height = 250 + (105*self._num_guesses)
        str_window_size = str(window_width) + "x" + str(window_height)

        self._gui.title("Classic Mode")
        self._gui.geometry(str_window_size)
        self._gui.minsize(window_width,window_height)
        self._gui.maxsize(window_width,window_height)

        title_banner = Label(self._gui, text = "Classic Mode", font = ("Arial", 25)).place(relx=.5, y=33, anchor=CENTER)
        info_banner = Label(self._gui, text = "Type Your Guess in the box below to begin").place(relx=.5, y=66, anchor=CENTER)

        letters = []

        for ypos in range(self._num_guesses):
            letters.append([])
            for xpos in range(self._word_len):
                letters[ypos].append(Frame(self._gui, borderwidth=1, relief="solid", width=100, height=100))
                letters[ypos][xpos].place(x=5+(xpos*105), y=100+(ypos*105))

        guess_var = StringVar()
        self._guess_entry = Entry(self._gui, textvariable = guess_var, font = ("Arial", 25))
        self._guess_entry.place(relx=.5, y=window_height-100, anchor=CENTER)
        guess_button = Button(self._gui, text = "Guess", command=self._send_guess).place(relx=.5, y = window_height-50, anchor=CENTER)
        self._gui.bind('<Return>', self._event_enter)




    def start_game_verbose(self):
        #do something, set verbose flag
        return()

    def start_game_no_gui(self):
        #do something, set verbose flag, set no gui flag
        return()

    def start_game(self):
        self._set_gui()
        self._gui.mainloop()

    def end_game(self):
        self._gui.destroy()

    def _send_guess(self):
        guess = self._guess_entry.get()
        self._guess_entry.delete(0,END)
        self.make_guess(guess)

    def _event_enter(self, event):
        guess = self._guess_entry.get()
        self._guess_entry.delete(0,END)
        self.make_guess(guess)

    def make_guess(self, guess):
        # return something to indicate guess
        print("Guessed ", guess)
        return()
