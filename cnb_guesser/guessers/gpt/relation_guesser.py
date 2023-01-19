from .gpt_guesser import GPTGuesser

class RelationGuesser(GPTGuesser):
    def guess(self, words, clue, num):
        self._completer.clear_history()

        relations = [ self._get_relation(word, clue) for word in words ]
        relations_str = [ f"{word}: {relation}" for word, relation in zip(words, relations) ]
        relations_str = "\n".join(relations_str)

        prompt = self.get_instruction(words, clue, num) + "\n" + \
                f"First let's see why {clue} might be related to each of the given words.\n\n" + \
                relations_str
        
        completion = self._completer._get_completion(prompt).strip()

        prompt2 = self.get_instruction(words, clue, num) + "\n" + \
                completion + "\n\n" + \
                "Answer (comma-separated):"
        
        completion2 = self._completer._get_completion(prompt2).strip()

        return self.process_answer(completion2), self._completer.get_history()


    def _get_relation(self, word1, word2):
        prompt = f"Explain why \"{ word1.lower() }\" and \"{ word2.lower() }\" might be related."
        completion = self._completer._get_completion(prompt)
        return completion.strip()