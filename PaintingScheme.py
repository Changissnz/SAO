'''
this is how the World should be painted,
given ...cerTain conditions, including cerTain times only in conjunction with cerTain moods,
...cerTain human moods...
'''
from math import sqrt
from random import uniform, random
from copy import deepcopy

# TODO : assigning and updating centroids

class PaintingScheme:

    '''
    description:
    - returns a dictionary of keys words/setOfWords and values gameboard coordinates
    '''
    @staticmethod
    def paint_scheme_given_gameboard_data(coordinateRange, languages):
        accounted = {} #
        return -1

    @staticmethod
    def color_generator_cycle(numColors):
        return -1

    '''
    description:
    -

    centroids := list(set(str))
    '''
    @staticmethod
    def centroids_to_gameboard_points(centroids, coordinateRange):
        return -1

    '''
    description:
    -

    arguments:
    -


    '''
    @staticmethod
    def get_distance_between_coordinates(coord1, coord2):
        assert len(coord1) == 2 and len(coord2) == len(coord1), "only 2-dimensions are permitted."
        return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2 )

    '''
    description:
    - chooses n centroids on game board

    arguments:
    - numCentroids := int
    - coordinateRange := (int::(maxX), int::(maxY))

    return:
    -
    '''
    @staticmethod
    def choose_n_points(numCentroids, coordinateRange, setOfCoordinates, minDistance = "auto"):

        ##def get_valid_coordinate(otherCoordinates, coordinateRange, minDistance):
        def farEnough(x):
            print("X :\t", x)
            for c in otherCoordinates:
                if PaintingScheme.get_distance_between_coordinates(c, x) <= minDistance:
                    return False
            return True

        if minDistance == "auto":
            minDistance = (coordinateRange[0] * coordinateRange[1]) / (2 * numCentroids)

        otherCoordinates = deepcopy(setOfCoordinates)
        centroids = []
        while len(centroids) < numCentroids:
            x = (uniform(0, coordinateRange[0]), uniform(0, coordinateRange[1]))
            if farEnough(x):
                print("coordinate :\t", x)
                otherCoordinates.add(x)
                centroids.append(x)
            #print("length :\t", len(centroids))
        return centroids

    def check_points_for_minimum_distance(listOfPoints):
        return -1

    '''
    description:
    - chooses a random coordinate in the ball radius of some point p

    arguments:
    -

    return:
    -
    '''
    @staticmethod
    def choose_random_point_in_radius(p, radius):
        p_ = []
        for p1 in p:
            px = uniform(0, radius)
            px = -px if random() < 0.5 else px
            p_.append(px)
        return tuple(p_)

    # TODO : merge `languageContents` and `correspondingColors` into a dict-like object
    @staticmethod
    def populate_by_scheme1(languageContents, correspondingColors, wordToCoordinateFunc, minDistance = "auto"):


        # get centroid coordinates

        # for each language
        # determine its radius
        # for each word in language
        # if word does not have coordinate
        # assign it coordinate
        # else
        # paint the pixel by painting scheme
        centroids = PaintingScheme.choose_n_points(len(languageContents), gameBoardCoordinates, setOfCoordinates, minDistance = minDistance)

        wordToCoordinate = {}
        for lc in languageContents:
            return -1

        # a better approach would be to keep track of the
        return -1

    '''

    arguments:
    - board := GameBoard
    '''
    @staticmethod
    def initial_populate_by_scheme(board, minDistance = "auto"):

        '''
        description:
        - calculates the area for each element based on their language contents.

        arguments:
        - mode := net|set

        return:
        - list(int)
        '''
        def get_areas_for_elements(mode = "net"):
            areas = []
            for e in board.elements:
                if mode == "net":
                    return
                else:
                    return
            return -1


        # get the centroids
        centroids = PaintingScheme.choose_n_points(len(board.languages), board.dimensions, board.wordCoordinates, minDistance = minDistance)

        # assign language word centroids to points centered around point centroids
        for i in range(len(centroids)):
            centroids[i]

        # assign words
        return -1

    '''
    
    '''
    @staticmethod
    def populate_by_word_to_coordinate_assignment():
        return -1

    '''
    circle and radius
    '''
    @staticmethod
    def populate_by_element_to_region_assignment():
        return -1




def PaintingScheme_ChooseNCentroids():

    numPoints = 100
    gameBoardCoordinates = (50, 20)
    setOfCoordinates = {(4, 9), (20, 25), (42, 55)}
    centroids = PaintingScheme.choose_n_points(numPoints, gameBoardCoordinates, setOfCoordinates, minDistance = 2)
    return centroids

centroids = PaintingScheme_ChooseNCentroids()


"""
description:
- make a paintHistory value.
cumulative(n past color values are kepted and averaged) vs layered(only 1 color value kept)

arguments:
- languageContents := list((set(str), container(str)))
- wordToCoordinateFunc :=

return:
-
"""
