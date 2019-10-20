'''
this is the game board.
'''
####
'''
there are many ways to design a game board, which could be:

1. each block denotes a set of words
    a. an element's territory will be marked by a character
    b. each element will be represented as a set of blocks centered around a centroid.
    c. the higher the intersection, the more overlap between these two "circular regions"

    a. an element's territory will be marked by a character
    b. each element will be represented as a set of blocks on board.

'''


class GameBoard:

    def __init__(self, languageInfo, dimensions, elements):
        assert len(elements) <= 52, "cannot operate on more than 52 elements"
        self.dimensions, self.elements = dimensions, elements
        self.wordCoordinates = {}
        self.set_languages(languageInfo)

    '''
    description:
    -
    '''
    def set_languages(self, languageInfo):
        if type(languageInfo) is int:
            self.languages = LanguageMaker.get_languages(n = languageInfo[0], minSizeInfo = languageInfo[1], startSizeInfo = languageInfo[2], mode = "geq")
        elif type(languageInfo) is list: # list of languages
            self.languages = languageInfo

        return -1

    '''
    description:
    - sets the initial board using element languages.
    '''
    def set_initial_board(self):
        return -1
