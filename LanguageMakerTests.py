from LanguageMaker import *
import unittest

class LanguageMakerMethodsTest(unittest.TestCase):

    def test_Language_GetTfidfMeasure(self):
        return -1

    '''
    description:
    - checks the size of descriptors of bag for minimum size requirement
    '''
    # TODO : check first chunk code
    @staticmethod
    def test_LanguageMaker_GetDescriptorsForBag():
        x = LanguageMaker()
        bow = x.fetch_nonstop_words(100)
        desc = x.get_descriptors_for_bag(bow, 100)
        if desc is None:
            print("desk is None")
        assert len(desc) >= 100, "desc is len {}, want at least 100".format(len(desc))

        bow = x.fetch_nonstop_words(100)
        desc = x.get_descriptors_for_bag_try_except(bow, 100, "const")
        if desc is None:
            print("desk is None")
        assert len(desc) == 100, "desc is len {}, want exactly 100".format(len(desc))

    # TODO : make assertions for methods below
    #-----------------------------------------------------
    @staticmethod
    def LanguageMaker_GetDescriptorsForBag_ContentsTest():
        x = LanguageMaker()
        bow = x.fetch_nonstop_words(1)
        bow = {"* metamorphoses"}
        print("* word to look at :\n{}".format(bow))
        desc = x.get_descriptors_for_bag(bow, 100)
        print("* descriptors :\n")
        print(desc)

    def test_LanguageMaker_GetListOfDescriptors_ContentsTest(self):
        q = LanguageMaker.get_list_of_descriptors(100, 5, mode = "geq")

    def test_LanguageMaker_GetLanguagesByContentSamples(self):
        centroidsForEach = [{"dog", "whale"}, {"cat", "rhino"}, {"water"}, {"hydrogen"}]
        q = LanguageMaker.get_languages_by_content_standard(centroidsForEach, outputForEach = list)

    @staticmethod
    def test_LanguageMaker_GetLanguages():
        q = LanguageMaker.get_languages_standard(5, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
        print("languages\n")
        for q_ in q:
            print("*\t{}".format(q_))
            print()

    @staticmethod
    def test_LanguageMaker_GetLanguagesByContentStandard():
        centroids = [{"dog", "whale"}]
        l = LanguageMaker.get_languages_by_content_standard(centroids, outputForEach = list)
        print("LANGUAGES :\n", l)
    #-----------------------------------------------------


if __name__ == '__main__':
    LanguageMakerMethodsTest.test_LanguageMaker_GetLanguagesByContentStandard()