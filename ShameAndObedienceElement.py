'''
this file is an extension of the Element class. Use this with Shame And Obedience
Simulation.
'''
from Element import *
from collections import Counter, defaultdict
import numpy as np
from math import ceil
from Functions import *

class ShameAndObedienceElement(Element):

    def __init__(self, idn, language, color):
        super().__init__(idn, language)
        assert LanguageMaker.get_language_type(language.language) == "standard", "invalid language type"
        self.classColor = deepcopy(color)
        self.currentColor = deepcopy(color)

        ## devising alignment scores for this element
        self.location = None
        self.shameObeyTable = {}
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
    - output := counts|ratio

    return:
    - float::(overlap measure for e1), float::(overlap measure for e2)
    """
    @staticmethod
    def get_element_descriptor_overlap_info(e1, e2, output = "counts"):
        # both languages must be same type
        t1, t2 = LanguageMaker.get_standard_language_type(e1.language.language), LanguageMaker.get_standard_language_type(e2.language.language)
        assert t1 == t2, "incompatible languages!"
        assert output in {"counts", "ratio"}, "output {} is invalid".format(output)

        if e1.descriptorCount == 0 or e2.descriptorCount == 0: return False # TODO remove this

        c,d = (set(),[])  if t1 == "l" else (set(), set())

        # convert descriptors to sets first and get existing
        # then get counts for each
        overlap = set(e1.language.language[1]) & set(e2.language.language[1])

        if t1 == "s":
            if output == "counts":
                return len(overlap), len(overlap)
            return len(overlap) / e1.descriptorCount, len(overlap) / e2.descriptorCount

        # get descriptor overlap
        # average out the counts
        counts1 = Counter(e1.language.language[1])
        counts2 = Counter(e2.language.language[1])
        overlapCount1, overlapCount2 = 0, 0
        for o in overlap:
            overlapCount1 += counts1[o]
            overlapCount2 += counts2[o]

        if output == "counts":
            return overlapCount1, overlapCount2

        overlapRatio1 = overlapCount1 / e1.descriptorCount
        overlapRatio2 = overlapCount2 / e2.descriptorCount
        return overlapRatio1, overlapRatio2

    """
    description:
    - calculates the measure that takes into account the number of words that
      intersects between e1.language and e2.language

    arguments:
    - e1 := Element
    - e2 := Element

    return:
    - float::(`measure for e1`), float::(`measure for e2`)
    """
    @staticmethod
    def get_element_language_overlap_measures(e1,e2):
        t1, t2 = LanguageMaker.get_standard_language_type(e1.language.language), LanguageMaker.get_standard_language_type(e2.language.language)
        assert t1 == t2, "incompatible languages!"
        if e1.wordCount == 0 or e2.wordCount == 0: return 0,0 # TODO remove this
        dc1, dc2 = ShameAndObedienceElement.get_element_descriptor_overlap_info(e1, e2, output = "counts")
        centroidCount = len(e1.language.get_centroids() & e2.language.get_centroids())
        return dc1 / e1.wordCount, dc2 / e2.wordCount

    """
    description:
    - calculates element disjoint measures based on the number of their disjoint
      terms

    arguments:
    - e1 := Element
    - e2 := Element

    return:
    - float::(`measure for e1`), float::(`measure for e2`)
    """
    @staticmethod
    def get_element_language_disjoint_measures(e1, e2):
        c1 = e1.language.language[0] - e2.language.language[0]
        d1 = ShameAndObedienceElement.get_element_descriptor_disjoint_from(e1,e2)
        #print("C1 {}:\t{}".format(len(c1), c1))
        #print("D1 {}:\t{}".format(len(d1), d1))
        c2 = e2.language.language[0] - e1.language.language[0]
        d2 = ShameAndObedienceElement.get_element_descriptor_disjoint_from(e2,e1)

        if LanguageMaker.get_standard_language_type(e1.language.language) == "l":
            desc1 = len([l for l in e1.language.language[1] if l in d1])
            desc2 = len([l for l in e2.language.language[1] if l in d2])
            x1, x2 = len(c1) + desc1, len(c2) + desc2
        else:
            x1, x2 = len(c1) + len(d1), len(c2) + len(d2)

        #print("desc1 :\t{}\tdesc2 :\t{}".format(desc1, desc2))
        #print("c1 {}\tc2 {}\t".format(x1, x2))
        return x1 / e1.wordCount, x2 / e2.wordCount


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
    def get_element_language_measures(self, otherElements, setClassVar = False):

        if setClassVar:
            self.shameObeyTable = {}
        else:
            out = {}

        for e in otherElements:
            ov1, ov2 = self.get_element_language_overlap_measures(self, e)
            d1, d2 = self.get_element_language_disjoint_measures(self, e)
            #print("HERE :\t", ov1, ov2)
            if setClassVar:
                self.shameObeyTable[e.idn] = (ov1, d1)
            else:
                out[e.idn] = (ov1,d1)

        if setClassVar: return deepcopy(self.shameObeyTable)
        return out

    """
    description:
    - calculates element descriptor overlap measure

    arguments:
    - otherElements := list(`Element`)

    return:
    - list(int)
    """
    def get_element_descriptor_overlaps(self, otherElements):
        ratios = []
        for e in otherElements:
            o1, _ = ShameAndObedienceElement.get_element_descriptor_overlap_info(self, e, output = "ratio")
            ratios.append(o1)
        return ratios

    """

    arguments:
    - otherElements := list(`Element`)

    return:
    - dict, `color`->`measure`
    """
    # TODO : test this
    def update_element_color_info_from_descriptor_overlaps(self, otherElements):
        overlapRatios = self.get_element_descriptor_overlaps(otherElements)
        self.colorTable = {self.classColor : 1} # reset to default
        for i, v in enumerate(overlapRatios):
            self.colorTable[otherElements[i].classColor] = v

    # TODO : test this
    """
    description:
    - calculates color of element by averaging color in colorTable

    arguments:
    - colorTable := dict, key is color, value is float ratio
    - roundDecimalPlaces := int

    return:
    - tuple::(size 3)
    """
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
    """
    description:
    - updates color for each round

    arguments:
    - otherElements := list(`Element`)

    return:
    - `color`
    """
    def update_color(self, otherElements, roundDecimalPlaces = 2):
        self.update_element_color_info_from_descriptor_overlaps(otherElements)
        self.currentColor = ShameAndObedienceElement.calculate_color_by_color_table(self.colorTable, roundDecimalPlaces)
        return self.currentColor

    ###################### START : shame and align functions here

    """
    description:
    - shames the other element's language by `degree` of reference `shameReference`
    arguments:
    - element := Element
    - degree := 0 <= float <= 1
    - typeShame := {centroid}|{descriptor}|{centroid, descriptors}
    - shameReference := self|other

    return:
    - set(`words`)
    """
    def shame(self, element, degree, typeShame, shameReference = "other"):
        assert degree >= 0 and degree <= 1, "invalid degree {}".format(degree)
        assert shameReference in {"self", "other"}, "invalid shameReference {}".format(shameReference)

        # get random sample from each

        ## TODO : relocate these to better locations
        self.update_language_stats()
        element.update_language_stats()

        q = set()
        if "centroid" in typeShame:
            x = element.get_active_centroids()
            ##print("ACTIVE CENTROIDS :\t", x)
            if shameReference == "self":
                numToChoose = min(ceil(degree * self.activeCentroidCount), self.activeCentroidCount)
                ##print("DEGREE AND ACTIVE :\t", degree, self.activeCentroidCount)
            else:
                numToChoose = min(ceil(degree * element.activeCentroidCount), element.activeCentroidCount)
                ##print("DEGREE AND ACTIVE :\t", degree, element.activeCentroidCount)

            ##print("LEN X :\{}\t{}".format(len(x), numToChoose))
            r = sample(x, k = numToChoose)
            q.update(r)
        if "descriptor" in typeShame:
            x = element.get_active_descriptors()

            if shameReference == "self":
                numToChoose = min(ceil(degree * self.activeDescriptorCount), self.activeDescriptorCount)
                ##print("DEGREE AND ACTIVE :\t", degree, self.activeDescriptorCount)
            else:
                numToChoose = min(ceil(degree * element.activeDescriptorCount), element.activeDescriptorCount)
                ##print("DEGREE AND ACTIVE :\t", degree, element.activeDescriptorCount)
            ##print("LEN Y :\{}\t{}".format(len(x), numToChoose))
            r = sample(x, k = numToChoose)
            q.update(r)
        element.prohibitedSpeech.update(q)
        return q

    """
    description:
    - mates languages by adding `degree` of e1.language to e2.language

    arguments:
    - e1 := Element
    - e2 := Element
    - degree := float

    return:
    - `centroids to add to e2`, `descriptors to add to e2`
    """
    @staticmethod
    def mate_languages(e1, e2, degree):
        l = list(e1.language.get_centroids())

        # get number of disjoint centroids in e1
        dc = list(e1.language.language[0] - e2.language.language[0])
        requiredNumberOfWordsToMerge = ceil(len(dc) * degree)
        q = choices(dc, k = requiredNumberOfWordsToMerge)

        # generate descriptions for set of words
        x = LanguageMaker.get_descriptors(q, output = type(e1.language.language[1]))
        e2.update_language_centroids(q, set())
        e2.update_language_descriptors(x, set())
        return q, x

    """
    description:
    - `align` is an operation that adds centroids from self to element based on degree
    """
    def align(self, element, degree):
        self.update_language_stats()
        element.update_language_stats()
        c, d= ShameAndObedienceElement.mate_languages(self, element, degree)
        return c,d

    """
    description:
    - class variables and related should be set before using this method
    - pertinent class variables include:
        - shameObeyTable
    """
    def move_against(self, otherElement, typeShame, timestamp):
        toShameDegree, toAlignDegree = self.decide(otherElement.idn)

        s = self.shame(otherElement, toShameDegree, typeShame) # shame other element
        d = self.align(otherElement, toAlignDegree)
        #print("SHAME? :\t", toShameDegree)
        #print("ALIGN? :\t", toAlignDegree)
        self.log_timestamp_events(otherElement.idn, toShameDegree, toAlignDegree, timestamp)

    # TODO : return change in size
    """
    description:
    -

    arguments:
    - otherElements :=
    - typeShame :=
    - timestamp := int, >= 0
    - reproduceInfo := (int::(frequency), int::(degree))
    """
    def move_one_timestamp(self, otherElements, typeShame, timestamp, reproduceInfo):
        # move against all other elements
        for e in otherElements:
            self.move_against(e, typeShame, timestamp)

        # reproduce and generate
        self.do_self_actions_standard(reproduceInfo[0], reproduceInfo[1])


    ######################## START : deciding and recording things #########################

    def log_timestamp_events(self, otherElementIdn, toShameDegree, toAlignDegree, timestamp):
        self.log_action("shame", otherElementIdn, toShameDegree, timestamp)
        self.log_received("shame", otherElementIdn, toShameDegree, timestamp)
        self.log_action("align", otherElementIdn, toAlignDegree, timestamp)
        self.log_received("align", otherElementIdn, toAlignDegree, timestamp)

    """
    description:
    - logs action given variables

    arguments:
    - typeAction := shame|align
    - elementIdn := int
    - degree := 0 <= float <= 1
    - timestamp := int, unit-of-time with respect to game
    """
    def log_action(self, typeAction, elementIdn, degree, timestamp):
        assert typeAction in {"shame", "align"}, "typeAction {} invalid".format(typeAction)

        if elementIdn in self.actionHistory[timestamp]:
            self.actionHistory[timestamp][elementIdn][typeAction] = degree
        else:
            self.actionHistory[timestamp][elementIdn] = {}
            self.actionHistory[timestamp][elementIdn][typeAction] = degree


    """
    description:
    - logs receive given variables

    arguments:
    - typeAction := shame|align
    - degree := 0 <= float <= 1
    """
    def log_received(self, typeAction, otherElementId, degree, timestamp):
        assert typeAction in {"shame", "align"}, "typeAction {} invalid".format(typeAction)

        if otherElementId in self.receiveHistory[timestamp]:
            self.receiveHistory[timestamp][otherElementId][typeAction] = degree
        else:
            self.receiveHistory[timestamp][otherElementId] = {}
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
        #print("SHAME {}/{} OBEY {}/{}".format(s, shameDegree, a, alignDegree))
        return shameDegree, alignDegree

    ######################## END : deciding and recording things #########################

    ######## START : terminating condition for ShameAndObedienceElement ##################

    def display_alignments(self):
        print("displaying alignments for : {}".format(self.idn))
        for k, v in self.shameObeyTable.items():
            print("key : {}\tvalue : {}".format(k, v))

    def display_history(self):
        print("** displaying history for : {}".format(self.idn))
        print("\t* action history")
        for k, v in self.actionHistory.items():
            print("{} : {}".format(k, v))
        print()
        print()
        print("\t* receive history")
        for k, v in self.receiveHistory.items():
            print("{} : {}".format(k, v))

    """
    description:
    - determines if instance is still active based on non-prohibited words.
    """
    def is_mute(self, minSpeakingRatio):
        return -1
