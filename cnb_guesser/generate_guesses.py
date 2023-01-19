from argparse import ArgumentParser

from tqdm import tqdm
import os

from .utils import get_guesser
from config import SCENARIOS, GENERATED_GUESSES, GENERATED_GUESSES_NOTES
import yaml
import random

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-m", type=str, required=True)
    args = parser.parse_args()
    return args.m


def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)


def main():
    random.seed(0)
    model_name = parse_args()
    model = get_guesser(model_name)

    output_path = os.path.join(GENERATED_GUESSES, f"{model_name}_guesses.yaml")
    notes_path = os.path.join(GENERATED_GUESSES_NOTES, f"{model_name}_guesses.yaml")

    with open(SCENARIOS, "r") as file:
        scenarios = yaml.safe_load(file.read())

    guesses = dict()
    if os.path.exists(output_path):
        with open(output_path, "r") as file:
            guesses = yaml.safe_load(file.read())

    notes = dict()
    if os.path.exists(notes_path):
        with open(notes_path, "r") as file:
            notes = yaml.safe_load(file.read())
    
    #scenario_ids = list(scenarios.keys())[:100]
    missing_scenarios = [ scenario_id for scenario_id in scenarios if scenario_id not in guesses ]

    for key in tqdm(missing_scenarios):
        words = scenarios[key]["pos"] + scenarios[key]["neg"]
        random.shuffle(words)
        clue = scenarios[key]["clue"]
        guess, text = model.guess(words, clue, len(scenarios[key]["pos"]))
        guesses[key] = guess
        notes[key] = text

        with open(output_path, "w+") as file:
            file.write(yaml.dump(guesses, default_flow_style=None))
        
        with open(notes_path, "w+") as file:
            file.write(yaml.dump(notes, default_style="|"))        

        model.print_usage()