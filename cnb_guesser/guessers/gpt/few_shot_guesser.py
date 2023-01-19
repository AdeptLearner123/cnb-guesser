from .gpt_guesser import GPTGuesser

from config import GUESSER_FEW_SHOT_PROMPT

class FewShotGuesser(GPTGuesser):
    def __init__(self):
        super().__init__()
        with open(GUESSER_FEW_SHOT_PROMPT, "r") as file:
            self._examples = file.read()


    def guess(self, words, clue, num):
        self._completer.clear_history()

        prompt = self._examples + "\n" + \
                self.get_instruction(words, clue, num)
        
        completion = self._completer._get_completion(prompt).strip()
        lines = completion.splitlines()
        answer_line = lines[-1]
        answer = answer_line.split(":")[-1]

        return self.process_answer(answer), self._completer.get_history()