from cnb_guesser.guessers.vector_guesser import Word2VecGuesser, GloveNetGuesser
from cnb_guesser.guessers.gpt.few_shot_guesser import FewShotGuesser
from cnb_guesser.guessers.gpt.gpt_guesser import SimpleGuesser, ListGuesser
from cnb_guesser.guessers.gpt.relation_guesser import RelationGuesser, FewShotRelationGuesser
from cnb_guesser.guessers.vote_guesser import VoteGuesser

def get_guesser(name):
    if name == "word2vec":
        return Word2VecGuesser()
    elif name == "glove":
        return GloveNetGuesser()
    elif name == "gpt-simple":
        return SimpleGuesser()
    elif name == "gpt-list":
        return ListGuesser()
    elif name == "gpt-relation":
        return RelationGuesser()
    elif name == "gpt-few-shot":
        return FewShotGuesser()
    elif name == "gpt-relation-few-shot":
        return FewShotRelationGuesser()
    elif name == "vote":
        return VoteGuesser()
    raise ValueError()