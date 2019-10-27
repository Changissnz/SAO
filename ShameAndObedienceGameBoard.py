'''
this is where visualization of gameboard in Shame And Obedience goes.
'''

# classes to work on
# GameBoard
# PaintingScheme
# this

from GameBoard import *
from PaintingScheme import *

class ShameAndObedienceGameBoard(GameBoard):

    # TODO : make assertion for pixelRes
    def __init__(self, languageInfo, dimensions, maxNumLanguages, pixelRes = (400, 400), areaChangeUpdate = "auto"):
        assert maxNumLanguages < 12, "Shame And Obedience accepts a maximum of 12 elements"
        super().__init__(languageInfo, dimensions, maxNumLanguages)
        self.pixelRes = pixelRes
        self.set_area_change_update(areaChangeUpdate)

    """
    description:
    - gets color for element based on its language stats
    - element stats cannot be none
    """
    def get_element_colors(self):
        return -1


    def set_area_change_update(self, areaChangeUpdate):
        assert areaChangeUpdate == "auto" or type(areaChangeUpdate) is float, "invalid areaChangeUpdate {}".format(areaChangeUpdate)
        self.areaChangeUpdate = self.area / 4 if areaChangeUpdate == "auto" else areaChangeUpdate

    def paint_gameboard(self):
        # get element stats
        self.get_element_stats()
        # assign elements to regions
        self.assign_elements_to_region()
        # get color for elements
        return -1

    """
    description:
    - paints image for gameboard

    arguments:
    - regionAndColorPairs := list((`region`, `its color`))
    - zheFile := str, filepath to save painted image to
    - mode := "clear first"|None, determines if picture should be cleared first

    return:
    - bool
    """
    # TODO : test this. 
    def paint(self, regionAndColorPairs, zheFile = "defaultPitcherOfEmotions.png", mode = "clear first"):
        assert mode in {"clear first", None}

        if mode == "clear first":
            PaintingScheme.make_blanko(self.pixelRes, zheFile)

        for r, c in regionAndColorPairs:
            PaintingScheme.paint_image_given_region_and_color(r, c, zheFile = zheFile)
        return True

    """
    description:
    - determines colors of element regions
    """
    def get_region_colors():
        return -1
