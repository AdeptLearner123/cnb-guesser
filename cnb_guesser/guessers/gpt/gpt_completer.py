import openai
import time

class GPTCompleter:

    def __init__(self):
        self._prompt_tokens = 0
        self._completion_tokens = 0
        self._total_tokens = 0
        self._completions = 0
        self._history = []


    def _update_usage(self, usage):
        if "prompt_tokens" in usage:
            self._prompt_tokens += usage["prompt_tokens"]
        if "completion_tokens" in usage:
            self._completion_tokens += usage["completion_tokens"]
        if "total_tokens" in usage:
            self._total_tokens += usage["total_tokens"]
        self._completions += 1


    def print_usage(self):
        print({
            "completions": self._completions,
            "prompt tokens": self._prompt_tokens, 
            "completion tokens": self._completion_tokens,
            "total tokens": self._total_tokens
        })


    def clear_history(self):
        self._history = []
    

    def get_history(self):
        return self._history


    def _get_completion(self, prompt):
        completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0, top_p=1, max_tokens=256)
        self._update_usage(completion.usage)
        time.sleep(1)
        completion_text = completion.choices[0].text
        self._history.append({
            "prompt": prompt,
            "completion": completion_text.strip()
        })
        return completion_text