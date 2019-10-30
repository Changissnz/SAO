'''
this file is an extension of the Element class. Use this with Shame And Obedience
Simulation.
'''
# TODO : could add a `setOther` variable to some of the method names so that element
#        variables get set for both elements.

# TODO : need to devise `shameFunc` and `alignFunc`

##def make_func_float_weighted_by_history
from Element import *
from collections import Counter, defaultdict
import numpy as np
from math import ceil
from Functions import *

# alternative shame function can take into account other ratio values
# ex. : ratio of x(shame)/x(align), in which x is a function.
class ShameAndObedienceElement(Element):

    def __init__(self, idn, language, color):
        super().__init__(idn, language)
        assert LanguageMaker.get_language_type(language.language) == "standard", "invalid language type"
        self.classColor = deepcopy(color)
        self.currentColor = deepcopy(color)

        ## devising alignment scores for this element
        self.location = None
        self.shameObeyTable = None
        self.colorTable = {self.classColor : 1} # PaintingScheme will use this to paint world
        self.shameRange, self.alignRange = None, None
        self.shameFunc, self.alignFunc = None, None

        self.actionHistory = defaultdict(defaultdict) # keys are time stamps, values will consist of dict of form elementId->align|shame
        self.receiveHistory = defaultdict(defaultdict)

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
    - e1 := Element
    - e2 := Element

    return:
    - float::(overlap measure for e1), float::(overlap measure for e2)
    """
    @staticmethod
    def get_element_descriptor_overlap_measures(e1, e2):
        # both languages must be same type
        t1, t2 = LanguageMaker.get_standard_language_type(e1.language.language), LanguageMaker.get_standard_language_type(e2.language.language)
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
    - gets descriptor overlap between elements e1 and e2

    arguments:
    - e1 := Element
    - e2 := Element

    return:
    - set(`words`)
    """
    @staticmethod
    def get_element_descriptor_overlap(e1,e2):
        t1, t2 = LanguageMaker.get_standard_language_type(e1.language.language), LanguageMaker.get_standard_language_type(e2.language.language)
        assert t1 == t2, "incompatible languages!"
        if e1.descriptorCount == 0 or e2.descriptorCount == 0: return set() # TODO remove this

        # convert descriptors to sets first and get existing
        # then get counts for each
        overlap = set(e1.language.language[1]) & set(e2.language.language[1])
        return overlap

    """
    description:
    - gets descriptors found only in e1

    arguments:
    - e1 := Element
    - e2 := Element

    return:
    - set(`words`)
    """
    @staticmethod
    def get_element_descriptor_disjoint_from(e1, e2):
        t1, t2 = LanguageMaker.get_standard_language_type(e1.language.language), LanguageMaker.get_standard_language_type(e2.language.language)
        assert t1 == t2, "incompatible languages!"
        overlap = set(e1.language.language[1]) - set(e2.language.language[1])
        return overlap



    """
    description:
    - gets overlap measure with other elements

    arguments:
    - otherElements := list(`Element`)
    - setData` := bool, if class variable `shameAlign` gets set
    - output := list|dict

    return:
    - list(float)::(length of size `otherElements`)
    - dict(key::(elementId), value::(overlapRatio))
    """
    def get_element_descriptor_overlaps(self, otherElements, setData = True, output = list):
        overlapRatios = {} if output is dict else []
        if setData: self.shameObeyTable = {}

        for e in otherElements:
            o1, x = ShameAndObedienceElement.get_element_descriptor_overlap_measures(self, e)
            if output is list: overlapRatios.append(o1)
            else: overlapRatios[e.idn] = o1

            if setData:
                self.shameObeyTable[e.idn] = (o1,x) # ratio overlaps for e1 and other respectively
        return overlapRatios

    """

    arguments:
    - otherElements := list(`Element`)

    return:
    - dict, `color`->`measure`
    """
    # TODO : test this
    def update_element_color_info_from_descriptor_overlaps(self, otherElements):
        overlapRatios = self.get_element_descriptor_overlaps(otherElements, setData = True, output = list)
        self.colorTable = {self.classColor : 1}
        for i, v in enumerate(overlapRatios):
            ##assert otherElements[i].location != None, "cannot operate on None location"
            self.colorTable[otherElements[i].classColor] = v

    # TODO : test this
    @staticmethod
    def calculate_color_by_color_table(colorTable, roundDecimalPlaces = 2):
        maxxy = 10 ** roundDecimalPlaces
        sequenceColors = []
        colorCounts = {}
        for k, v in colorTable.items():
            # perform rounding first
            colorTable[k] = round(v, roundDecimalPlaces)
            numColors = int(round(colorTable[k] * maxxy, 0))
            # get sequence of colors
            sequenceColors += [k for i in range(numColors)]

        sequenceColors = np.array(sequenceColors)
        q = np.asarray(np.mean(sequenceColors, axis = 0), dtype = int)
        return tuple(q)

    # TODO : test this
    def update_color(self, otherElements, roundDecimalPlaces = 2):
        self.update_element_color_info_from_descriptor_overlaps(otherElements)
        self.currentColor = ShameAndObedienceElement.calculate_color_by_color_table(self.colorTable, roundDecimalPlaces)
        return self.currentColor

    """
    arguments:
    - element := Element
    - degree := 0 <= float <= 1
    - typeShame := {centroid}|{descriptor}|{centroid, descriptors}

    return:
    - set(`words`)
    """
    def shame(self, element, degree, typeShame):
        assert degree >= 0 and degree <= 1, "invalid degree {}".format(degree)

        # get random sample from each
        q = set()
        if "centroid" in typeShame:
            x = list(element.language.get_centroids())
            numToChoose = ceil(degree * len(x))
            r = sample(x, k = numToChoose)
            q.update(r)
        if "descriptor" in typeShame:
            x = list(element.language.get_descriptors())
            numToChoose = ceil(degree * len(x))
            r = sample(x, k = numToChoose)
            q.update(r)
        element.prohibitedSpeech.update(q)
        return q

    @staticmethod
    def mate_languages(e1, e2, degree):
        l = list(e1.language.get_centroids())

        # get number of disjoint centroids in e1
        dc = list(e1.language.language[0] - e2.language.language[0])
        requiredNumberOfWordsToMerge = ceil(len(dc) * degree)

        q = choices(dc, k = requiredNumberOfWordsToMerge)
        descriptors = LanguageMaker.get_descriptors(q, output = type(e2.language.get_descriptors()))
        e2.update_language_centroids(q, set())
        e2.update_language_descriptors(descriptors, set())
        return q, descriptors

    """
    description:
    - `align` is an operation that adds centroids from self to element based on degree
    """
    def align(self, element, degree):
        c, d= ShameAndObedienceElement.mate_languages(self, element, degree)
        return c,d

    """
    description:
    - class variables and related should be set before using this method
    - pertinent class variables include:
        - shameObeyTable
    """
    def move_against(self, otherElement, typeShame, timestamp = 1):
        toShameDegree, toAlignDegree = self.decide(otherElement.idn)
        s = self.shame(otherElement, toShameDegree, typeShame) # shame other element
        d = self.align(otherElement, toAlignDegree)

        self.log_action("shame", toShameDegree, timestamp)
        self.log_received(otherElement.idn, "shame", toShameDegree, timestamp)
        self.log_action("align", toShameDegree, timestamp)
        self.log_received(otherElement.idn, "align", toShameDegree, timestamp)

    def log_action(self, typeAction, degree, timestamp):
        assert typeAction in {"shame", "align"}, "typeAction {} invalid".format(typeAction)
        self.actionHistory[timestamp][self.idn][typeAction] = degree

    def log_received(self, otherElementId, typeAction, degree, timestamp):
        assert typeAction in {"shame", "align"}, "typeAction {} invalid".format(typeAction)
        self.receiveHistory[timestamp][otherElementId][typeAction] = degree

    """
    description:
    - determines shame and align degree for other element

    arguments:
    - otherElementIdn := int,
    """
    def decide(self, otherElementIdn):
        s, a = self.shameObeyTable[otherElementIdn]
        shameDegree, alignDegree = self.shameFunc(s), self.alignFunc(a)
        return shameDegree, alignDegree

    ######## START : terminating condition for ShameAndObedienceElement

    """
    description:
    - determines if instance is still active based on non-prohibited words.
    """
    def is_mute(self, minSpeakingRatio):
        return -1
