###
"""
a measure of influence that does not use direct intersection:
"functionality" : definitional capacity.
    - FUNC(definitions(Element.bagOfWords), (otherElement.bagOfWords)) => 0 <= float <= 1
    - will use similarity scores
    - FUNC should not be commutative
"""
###

from random import choice

class Language:

    def __init__(self, idn, bagOfWords):
        self.idn = idn
        self.bagOfWords = bagOfWords
        self.prohibited = set() # prohibited words

    def get_pertinent_definitions():
        return -1

    '''
    description:
    - gets the influence of this language over some other
    '''
    def get_influence_over(self, otherLanguage):
        return -1

    def get_influence_score_over_targets(self):
        return -1

    '''
    description:
    - pops subset of bagOfWords to prohibited
    '''
    def prohibit_speech(self, subsetBagOfWords):
        return -1

    '''
    description:
    - outputs a random string, consists of words from bagOfWords separated by whitespace
    '''
    def output_random_string(self):
        return -1

    # TODO
    def output_string_based_on_effect(self, factors):
        return -1

    @staticmethod
    def words_to_romantic(words):
        romantic = ["ia", "io", "o", "a", "ni", "li", "sa", "la", "si", "zzi"]
        for w in words:
            yield w + choice(romantic)
