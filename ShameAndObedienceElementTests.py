from GameBoard import *
import unittest

## methods to test:
"""
def update_element_color_info_from_descriptor_overlaps(self, otherElements):
"""



class ShameAndObedienceElementMethodsTest(unittest.TestCase):

    def setUp(self):
        self.testSample1 = ShameAndObedienceElementMethodsTest.test_sample_languages_1()
        self.testSampleElements = ShameAndObedienceElementMethodsTest.test_sample_ShameAndObedienceElement()

    """
    description:
    - makes sample languages

    return:
    - list(`language`)
    """
    @staticmethod
    def test_sample_languages_1():

        c1 = {"dog", "whistle"}
        c2 = {"cat", "whistle"}
        c3 = {"dog", "cat", "mountain"}
        c4 = {"weird"}
        c5 = {"weird", "weird"}
        centroidsForEach = [c1,c2,c3,c4, c5]
        languages = []

        for (i, c) in enumerate(centroidsForEach):

            l = Language.random_by_centroid(idn = i, centroids = c, languageOutput = list,\
                        minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
            #print("LANGUAGE :\t", l)
            #print("\ncontents :\t", l.language)
            languages.append(l)
        return languages

    @staticmethod
    def test_sample_ShameAndObedienceElement():
        l = ShameAndObedienceElementMethodsTest.test_sample_languages_1()
        e = []

        for (i, l_) in enumerate(l):
            e_ = ShameAndObedienceElement(i, l_, (1,2,3))
            e.append(e_)
        return e
        ##dim = (8,8)
        ##return GameBoard(languages, dim)

    ################### START : methods test #######################################

    @staticmethod
    def test_ShameAndObedienceElement_Init():
        l = ShameAndObedienceElementMethodsTest.test_sample_languages_1()[0]
        x = ShameAndObedienceElement(1, l, (1,2,3))

    def test_ShameAndObedienceElement_GetElementDescriptorOverlapInfo(self):
        # try with [0] and [1]
        e1, e2 = self.testSampleElements[0], self.testSampleElements[1]
        q = ShameAndObedienceElement.get_element_descriptor_overlap_info(e1,e2, output = "counts")

        ##
        """
        print(e1.language)
        print(e2.language)
        print("overlap for e1 :\t", q[0])
        print("overlap for e2 :\t", q[1])
        """
        ##

        q2 = ShameAndObedienceElement.get_element_descriptor_overlap_info(e1,e2, output = "ratio")
        self.assertAlmostEqual(q[0] / len(e1.language.get_descriptors()), q2[0])
        self.assertAlmostEqual(q[1] / len(e2.language.get_descriptors()), q2[1])

        # try with [3] and [4]
        e3, e4 = self.testSampleElements[3], self.testSampleElements[4]
        q = ShameAndObedienceElement.get_element_descriptor_overlap_info(e3,e4, output = "counts")

        ##
        """
        print(e1.language)
        print(e2.language)
        print("overlap for e3 :\t", q[0])
        print("overlap for e4 :\t", q[1])
        """
        ##
        q2 = ShameAndObedienceElement.get_element_descriptor_overlap_info(e3,e4, output = "ratio")
        self.assertAlmostEqual((1,1), q2)

    """
    description:
    - pass of above test implies this tested function will work
    """
    def test_ShameAndObedienceElement_GetElementLanguageOverlapMeasures(self):
        return -1

    """
    description:
    -
    """
    def test_ShameAndObedienceElement_GetElementLanguageDisjointMeasures(self):
        ## def get_element_language_disjoint_measures(e1, e2):
        e1, e2 = self.testSampleElements[0], self.testSampleElements[1]
        d1, d2 = ShameAndObedienceElement.get_element_language_disjoint_measures(e1,e2)

        ###
        """
        print(e1.language)
        print()
        print(e2.language)
        """
        ###
        print("disjoint m1 :\t", d1)
        print("disjoint m2 :\t", d2)
        self.assertAlmostEqual(0.6153846153846154, d1, msg = "invalid disjoint [0]")
        self.assertAlmostEqual(0.5454545454545454, d2, msg = "invalid disjoint [1]")

    def test_ShameAndObedienceElement_CalculateColorByColorTable(self):
        colorTable = {(0,0,0) : 1, (255,255,255) : 1}
        q = ShameAndObedienceElement.calculate_color_by_color_table(colorTable, roundDecimalPlaces = 2)
        self.assertAlmostEqual((127, 127, 127), q)

    def test_ShameAndObedienceElement_Shame(self):
        q0, q1 = deepcopy(self.testSampleElements[0]), deepcopy(self.testSampleElements[1])

        # either one or the other chunks below need to be commented out
        # due to modification
        degree = 1
        typeShame = {"centroid"}

        print("HERE :\t", q0.get_active_centroids())
        x = q0.shame(q1, degree, typeShame)
        ##print("SHAME :\t", x)
        self.assertTrue(x == {'whistle', 'cat'}, "wrong shame")
        self.assertTrue(x == q1.prohibitedSpeech, "wrong prohibited speech")

        q0, q1 = deepcopy(self.testSampleElements[0]), deepcopy(self.testSampleElements[1])
        degree = 0.5
        x = q0.shame(q1, degree, typeShame)
        print("SHAME HERE :\t", x)
        self.assertTrue(len(x) == 1, "wrong shame 2")

        typeShame = {"centroid", "descriptor"}
        x = q0.shame(q1, degree, typeShame)
        print("SHAME :\t", x)

    def test_ShameAndObedienceElement_Align(self):
        q0, q1 = self.testSampleElements[0], self.testSampleElements[1]
        c, d = q0.align(q1, 0.1)
        self.assertTrue(c == ['dog'], "wrong align #1")

        d_ = sorted(d)
        x = sorted(['wolf', 'breeds', 'occurs', 'Canis', 'man', 'descended', 'many', 'member', 'since', 'common', 'times', 'prehistoric', 'domesticated', 'genus', 'probably'])
        self.assertTrue(d_ == x, "wrong align #2")

        """
        print("centroids")
        print(c)
        print()
        print("descriptors")
        print(d)
        """


# TODO : make an active_language variable.

if __name__ == "__main__":
    #ShameAndObedienceElementMethodsTest.test_ShameAndObedienceElement_Init()
    unittest.main()
