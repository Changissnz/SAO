from GameBoard import *
import unittest

class ShameAndObedienceElementMethodsTest(unittest.TestCase):

    def setUp(self):
        self.testSample1 = ShameAndObedienceElementMethodsTest.test_sample_1()

    """
    description:
    - makes a game board
    """
    @staticmethod
    def test_sample_1():

        c1 = {"dog", "whistle"}
        c2 = {"cat", "whistle"}
        c3 = {"dog", "cat", "mountain"}
        c4 = {"weird"}
        centroidsForEach = [c1,c2,c3,c4]
        languages = []

        for (i, c) in enumerate(centroidsForEach):

            l = Language.random_by_centroid(idn = i, centroids = c, languageOutput = list,\
                        minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
            print("LANGUAGE :\t", l)
            print("\ncontents :\t", l.language)
            languages.append(l)

        dim = (8,8)
        return GameBoard(languages, dim)


    def test_ShameAndObedienceElement_get_descriptor_overlap_measures(self):

        e = self.testSample1.elements[0]
        other = self.testSample1.elements[1:]

        q = ShameAndObedienceElement.get_element_descriptor_overlap_measures(e, other)

        print("overlap m 1 :\t", q[0])
        print("overlap m 2 :\t", q[1])

        return




if __name__ == "__main__":
    unittest.main()
