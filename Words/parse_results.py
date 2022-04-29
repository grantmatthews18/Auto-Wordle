import json
import copy

with open("Words/results_gen2.json","r+") as results_json:
    results = json.load(results_json)


for key in results.keys():
    total_guesses = 0
    number_lost = 0
    ct = 0
    for word in results[key].keys():
        if results[key][word][0] == "win":
            total_guesses +=  results[key][word][1]
        else:
            number_lost += 1
        ct += 1

    average_guesses = total_guesses/ct
    print("Agent: ", key, ". Average guesses: ", average_guesses, ". Total Lost: ", number_lost)
