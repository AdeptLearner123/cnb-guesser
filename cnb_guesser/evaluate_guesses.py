from argparse import ArgumentParser

from config import SCENARIOS, GENERATED_GUESSES, SCENARIOS_DATA, GENERATED_GUESSES_NOTES
import yaml
import os
from collections import Counter

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-f", type=str, required=True)
    parser.add_argument("-r", action="store_true")
    args = parser.parse_args()
    return args.f, args.r


def evaluate_guess(scenario, guesses):
    return set(guesses) == set(scenario["pos"])


def main():
    file_name, review = parse_args()
    file_path = os.path.join(GENERATED_GUESSES, f"{file_name}.yaml")

    with open(file_path, "r") as file:
        scenario_guesses = yaml.safe_load(file.read())
    
    with open(SCENARIOS, "r") as file:
        scenarios = yaml.safe_load(file.read())
    
    with open(SCENARIOS_DATA, "r") as file:
        scenarios_data = yaml.safe_load(file.read())
    
    corrects = Counter()
    totals = Counter()
    failures = []
    for scenario_id in scenario_guesses:
        keys = ["all"]
        if scenarios_data[scenario_id]["is_easy"]:
            keys.append("easy")
        else:
            keys.append("hard")

        if evaluate_guess(scenarios[scenario_id], scenario_guesses[scenario_id]):
            for key in keys:
                corrects[key] += 1
        else:
            failures.append(scenario_id)
        
        for key in keys:
            totals[key] += 1

    for key in corrects:
        print(f"{key}: {corrects[key]} / {totals[key]} = {corrects[key] / totals[key]}")
    
    if review:
        with open(os.path.join(GENERATED_GUESSES_NOTES, f"{file_name}.yaml"), "r") as file:
            notes = yaml.safe_load(file.read())
        
        for i, failure_id in enumerate(failures):
            print(f"\n\n\n=== {i} ===")
            print("Pos:", scenarios[failure_id]["pos"])
            print("Clue:", scenarios[failure_id]["clue"])
            print("Guess:", scenario_guesses[failure_id])
            print("Notes:", notes[failure_id])


if __name__ == "__main__":
    main()