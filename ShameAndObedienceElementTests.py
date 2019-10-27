from GameBoard import *
import unittest

class ShameAndObedienceElementMethodsTest(unittest.TestCase):

    def setUp(self):
        self.testSample1 = ShameAndObedienceElementMethodsTest.test_sample_languages_1()

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
        print("X :\t", x.language)
        print("X2:\n", x.language.language)

    def test_ShameAndObedienceElement_GetDescriptorOverlapMeasures(self):

        """
        e = self.testSample1.elements[0]
        other = self.testSample1.elements[1:]
        """
        x = ShameAndObedienceElementMethodsTest.test_sample_ShameAndObedienceElement()
        e = x[0]
        other = x[1:]

        q = ShameAndObedienceElement.get_element_descriptor_overlap_measures(e, x[1])
        print("overlap m 1 :\t", q[0])
        print("overlap m 2 :\t", q[1])
        return

    def test_ShameAndObedienceElement_CalculateColorByColorTable(self):

        colorTable = {(0,0,0) : 1, (255,255,255) : 1}
        q = ShameAndObedienceElement.calculate_color_by_color_table(colorTable, roundDecimalPlaces = 2)
        print("q :\t", q)
        self.assertAlmostEqual((127.5, 127.5, 127.5), q)


if __name__ == "__main__":
    #ShameAndObedienceElementMethodsTest.test_ShameAndObedienceElement_Init()
    unittest.main()
