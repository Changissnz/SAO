from Language import *
import unittest

def Language_Sample():
    languages = LanguageMaker.get_languages(2, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
    L = Language(5, languages[0])
    return L

class LanguageMethodsTest(unittest.TestCase):

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
        x3 = LanguageMaker_GetLanguagesByContentSamples()
        l1, l2 = x3[0], x3[1] # get languages for (dog,whale), and (cat,rhino)
        # mate "rhino" : l2->l1
        ml = Language.mate_languages(l1, l2, (2,1), {"rhino"}, returnType = "lang+additions")

        # get cosine intersection
        cm = Language.get_cosine_similarity_measure_(ml[0][1], ml[1][1])
        self.assertTrue(cm >= 0.15)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
