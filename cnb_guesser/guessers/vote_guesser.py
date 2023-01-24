import random

from .guesser_base import GuesserBase
from .gpt.gpt_guesser import ListGuesser

class VoteGuesser(GuesserBase):
    NUM_TRIES = 10

    def __init__(self):
        super().__init__()
        self._guesser = ListGuesser()
    
    def guess(self, words, clue, num):
        votes = { word: 0 for word in words}
        guesses_list = []

        for _ in range(self.NUM_TRIES):
            words_shuffled = words.copy()
            random.shuffle(words_shuffled)
            guesses, _ = self._guesser.guess(words_shuffled, clue, num)

            guesses_list.append(guesses)

            for guess in guesses:
                if guess in votes:
                    votes[guess] += 1
        
        votes_dict = votes
        votes = [ (vote_count, word) for word, vote_count in votes.items() ]
        votes = sorted(votes, reverse=True)
        sorted_words = [ word for _, word in votes ]
        guesses = sorted_words[:num]
        return guesses, {
            "votes": votes_dict,
            "guesses": guesses_list
        }
    
    def print_usage(self):
        self._guesser.print_usage()