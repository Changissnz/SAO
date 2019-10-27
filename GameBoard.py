'''
update on GameBoard, specialized for shame and obedience element
'''
from ShameAndObedienceElement import *
from GameBoardHandler import *
from math import sqrt

class GameBoard:

    """
    description:
    -

    arguments:
    - languageInfo := int|list(`languages`)
    - dimensions := (int,int)
    """
    def __init__(self, languageInfo, dimensions, maxNumLanguages = 52):
        self.dimensions = dimensions
        self.area = self.dimensions[0] * self.dimensions[1]
        self.wordCoordinates = {} ## these are not used for Shame And Obedience
        self.centroidCoordinates = None ## these are not used for Shame And Obedience
        self.set_languages(languageInfo, maxNumLanguages = maxNumLanguages)
        self.get_element_stats()
        self.assign_elements_to_region()

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
        self.elements = []

        i = 0
        for l, c in zip(languages, colors):
            s = ShameAndObedienceElement(i, l, c)
            self.elements.append(s)
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
        for e in self.elements:
            d[e.idn] = e.get_language_stats_with_prohibition()
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

    # TODO : test this, make argument for alternative config alg.
    """
    description:
    - assigns elements to region after alreading setting element stats
    """
    def assign_elements_to_region_(self):

        def get_element_dim_from_ratio(r):
            assert r >= 0 and r <= 1, "invalid r {}".format(r)
            elemArea = r * self.area
            return round(sqrt(elemArea), 4)

        # get element dimensions
        elementDim = []
        for k, v in self.elementLanguageRatio.items():
            q = get_element_dim_from_ratio(v)
            elementDim.append((k,(q,q)))

        config, areaDiff = GameBoardHandler.get_best_config_by_random_inspection(elementDim,\
            self.dimensions)

        if len(config) < len(self.elements):
            return False
        return config, areaDiff


    def assign_elements_to_region(self):
        q = self.assign_elements_to_region_()
        if q == False: return False
        self.config, self.configAreaDiff = q[0],q[1]

    ################# END : methods below used to calculate the element-to-region assignment
