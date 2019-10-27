from Language import *
import unittest

def Language_Sample():
    languages = LanguageMaker.get_languages(2, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
    L = Language(5, languages[0])
    return L

class LanguageMethodsTest(unittest.TestCase):

    def test_Language_Random(self):
        x = Language.random()

    def test_Language_GetTfidfMeasure(self):
        try:
            languages = LanguageMaker.get_languages_standard(2, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
            l1, l2 = ' '.join(languages[0][1]), ' '.join(languages[1][1])
            tm = Language.get_tfidf_measure(l1,l2)
        except:
            self.assertRaises("could not complete tfidf measure")

    def test_Language_GetCosineSimilarityMeasure(self):
        languages = LanguageMaker.get_languages_standard(2, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
        l1, l2 = languages[0], languages[1] # centers, and sprawl
        tm = Language.get_cosine_similarity_measure_(l1[1],l2[1])
        self.assertTrue(tm >= 0 and tm <= 1)

    def test_Language_MateLanguages(self):

        x3 = LanguageMaker.get_languages_by_content_standard([{"dog", "whale"}, {"cat", "rhino"}], outputForEach = list)

        l1, l2 = x3[0], x3[1] # get languages for (dog,whale), and (cat,rhino)
        # mate "rhino" : l2->l1
        ml = Language.mate_languages(l1, l2, (2,1), {"rhino"}, returnType = "lang+additions")

        # get cosine intersection
        cm = Language.get_cosine_similarity_measure_(ml[0][1], ml[1][1])
        self.assertTrue(cm >= 0.15)

    @staticmethod
    def demonstrate_Language_RandomByCentroid():

        q = Language.random_by_centroid(centroids = {"knight", "shine", "armor"})
        print("here:\n",q.language)

    def test_Language_SelfReproduce(self):
    ##def self_reproduce(self, numberOfDescriptors):
        return -1

if __name__ == '__main__':
    q = LanguageMethodsTest.demonstrate_Language_RandomByCentroid()
    #unittest.main()
