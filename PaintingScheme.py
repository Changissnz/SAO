'''
this is how the World should be painted,
given ...cerTain conditions, including cerTain times only in conjunction with cerTain moods,
...cerTain human moods...
'''
from math import sqrt
from random import uniform, random
from copy import deepcopy
from PIL import Image

from GameBoardHandler import *

# TODO : assigning and updating centroids
class PaintingScheme:

    def __init__(self, simulation = "Shame And Obedience"):
        assert simulation == "Shame And Obedience", "simulation {} has not yet been implemented".format(simulation)
        self.simulation = simulation

############# BELOW CODE NEEDS TO BE REWRITTEN ############################################
###########################################################################################

    ########### START : methods for painting image given element info

    @staticmethod
    def make_blanko(pixelRes, saveFile = "defaultPitcherOfEmotions.png"):
        img = Image.new("RGB", pixelRes, 255)

        data = img.load()

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                data[x,y] = (
                    255,
                    255,
                    255,
                )
        img.save(saveFile)

    """
    description:
    - `region` must be a `proper image region`, defined as
        ((int,int),(int,int))
    -
    """
    @staticmethod
    def paint_image_given_region_and_color(region, color, zheFile = "defaultPitcherOfEmotions.png"):

        # load image here
        try:
            img = Image.open(zheFile)
        except: raise IOError("zheFile {} invalid".format(zheFile))

        data = img.load()

        # paint will go left to right
        # from bottom to top
        y = region[0][1]

        while y <= region[1][1]:
            for x in range(region[0][0], region[1][0] + 1):
                data[x,y] = color
            y += 1
        img.save(zheFile)

    @staticmethod
    def paint_image_using_gameboard_info(gameboard):
        return -1


    ########### END : methods for painting image given element info


    #----------------------------------------------------------------------------------------

    # TODO ?
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
