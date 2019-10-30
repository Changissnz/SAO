'''
this is where visualization of gameboard in Shame And Obedience goes.
'''

# classes to work on
# GameBoard
# PaintingScheme
# this

from GameBoard import *
from PaintingScheme import *
from FreeAndSimpleScanner import *

class ShameAndObedienceGameBoard(GameBoard):

    # TODO : make assertion for pixelRes
    """
    arguments:
    - languageInfo := list(Language)
    - dimensions := (int,int), info for gameboard
    - pixelRes := (int,int), resolution info. for screen
    - areaChangeUpdate := "auto"|float, threshold value determines when visualization needs to be updated
    - selfReproductionFrequency := (int::(number of rounds before update), float::(ratio of current language size)) ;
                                value determines how elements will reproduce
    """
    def __init__(self, languageInfo, dimensions, assignElementsToRegion = False,\
            pixelRes = (400, 400), areaChangeUpdate = "auto", typeShame = {"centroid", "descriptor"},\
            selfReproductionFrequency = (1, 0.05)):
        assert len(languageInfo) < 12, "Shame And Obedience accepts a maximum of 12 elements"
        super().__init__(languageInfo, dimensions, 12, assignElementsToRegion = assignElementsToRegion)
        self.pixelRes = pixelRes
        self.set_area_change_update(areaChangeUpdate)
        self.typeShame = typeShame
        self.selfReproductionFrequency = selfReproductionFrequency
        self.update_element_colors()
        PaintingScheme.make_blanko(self.pixelRes)
        self.eventLogger = EventHistory(frequency = 10)

    ######################### START : methods for visualization here ###############
    """
    description:
    - gets color for element based on its language stats
    - element stats cannot be none
    """
    def update_element_colors(self):
        for k, v in self.elements.items():
            q = deepcopy(self.elements)
            del q[k]
            q = [q_ for q_ in q.values()]
            v.update_color(q)
        return

    def set_area_change_update(self, areaChangeUpdate):
        assert areaChangeUpdate == "auto" or type(areaChangeUpdate) is float, "invalid areaChangeUpdate {}".format(areaChangeUpdate)
        self.areaChangeUpdate = self.area / 4 if areaChangeUpdate == "auto" else areaChangeUpdate

    def paint_element(self, elementIndex, zheFile = "defaultPitcherOfEmotions.png"):
        q = self.elements[elementIndex]

        if q.location != None:
            x = PaintingScheme.convert_region_to_pixel_region(q.location, self.dimensions, self.pixelRes)
            ##print("PAINTING :\t", x)
            PaintingScheme.paint_image_given_pixel_region_and_color(x, q.currentColor, zheFile = zheFile)

    def paint_elements(self,  zheFile = "defaultPitcherOfEmotions.png", mode = "clear first"):
        assert mode in {"clear first", None}

        if mode == "clear first":
            PaintingScheme.make_blanko(self.pixelRes, zheFile)

        for k in self.elements.keys():
            self.paint_element(k)
        return True

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
            PaintingScheme.paint_image_given_pixel_region_and_color(r, c, zheFile = zheFile)
        return True

    ######################### END : methods for visualization here ###############

    ######################### START : methods for moving one timestamp on gameboard ###############

    """
    description:
    -
    """
    def move_one(self):
        self.update_element_alignments()
        self.move_elements()

        # update visualization and areas here


    def move_elements(self):
        def others(ex):
            return [e for self.elements if e.idn != ex]


        for k, v in self.elements.items():
            oth = others(v.idn)
            for o in oth:
                v.move_against(o, self.typeShame)



    def run(self):

        return -1



    ######################### END : methods for moving one timestamp on gameboard ###############
