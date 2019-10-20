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
        self.centroidCoordinates = None
        self.set_languages(languageInfo)

    def get_area(self):
        return self.dimensions[0] * self.dimensions[1]

    '''
    description:
    - adds coordinate info to variable `wordCoordinates`,

    arguments:
    - words := set(str)
    - possibleCoordinates := list(tuple::(2-dim))

    return:
    - set, of words added
    '''
    def add_word_coordinate_info(self, words, possibleCoordinates):
        assert len(words) == len(possibleCoordinates), "invalid argumennt size: {} words and {} coordinates".format(len(words), len(possibleCoordinates))

        additions = {}
        for i, w in enumerate(words):
            if w not in self.wordCoordinates:
                self.wordCoordinates[w] = possibleCoordinates[i]
                additions.add(w)
        return additions

    '''
    description:
    -

    arguments:
    - languageInfo :=

    return:
    -
    '''
    def set_languages(self, languageInfo):
        if type(languageInfo) is int:
            self.languages = LanguageMaker.get_languages(n = languageInfo[0], minSizeInfo = languageInfo[1], startSizeInfo = languageInfo[2], mode = "geq")
        elif type(languageInfo) is list: # list of languages
            self.languages = languageInfo
        # call populate_by_word_to_coordinate_assignment
        return

    def set_centroid_coordinates(self, centroids):
        assert len(centroids) == len(self.elements), "invalid argumennt size: {} words and {} coordinates".format(len(centroids), len(self.elements))
        self.centroids = centroids

    '''
    description:
    - sets the initial board using element languages.
    '''
    def set_initial_board(self):
        return -1
