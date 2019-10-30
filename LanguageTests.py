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
