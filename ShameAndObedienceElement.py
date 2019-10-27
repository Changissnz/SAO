'''
this file is an extension of the Element class. Use this with Shame And Obedience
Simulation.
'''

from Element import *
from collections import Counter
import numpy as np

class ShameAndObedienceElement(Element):

    def __init__(self, idn, language, color):
        super().__init__(idn, language)
        self.classColor = deepcopy(color)
        self.currentColor = deepcopy(color)

        ## devising alignment scores for this element
        self.location = None
        self.shameObeyTable = None
        self.colorTable = {self.classColor : 1} # PaintingScheme will use this to paint world
        ##

    """
    description:
    - sets a region as location for instance
    """
    def set_location(self,region):
        assert FreeAndSimpleScanner.is_proper_region(region), "invalid region {}".format(region)
        self.location = region

    # TODO : test this.
    """
    description:
    - determines the centroids and descriptors that overlap between e1 and e2
    - uses set operations and casting
    - this value will be used to determine shame/obey values
    - does not consider prohibition

    arguments:
    - e1 :=
    - e2 :=

    return:
    - float::(overlap measure for e1), float::(overlap measure for e2)
    """
    @staticmethod
    def get_element_descriptor_overlap_measures(e1, e2):
        # both languages must be same type
        t1, t2 = LanguageMaker.get_standard_language_type(e1), LanguageMaker.get_standard_language_type(e2)
        assert t1 == t2, "incompatible languages!"
        if e1.descriptorCount == 0 or e2.descriptorCount == 0: return False # TODO remove this

        c,d = (set(),[])  if t1 == "l" else (set(), set())

        # convert descriptors to sets first and get existing
        # then get counts for each
        overlap = set(e1.language.language[1]) & set(e2.language.language[1])

        if t1 == "s":
            return len(overlap) / e1.descriptorCount, len(overlap) / e2.descriptorCount

        # get descriptor overlap
        # average out the counts
        counts1 = Counter(e1.language.language[1])
        counts2 = Counter(e2.language.language[1])
        overlapCount1, overlapCount2 = 0, 0
        for o in overlap:
            overlapCount1 += counts1[o]
            overlapCount2 += counts2[o]
        overlapRatio1 = overlapCount1 / e1.descriptorCount
        overlapRatio2 = overlapCount2 / e2.descriptorCount
        return overlapRatio1, overlapRatio2

    """
    description:
    - gets overlap measure with other elements

    arguments:
    - otherElements := list(`Element`)

    return:
    - list(float)::(length of size `otherElements`)
    """
    def get_element_descriptor_overlaps(self, otherElements):
        overlapRatios = []
        for e in otherElements:
            o1, _ = ShameAndObedienceElement.get_element_descriptor_overlap_measures(self, e)
            overlapRatios.append(o1)
        return overlapRatios

    """

    return:
    - dict, `color`->`measure`
    """
    # TODO : test this
    def update_element_color_info_from_descriptor_overlaps(self, otherElements):
        overlapRatios = self.get_element_descriptor_overlaps(otherElements)
        self.colorTable = {self.classColor : 1}
        for i, v in enumerate(overlapRatios):
            assert otherElements[i].location != None, "cannot operate on None location"
            self.colorTable[otherElements[i].classColor] = v

    # TODO : test this 
    def calculate_color_from_color_table(self, roundDecimalPlaces = 2):
        maxxy = 10 ** roundDecimalPlaces
        sequenceColors = []
        colorCounts = {}
        for k, v in self.colorTable.items():
            # perform rounding first
            self.colorTable[k] = round(v, roundDecimalPlaces)
            numColors = int(round(self.colorTable[k] * maxxy, 0))
            # get sequence of colors
            sequenceColors += [k for i in range(numColors)]

        sequenceColors = np.array(sequenceColors)
        return np.mean(sequenceColors, axis = 0)

    # shame is disjoint, obey is overlap
    def get_shame_obey_table(self):
        return -1

    def shame(self):
        return -1

    def move_against(self):
        x = random()

    ######## START : terminating condition for ShameAndObedienceElement

    """
    description:
    - determines if instance is still active based on non-prohibited words.
    """
    def is_mute(self, minSpeakingRatio):
        return -1


def test_ShameAndObedienceElement_GetElementDescriptorOverlapMeasures():
    return -1
