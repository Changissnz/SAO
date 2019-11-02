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
        assert ShameAndObedienceGameBoard.is_valid_pixel_res(pixelRes), "invalid pixelRes {}".format(pixelRes)
        self.pixelRes = pixelRes
        self.imageRes = ShameAndObedienceGameBoard.dim_to_square_dim(self.pixelRes)

        self.set_area_change_update(areaChangeUpdate)
        self.typeShame = typeShame
        self.selfReproductionFrequency = selfReproductionFrequency
        self.update_element_colors()
        PaintingScheme.make_blanko(self.pixelRes)
        self.eventLogger = EventHistory(1, None)
        self.set_action_functions(actionFunctions)

        # visualization here
        self.paint_elements()

    """
    description:
    -
    """
    @staticmethod
    def is_valid_pixel_res(pixelRes):
        if pixelRes[0] <= 0 or pixelRes[1] <= 0 or pixelRes[0] <= pixelRes[1]: return False
        if type(pixelRes[0]) is not int or type(pixelRes[1]) is not int:
            return False


        minimum, maximum = min(pixelRes), max(pixelRes)
        if minimum < 400: return False

        arbitraryScaleRange = (1.33, 2)
        if maximum/minimum >= arbitraryScaleRange[0] and maximum/minimum <= arbitraryScaleRange[1]:
            return True
        return False

    @staticmethod
    def dim_to_square_dim(pr):
        return (min(pr), min(pr))

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
            x = PaintingScheme.convert_region_to_pixel_region(q.location, self.dimensions, self.imageRes)
            print("PAINTING :\t", x)
            PaintingScheme.paint_image_given_pixel_region_and_color(x, q.currentColor, zheFile = zheFile)
            return
        print("XXX")

    def paint_elements(self,  zheFile = "defaultPitcherOfEmotions.png", mode = "clear first"):
        assert mode in {"clear first", None}

        if mode == "clear first":
            PaintingScheme.make_blanko(self.imageRes, zheFile)

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
            PaintingScheme.make_blanko(self.imageRes, zheFile)

        for r, c in regionAndColorPairs:
            print("")
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

    arguments:
    - idn := int, identifier for element
    - mode := all|mute|non-mute

    return:
    - `all elements not of idn`
    """
    def the_others(self, idn, mode = "non-mute"):
        if mode == "all":
            return [e for e in self.elements.values() if e.idn != idn]
        elif mode == "mute":
            return [e for e in self.elements.values() if e.idn != idn and e.mute]
        return [e for e in self.elements.values() if e.idn != idn and not e.mute]

    """
    description:
    - moves against all other elements
    """
    def move_elements(self, mode = "standard"):
        assert mode == "standard", "mode {} is invalid".format(mode)

        for k, v in self.elements.items():
            # mute element, no move
            if v.mute:
                continue

            oth = self.the_others(v.idn)
            v.move_one_timestamp(oth, self.typeShame, self.eventLogger.timeStamp, self.selfReproductionFrequency)

    """
    description:
    -
    """
    def update_visualization(self):
        ## TODO : add boolean switch for change here
        if self.assignElementsToRegion:
            self.assign_elements_to_region()
            self.paint_elements()

    """
    description:
    -
    """
    def move_one(self):
        self.update_language_stats()
        self.update_element_alignments()
        self.move_elements()
        self.update_language_stats()

        # update visualization and areas here
        self.update_visualization()
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

                print("LANGUAGE FOR EACH ELEMENT")
                for e in self.elements.values():
                    print("e : {}".format(e.activeWordCount))
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
        # get number of mute elements
        c = 0
        for k, e in self.elements.items():
            if e.is_mute(minThreshold = 0):
                c += 1

        if c >= len(self.elements) - 1:
            return True
        return False



    ######################### END : methods for moving one timestamp on gameboard ###############
