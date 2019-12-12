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
            pixelRes = (400, 400), typeShame = {"centroid", "descriptor"},\
            selfReproductionFrequency = (1, 0.05), actionFunctions = None):
        assert len(languageInfo) < 12, "Shame And Obedience accepts a maximum of 12 elements"
        assert ShameAndObedienceGameBoard.is_valid_pixel_res(pixelRes), "invalid pixelRes {}".format(pixelRes)
        assert actionFunctions != None, "cannot proceed without any actions"

        super().__init__(languageInfo, dimensions, 12, assignElementsToRegion = assignElementsToRegion)
        self.pixelRes = pixelRes
        self.imageRes = ShameAndObedienceGameBoard.dim_to_square_dim(self.pixelRes)
        self.typeShame = typeShame
        self.selfReproductionFrequency = selfReproductionFrequency
        self.update_element_colors()
        PaintingScheme.make_blanko(self.pixelRes)
        self.eventLogger = EventHistory(1, None)
        self.set_action_functions(actionFunctions)
        self.set_element_action_functions_uniform()

        # visualization here
        self.visualizeCounter = 0
        print("******************************************************PAINTING")
        self.paint_elements()
        self.finish = False

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

    def paint_element(self, elementIndex, zheFile = "defaultPitcherOfEmotions.png"):

        q = self.elements[elementIndex]
        if q.location != None:
            x = PaintingScheme.convert_region_to_pixel_region(q.location, self.dimensions, self.imageRes)
            PaintingScheme.paint_image_given_pixel_region_and_color(x, q.currentColor, zheFile = zheFile)
            return

    def paint_elements(self, zheFile = "defaultPitcherOfEmotions.png", mode = "clear first"):
        assert mode in {"clear first", None}

        if self.assignElementsToRegion is False: return

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
            PaintingScheme.paint_image_given_pixel_region_and_color(r, c, zheFile = zheFile)
        return True

    ######################### END : methods for visualization here ###############

    ######################### START : methods for moving one timestamp on gameboard ###############

    """
    description:
    - updates language stats for each element,
      active descriptor and word counts.
    """
    def update_language_stats(self):
        for e in self.elements.values():
            e.update_language_stats()
        self.get_element_stats() # TODO : relocate


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
    - updates visualization depending on interval
    """
    def update_visualization(self):
        ## TODO : add boolean switch for change here
        if self.assignElementsToRegion is False:
            return
        self.visualizeCounter += 1
        if self.visualizeCounter % self.assignElementsToRegion[1] == 0:
            print("^ updating visual")
            self.visualizeCounter = 0
            self.assign_elements(self.assignElementsToRegion)
            self.paint_elements()

    #########################33 START : below methods need to be checked.

    """
    description:
    -
    """
    def move_one(self, calibrateSize = False):
        if self.finish: return

        self.update_language_stats()
        self.update_element_alignments()
        self.move_elements()
        self.update_language_stats()

        # update visualization and areas here
        self.update_visualization()

        # REFACTOR
        # update history here
        self.eventLogger.log(self)
        self.finish = self.termination_condition_mute()

        if calibrateSize != False:
            sizeCap, shrinkRatio = calibrateSize
            self.calibrate_size(sizeCap, shrinkRatio)

    def run(self, numRounds = None):
        # set shame and align functions first
        self.set_element_action_functions_uniform()

        # run a maximum of `numRounds`
        if numRounds != None:
            for _ in range(numRounds):
                self.move_one()
                if self.termination_condition_mute():
                    break
            return

        while self.termination_condition_mute() == False:
            self.move_one()

    ######################### END : methods for moving one timestamp on gameboard ###############

    ######################### START : termination and calibration methods #####################################

    """
    description:
    - calibrates the element languages if their total size exceeds some size cap,
      to `shrinkRatio`
    - for each language, will remove equal ratios for centroids and descriptors

    arguments:
    - sizeCap := int, integer limit before calibrating size
    - shrinkRatio := 0 <= float <= 1, determines the size to shrink languages to

    return:
    - dict(`new element sizes`)
    """
    def calibrate_size(self, sizeCap, shrinkRatio):
        assert shrinkRatio >= 0 and shrinkRatio <= 1, "invalid shrinkRatio"

        def shrink_language(element, wantedMaxSize):
            assert wantedMaxSize > 0, "invalid max size"
            # get number of actives
            q1, q2 = element.activeCentroidCount, element.activeDescriptorCount
            r = element.activeDescriptorCount // element.activeCentroidCount

            q = element.activeWordCount

            # get remove info
            numCentroidsToRemove, numDescriptorsToRemove = 0, 0
            while q > wantedMaxSize:
                numDescriptorsToRemove += r
                numCentroidsToRemove += 1
                q = element.activeWordCount - (numDescriptorsToRemove + numCentroidsToRemove)

            # pick and remove
            l_ = list(element.get_active_descriptors())
            s = sample(l_, k = numDescriptorsToRemove)
            element.update_language_descriptors(set(), s)

            l_ = list(element.get_active_centroids())
            s = sample(l_, k = numCentroidsToRemove)
            element.update_language_centroids(set(), s)

        q = sum(e.activeWordCount for e in self.elements.values())
        if q == 0: return

        if q >= sizeCap:
            newSz = ceil(sizeCap * shrinkRatio)

            # get wantedSizes of sizes for each element
            wantedSizes = {}
            for k,v in self.elements.items():
                wantedSizes[k] = ceil(v.activeWordCount / q * newSz)

            # shrink each language based on wanted size
            for k, v in wantedSizes.items():
                shrink_language(self.elements[k], v)


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

    ######################### END : termination and calibration methods #####################################
