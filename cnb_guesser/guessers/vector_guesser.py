from .guesser_base import GuesserBase

import gensim.downloader

class VectorGuesser(GuesserBase):
    def __init__(self, model_name):
        self._keyed_vectors = gensim.downloader.load(model_name)


    def guess(self, words, clue, num):
        word_similarities = [ (self._similarity(word, clue), word) for word in words ]
        word_similarities = sorted(word_similarities, reverse=True)
        print(word_similarities)
        top_words = word_similarities[:num]
        top_words = [ word for _, word in top_words ]
        return top_words


    def _similarity(self, word1, word2):
        word1 = word1.lower()
        word2 = word2.lower()

        if word1 not in self._keyed_vectors.key_to_index or word2 not in self._keyed_vectors.key_to_index:
            return 0
        return self._keyed_vectors.similarity(word1, word2)


class Word2VecGuesser(VectorGuesser):
    def __init__(self):
        super().__init__("word2vec-google-news-300")


class GloveNetGuesser(VectorGuesser):
    def __init__(self):
        super().__init__("glove-wiki-gigaword-300")