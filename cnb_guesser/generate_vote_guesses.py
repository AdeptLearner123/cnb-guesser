import yaml
from collections import Counter

from config import SCENARIOS

NUM_VOTES = 10
EARLY_STOPPING = True

def main():
    with open("guesses/notes/vote_guesses.yaml", "r") as file:
        vote_notes = yaml.safe_load(file.read())
    
    with open(SCENARIOS, "r") as file:
        scenarios = yaml.safe_load(file.read())
    
    guesses = dict()
    scenario_notes = dict()
    votes_used = 0

    for scenario_id in scenarios:
        guess, notes = generate_guess(vote_notes[scenario_id], scenarios[scenario_id])
        guesses[scenario_id] = guess
        scenario_notes[scenario_id] = notes
        votes_used += len(notes["guesses"])
    
    with open(f"guesses/notes/vote-10_early_stop_guesses.yaml", "w+") as file:
        file.write(yaml.dump(scenario_notes, default_flow_style=None))
    
    with open(f"guesses/vote-10_early_stop_guesses.yaml", "w+") as file:
        file.write(yaml.dump(guesses, default_flow_style=None))
    
    print("Votes used", votes_used)


def generate_guess(scenario_notes, scenario):
    words = scenario["pos"] + scenario["neg"]
    num = len(scenario["pos"])

    vote_counts = { word:0 for word in words }

    guesses_list = []
    guesses_left = NUM_VOTES

    for guess in scenario_notes["guesses"][:NUM_VOTES]:
        guesses_left -= 1
        if EARLY_STOPPING and should_stop(vote_counts, num, guesses_left):
            break

        guesses_list.append(guess)
        for word in guess:
            if word in vote_counts:
                vote_counts[word] += 1
    
    votes = [ (vote_count, word) for word, vote_count in vote_counts.items() ]
    votes = sorted(votes, reverse=True)
    sorted_words = [ word for _, word in votes ]
    guess = sorted_words[:num]

    return guess, {
        "votes": vote_counts,
        "guesses": guesses_list
    }


def should_stop(vote_counts, num, votes_left):
    counts = list(vote_counts.values())
    counts = sorted(counts, reverse=True)
    return counts[num - 1] - counts[num] >= votes_left