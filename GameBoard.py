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

    def __init__(self, dimensions, elements):
        assert len(elements) <= 52, "cannot operate on more than 52 elements"
        self.dimensions, self.elements = dimensions, elements

    '''
    description:
    - sets the initial board using element languages.
    '''
    def set_initial_board(self):
        return -1
