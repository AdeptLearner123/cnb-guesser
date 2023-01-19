from cnb_guesser.guessers.vector_guesser import Word2VecGuesser, GloveNetGuesser
from cnb_guesser.guessers.gpt.few_shot_guesser import FewShotGuesser
from cnb_guesser.guessers.gpt.gpt_guesser import SimpleGuesser, CoTGuesser, ListGuesser
from cnb_guesser.guessers.gpt.relation_guesser import RelationGuesser

def get_guesser(name):
    if name == "word2vec":
        return Word2VecGuesser()
    elif name == "glove":
        return GloveNetGuesser()
    elif name == "gpt-simple":
        return SimpleGuesser()
    elif name == "gpt-cot":
        return CoTGuesser()
    elif name == "gpt-list":
        return ListGuesser()
    elif name == "gpt-relation":
        return RelationGuesser()
    elif name == "gpt-few-shot":
        return FewShotGuesser()
    raise ValueError()