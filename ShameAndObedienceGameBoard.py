'''
this is where visualization of gameboard in Shame And Obedience goes.
'''
from GameBoard import *
from PaintingScheme import *
from FreeAndSimpleScanner import *
from EventHistory import *

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
    - actionFunctions := dict(`action`:func), `action` could be `shame` or `align`
    """
    def __init__(self, languageInfo, dimensions, assignElementsToRegion = False,\
            pixelRes = (400, 400), areaChangeUpdate = "auto", typeShame = {"centroid", "descriptor"},\
            selfReproductionFrequency = (1, 0.05), actionFunctions = None):
        assert len(languageInfo) < 12, "Shame And Obedience accepts a maximum of 12 elements"
        super().__init__(languageInfo, dimensions, 12, assignElementsToRegion = assignElementsToRegion)
        self.pixelRes = pixelRes
        self.set_area_change_update(areaChangeUpdate)
        self.typeShame = typeShame
        self.selfReproductionFrequency = selfReproductionFrequency
        self.update_element_colors()
        PaintingScheme.make_blanko(self.pixelRes)
        self.eventLogger = EventHistory(1, None)
        self.set_action_functions(actionFunctions)

    """
    description:
    - sets action functions for shame and align

    arguments:
    - af := dict, standard function dict.

    return:
    -
    """
    def set_action_functions(self, af):
        if af == None: return
        self.shameFunc, self.alignFunc = af["shame"], af["align"]

    """
    description:
    - codes for setting uniform element action functions
    """
    def set_element_action_functions_uniform(self):
        for e in self.elements.values():
            e.shameFunc = self.shameFunc
            e.alignFunc = self.alignFunc

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

    # TODO : update visualization here

    """
    description:
    - updates language stats for each element,
      active descriptor and word counts.
    """
    def update_language_stats(self):
        for e in self.elements.values():
            e.update_language_stats()

    # TODO : work on this, inefficient
    # TODO : work on element descriptor overlaps
    """
    description:
    - sets shame-align pairwise measures for elements
    """
    def update_element_alignments(self):

        for e in self.elements.values():
            q = self.the_others(e.idn)
            # set overlap measures
            e.get_element_language_measures(q, setClassVar = True)

    """
    arguments:
    - idn := int

    return:
    - `all elements not of idn`
    """
    def the_others(self, idn):
        return [e for e in self.elements.values() if e.idn != idn]

    """
    description:
    - moves against all other elements
    """
    def move_elements(self, mode = "standard"):
        assert mode == "standard", "mode {} is invalid".format(mode)

        for k, v in self.elements.items():
            oth = self.the_others(v.idn)
            v.move_one_timestamp(oth, self.typeShame, self.eventLogger.timeStamp, self.selfReproductionFrequency)

    """
    description:
    -
    """
    def move_one(self):
        self.update_language_stats()
        self.update_element_alignments()
        self.move_elements()

        # update visualization and areas here

        # REFACTOR
        # update history here
        self.eventLogger.log(self)


    def run(self, numRounds = None):
        # set shame and align functions first
        self.set_element_action_functions_uniform()

        # run a maximum of `numRounds`
        if numRounds != None:
            for _ in range(numRounds):
                self.move_one()
                if self.termination_condition_mute():
                    print("TERMINATED")
                    break
            return

        while self.termination_condition_mute() == False:
            self.move_one()

    # TODO
    '''
    description:
    - determines if game should halt based on following:
    -   if only 1 speaker
    '''
    def termination_condition_mute(self):
        nonmute = []
        # get number of mute elements
        for k, e in self.elements.items():
            if e.activeWordCount != 0:
                nonmute.append(k)

        if len(nonmute) <= 1:
            return True
        return False


    ######################### END : methods for moving one timestamp on gameboard ###############
