import json
import copy
from itertools import product
import sys
sys.path.insert(1, "AI/")
import constants as ac
# with open("Words/wordle-words.json","r+") as words_json:
#     words = json.load(words_json)

letters = ["e", "y", "g"]
it_arr = product(letters, repeat = 5)
possible_result_arrs = [char for char in it_arr]

# filepath = "Words/easy.txt"
# with open(filepath, "w+") as text:
#     for element in possible_result_arrs:
#         text.write(str(element) + ", ")

print(ac.POSSIBLE_RESULT_ARRAY[0])

tuple1 = ("a",)
tuple2 = ("b",)
tuple3 = tuple1 + tuple2
print(tuple3)
