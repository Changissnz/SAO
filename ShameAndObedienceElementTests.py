from GameBoard import *
import unittest

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
        centroidsForEach = [c1,c2,c3,c4]
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

    @staticmethod
    def test_ShameAndObedienceElement_Init():
        l = ShameAndObedienceElementMethodsTest.test_sample_languages_1()[0]

        x = ShameAndObedienceElement(1, l, (1,2,3))

    def test_ShameAndObedienceElement_GetDescriptorOverlapMeasures(self):

        """
        e = self.testSample1.elements[0]
        other = self.testSample1.elements[1:]
        """
        x = ShameAndObedienceElementMethodsTest.test_sample_ShameAndObedienceElement()
        e = x[0]
        other = x[1:]

        q = ShameAndObedienceElement.get_element_descriptor_overlap_measures(e, x[1])
        self.assertAlmostEqual(q[0], 0.375)
        self.assertAlmostEqual(q[1], 0.45)
        print("overlap m 1 :\t", q[0])
        print("overlap m 2 :\t", q[1])
        return

    def test_ShameAndObedienceElement_CalculateColorByColorTable(self):

        colorTable = {(0,0,0) : 1, (255,255,255) : 1}
        q = ShameAndObedienceElement.calculate_color_by_color_table(colorTable, roundDecimalPlaces = 2)
        self.assertAlmostEqual((127, 127, 127), q)

    def test_ShameAndObedienceElement_Shame(self):
        q0, q1 = self.testSampleElements[0], self.testSampleElements[1]

        degree = 1
        typeShame = {"centroid"}

        x = q0.shame(q1, degree, typeShame)
        self.assertTrue(x == {'whistle', 'cat'}, "wrong shame")
        self.assertTrue(x == q1.prohibitedSpeech, "wrong prohibited speech")

        degree = 0.5
        x = q0.shame(q1, degree, typeShame)
        self.assertTrue(len(x) == 1, "wrong shame 2")

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

if __name__ == "__main__":
    #ShameAndObedienceElementMethodsTest.test_ShameAndObedienceElement_Init()
    unittest.main()
