'''
update on GameBoard, specialized for shame and obedience element
'''
from ShameAndObedienceElement import *
from math import sqrt

# assignElementsToRegion needs to go from False -> "assignMode"
# add variable to this method : assign_elements_to_region
class GameBoard:

    """
    description:
    -

    arguments:
    - languageInfo := int|list(`languages`)
    - dimensions := (int,int)
    - maxNumLanguages := int, maximum languages supported
    - assignElementsToRegion := False|((t/e|fit)::assignmentMode, int::(assignFrequency))

    return:
    -
    """
    def __init__(self, languageInfo, dimensions, maxNumLanguages = 52, assignElementsToRegion = False):
        self.dimensions = dimensions
        self.area = self.dimensions[0] * self.dimensions[1]
        self.wordCoordinates = {} ## these are not used for Shame And Obedience
        self.centroidCoordinates = None ## these are not used for Shame And Obedience
        self.config, self.configAreaDiff = None, None
        self.set_languages(languageInfo, maxNumLanguages = maxNumLanguages)
        self.get_element_stats()
        self.assignElementsToRegion = assignElementsToRegion
        self.assign_elements(self.assignElementsToRegion)
        self.roundNumber = 0 

    # TODO : test this.
    '''
    - color is 3-tuple, each value is 0-255
    '''
    @staticmethod
    def generate_colors(numColors):
        assert numColors > 0, "invalid numColors {}".format(numColors)
        # uses a color-distance division scheme based on numColors
        # default first is black
        c = (0,0,0)
        colors = [c]
        if numColors == 1: return colors

        maxDistancePerIndex = 255
        hopPerIndex = maxDistancePerIndex // (numColors - 1)

        numColors -= 1
        while numColors > 0:
            c = (c[0] + hopPerIndex, c[1] + hopPerIndex, c[2] + hopPerIndex)
            colors.append(c)
            numColors -= 1
        return colors

    """
    description:
    - calculates area of gameboard

    return:
    - float
    """
    def get_area(self):
        return self.dimensions[0] * self.dimensions[1]

    # TODO : test
    '''
    description:
    - declares ShameAndObedienceElement instances using `languageInfo`

    arguments:
    - languageInfo := int|list(`languages`)
    '''
    def set_languages(self, languageInfo, maxNumLanguages):
        if type(languageInfo) is int:
            assert languageInfo <= maxNumLanguages, "cannot operate on more than {} elements".format(maxNumLanguages)
            languages = LanguageMaker.get_languages(n = languageInfo, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
        elif type(languageInfo) is list: # list of languages
            assert len(languageInfo) <= maxNumLanguages, "cannot operate on more than {} elements".format(maxNumLanguages)
            languages = languageInfo
        else:
            raise IOError("invalid languageInfo {}".format(languageInfo))

        # make colors for languages
        colors = GameBoard.generate_colors(len(languages))
        self.elements = {}

        i = 0
        for l, c in zip(languages, colors):
            s = ShameAndObedienceElement(i, l, c)
            self.elements[i] = s
            i += 1

    def get_element_stats(self):
        self.elementLanguageCount = self.get_element_stats_on_language()
        self.elementLanguageRatio = self.get_element_stats_on_language_by_ratio(self.elementLanguageCount)

    # TODO : test this
    """
    description:
    - calculates a dictionary of key element id and value their language stat
      with prohibition

    return:
    - dict(int : int)
    """
    def get_element_stats_on_language(self):
        d = {}
        for k, v in self.elements.items():
            d[k] = v.get_language_stats_with_prohibition()
        return d

    # TODO : test this
    """
    description:
    - averages values by sum from output of method above

    arguments:
    - q := None|dict::(element stats literal counts)

    return:
    - dict(int : float)
    """
    def get_element_stats_on_language_by_ratio(self, q = None):
        if q == None:
            q = self.get_element_stats_on_language()
        s = sum(q.values())

        if s != 0:
            return {k : v/s for k,v in q.items()}
        return False

    ################# START : methods below used to calculate the element-to-region assignment

    """
    description: 
    - calculates the wanted square region for element based on ratio 
    
    arguments: 
    - r := 0 <= x <= 1
    
    return: 
    - float::area 
    """ 
    def get_element_dim_from_ratio(self, r):
        assert r >= 0 and r <= 1, "invalid r {}".format(r)
        elemArea = r * self.area
        return round(sqrt(elemArea), 4)

    """
    description:
    - assigns elements to region after alreading setting element stats. `elementRatioScale` determines the proportion of the gameboard the elements
      occupy, 1 means area of all elements equals gameboard, 0 means none.

    arguments:
    - requiredFit := False|int::(positive), number of times to attempt fitting elements to gameboard
    - elementRatioScale := 0 <= float <= 1

    return:
    - `configInfo`, `areaDiff`
    """
    def assign_elements_to_region_(self, requiredFit, elementRatioScale):
        assert elementRatioScale >= 0 and elementRatioScale <= 1, "elementRatioScale {} invalid".format(elementRatioScale)

        # get element dimensions
        elementDim = self.get_element_dimensions(elementRatioScale = elementRatioScale)
        config, areaDiff = GameBoardHandler.get_best_config_by_random_inspection(elementDim,\
            self.dimensions, numRandomPoints = 2, cutOff = "auto")
        if type(requiredFit) is int:
            if requiredFit == 0:
                return config, areaDiff

            if len(config) < len(self.elements):
                return self.assign_elements_to_region_(requiredFit -1, elementRatioScale)

        return config, areaDiff

    """
    description:
    - assigns elements to region depending on some mode,
    """
    def assign_elements_to_region_by_fit(self, requiredFit = 0, elementRatioScale = 1):
        q = self.assign_elements_to_region_(requiredFit, elementRatioScale)
        if q == False: return False
        self.config, self.configAreaDiff = q[0],q[1]
        self.assign_to_elements_helper()

    """
    description:
    - assigns elements to region using some either fit-assignment or random assignment

    arguments:
    - assignElementsToRegion := False|((t/e|fit)::assignmentMode, int::(assignFrequency))
    """
    # TODO : add arguments here
    def assign_elements(self, assignElementsToRegion):

        if assignElementsToRegion is False:
            return

        assert assignElementsToRegion[0] in {"t/e", "fit"} and\
            type(assignElementsToRegion[1]) is int and len(assignElementsToRegion) == 2,\
            "invalid assignElementsToRegion {}".format(assignElementsToRegion)

        if assignElementsToRegion[0] == "fit":
            self.assign_elements_to_region_by_fit() # gets best fit
        else:
            self.assign_elements_to_region_by_trial_and_error() #

    """
    description:
    - calculates element dimensions from its ratio of game language.

    arguments:
    ~

    return:
    - list::((`id`, `dim`:(int,int)))
    """
    def get_element_dimensions(self, elementRatioScale = 1):
        # get element dimensions
        elementDim = []
        for k, v in self.elementLanguageRatio.items():
            q = self.get_element_dim_from_ratio(v)
            q = elementRatioScale * q
            elementDim.append((k,(q,q)))
        return elementDim

    """
    description:
    ~

    arguments:
    ~
    """
    def assign_elements_to_region_by_trial_and_error(self):
        ei = self.get_element_dimensions()
        self.config, self.configAreaDiff =\
            GameBoardHandler.get_best_config_by_trial_and_error(ei, self.dimensions, numTrials = 10)
        self.assign_to_elements_helper()

    """
    description:
    - assigns locations from `self.config` to `self.elements`
    """
    # TODO : test this
    def assign_to_elements_helper(self):
        for c in self.config:
            idn = c[0]
            reg = c[2]
            self.elements[idn].set_location(reg)
            
    ################# END : methods below used to calculate the element-to-region assignment