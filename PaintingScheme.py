'''
this is how the World should be painted,
given ...cerTain conditions, including cerTain times only in conjunction with cerTain moods,
...cerTain human moods...
'''
from math import sqrt
from random import uniform, random
from copy import deepcopy

from GameBoardHandler import *

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

    """
    description:
    - assigns gameboard locations based on element areas by the following scheme:
        using reference point R = (0, 0),
        for all areas,
            assign region starting at R to gameboard
            update R
        **assignment of region should be one with the most free space**
    """
    @staticmethod
    def assign_locations_for_elements_by_area(areas):

        refVal = (0,0)
        elementLocations = []

        for a in areas:
            return a
        return -1

    '''
    description:
    - gets the rectangular region that best fits element's `area` given the usedRegions

    arguments:
    - area := (int,int), specifies the new region's dimensions
    - boardDimensions := (int,int), specifies board dimensions
    - usedRegions := list(((int,int), (int,int)), contains regions that have already been allocated

    return:
    - (minX, maxX), (minY, maxY) : denotes new region
    - bool, if region overlaps with any other
    '''
    @staticmethod
    def get_region_to_fit_element(area, boardDimensions, usedRegions):

        # algorithm :
        # get lowest unmarked x value
        # get lowest unmarked y value
        return -1

    ########### TODO : methods for scanning left-to-right-fit below are not known
    '''
    description:
    - scans gameboard top to bottom looking for empty rectangle to fit `area`

    arguments:
    ~ see method PaintingScheme.get_region_to_fit_element

    return:
    - (minX, maxX), (minY, maxY) : denotes new region
    '''
    @staticmethod
    def scan_left_to_right(area, boardDimensions, usedRegions, scanIncrement = 0.01):
        return -1

    '''
    description:
    - scans gameboard top to bottom looking for empty rectangle to fit `area`

    arguments:
    -

    return:
    -
    '''
    @staticmethod
    def scan_top_to_bottom(area, boardDimensions, usedRegions):
        return -1

    ########### END TODO : methods for scanning left-to-right-fit below are not known

    @staticmethod
    def update_locations_for_elements_by_area(areas):
        return -1

    '''
    description:
    -

    centroids := list(set(str))
    '''
    @staticmethod
    def centroids_to_gameboard_points(centroids, coordinateRange):
        return -1

    def check_points_for_minimum_distance(listOfPoints):
        return -1

    #--------------------- DELETE THESE METHODS -------------------------------#
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

    # TODO : element.wordRatio of type ("net", "set")
    """

    schemes are defined as the following:
    - rectangle := each element is an m x n subset of GameBoard
                values m and n are determined by element.wordRatio

    arguments:
    - scheme := word2coord |element2Region


    """
    @staticmethod
    def populate_by_scheme(gameboard, scheme = "rectangle"):
        ##assert scheme in {"rectangle"}, "scheme {} has not been implemented.".format(scheme)
        assert scheme in {"word2coord", "element2region"}, "scheme {} has not been implemented.".format(scheme)

        if scheme == "rectangle":
            # get centroids first
            return -1

        return -1
    #----------------------------------------------------------------------------------------

    '''
    description:
    - assigns coordinates for unregistered words.
      this is initial assignment.

    arguments:
    - gameboard := GameBoard

    return:
    - gameboard
    '''
    # TODO : test this
    @staticmethod
    def populate_by_word_to_coordinate_assignment(gameboard, minDistance = "auto"):

        # set centroid coordinates
        centroids = GameBoardHandler.choose_n_points(len(gameboard.elements), gameboard.dimensions, gameboard.wordCoordinates, minDistance = minDistance)
        gameboard.set_centroid_coordinates(centroids)

        # get coordinates for each word in centroid

        # for centroids
        for i, c in enumerate(centroids):
            points = GameBoardHandler.choose_random_points_in_radius(c, radius, len(gameboard.elements[i].language.language[0]))
            gameboard.add_word_coordinate_info(gameboard.elements[i].language.language[0], points)

        # for all other points
        # TODO
        radiusValues = GameBoardHandler.calculate_radius_values_given_centroids()
        for i in range(len(gameboard.elements)):
            radiusValue = Game
            points = GameBoardHandler.choose_unused_random_points_in_radius(centroids[i], radiusValue)

    '''
    description:
    -

    arguments:
    - gameboard := GameBoard
    '''
    @staticmethod
    def populate_by_element_to_region_assignment(gameboard):
        # get centroid coordinates
        return -1

    @staticmethod
    def x():
        return -1

def PaintingScheme_ChooseNCentroids():
    numPoints = 100
    gameBoardCoordinates = (50, 20)
    setOfCoordinates = {(4, 9), (20, 25), (42, 55)}
    centroids = PaintingScheme.choose_n_points(numPoints, gameBoardCoordinates, setOfCoordinates, minDistance = 2)
    return centroids

centroids = PaintingScheme_ChooseNCentroids()
