from abc import ABC, abstractmethod

class GuesserBase(ABC):
    @abstractmethod
    def guess(self, words, clue, num):
        pass

    
    def print_usage(self):
        print("No usage")