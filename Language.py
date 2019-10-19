###
"""
a measure of influence that does not use direct intersection:
"functionality" : definitional capacity.
    - FUNC(definitions(Element.bagOfWords), (otherElement.bagOfWords)) => 0 <= float <= 1
    - will use similarity scores
    - FUNC should not be commutative
"""
###
from sklearn.feature_extraction.text import TfidfVectorizer
from random import choice
from nltk import word_tokenize
from LanguageMaker import *

class Language:

    def __init__(self, idn, language):
        self.idn = idn
        self.language = language
        self.prohibited = [] # prohibited words

    '''
    description:
    - compares 2 languages

    arguments:
    - mode := tf-idf | cosine
    '''
    def compare_language_contents(self, otherLang, mode = "tf-idf"):
        sl1, sl2 = ' '.join(self.language[1]), ' '.join(otherLang.language[1])
        if mode == "tf-idf":
            return Language.get_tfidf_measure(sl1,sl2)
        elif mode == "cosine":
            return Language.get_cosine_similarity_measure(sl1,sl2)
        else:
            raise ValueError("!!!")

    '''
    description:
    -

    arguments:
    - args : str

    return:
    -
    '''
    @staticmethod
    def get_tfidf_measure(l1, l2):
        VectorShell = TfidfVectorizer()
        return VectorShell.fit_transform([l1,l2])


    '''
    description:
    - program to measure similarity between
      two containers of words using cosine similarity.

     arguments:
     - wt1 := container(str)
     - wt2 := container(str)

     return:
     - 0 <= float <= 1
    '''
    @staticmethod
    def get_cosine_similarity_measure_(wt1,wt2):

        # sw contains the list of stopwords
        sw = stopwords.words('english')
        l1 =[];l2 =[]

        # remove stop words from string
        xs = {w for w in wt1 if not w in sw}
        ys= {w for w in wt2 if not w in sw}

        # form a set containing keywords of both strings
        rv = xs.union(ys)
        for w in rv:
            if w in xs: l1.append(1) # create a vector
            else: l1.append(0)
            if w in ys: l2.append(1)
            else: l2.append(0)
        c = 0

        # cosine formula
        for i in range(len(rv)):
                c+= l1[i]*l2[i]
        try:
            csn = c / float((sum(l1)*sum(l2))**0.5)
            return csn
        except:
            return 0 # 0-division

    def get_influence_score_over_targets(self):
        return -1

    '''
    description:
    - pops subset of bagOfWords to prohibited
    '''
    def prohibit_speech(self, subsetBagOfWords):
        return -1

    '''
    description:
    - outputs a random string, consists of words from bagOfWords separated by whitespace
    '''
    def output_random_string(self):
        return -1

    # TODO
    '''
    factors :=
    '''
    def output_string_based_on_effect(self, factors):
        return -1

    """
    description:
    - romannnnnnnnnnnnnnnntic

    arguments:
    - words := list(str)

    return:
    - generator(str)
    """
    @staticmethod
    def words_to_romantic(words):
        romantic = ["ia", "io", "o", "a", "ni", "li", "sa", "la", "si", "zzi"]
        for w in words:
            yield w + choice(romantic)

    '''
    description:
    -

    arguments:
    - lang1 := (set(str::centroids), container(str::relatedTerms))
    - lang2 := (set(str::centroids), container(str::relatedTerms))
    - direction := (2,1)|(1,2)|None
    - requiredWordsToMerge := int::(specifies number) | set::(specifies specific words)
    - returnType := "lang"|"lang+additions"

    return:
    - (set(str::centroids), container(str::relatedTerms)), (set(str::centroids), container(str::relatedTerms))
    OR
    - (set(str::centroids), container(str::relatedTerms)), (set(str::centroids), container(str::relatedTerms)),
        (set(str::centroids), container(str::relatedTerms))
    '''
    @staticmethod
    def mate_languages(lang1, lang2, direction, requiredWordsToMerge, returnType = "lang"):
        # check if words actually are in source
        assert direction in {(1,2),(2,1),None}, "direction {} is not valid".format(direction)
        assert returnType in {"lang", "lang+additions"}, "return type {} is invalid".format(returnType)
        assert type(lang1[1]) == type(lang2[1]), "languages in different worlds cannot operate on each other"

        newLang1, newLang2 = lang1[0], lang2[0]
        q = None
        if type(requiredWordsToMerge) is list:
            if direction == None: q = lang1[0] | lang2[0]
            elif direction[0] == 1: q = lang1[0]
            else: q =lang2[0]
            for x in requiredWordsToMerge:
                if x not in q:
                    raise ValueError("({}) is not a centroid value".format(x))

        # get descriptors for words
        descriptors = LanguageMaker.get_descriptors(requiredWordsToMerge, type(lang1[1]))

        # add words from source to dest
        x, x2 = lang1[1], lang2[1]
        if direction == None:
            newLang1, newLang2 = lang1[0] | requiredWordsToMerge, lang2[0] | requiredWordsToMerge
            if type(lang1[1]) is list:
                x, x2 = lang1[1] + descriptors, lang2[1] + descriptors
            elif type(lang2[1]) is set:
                x, x2 = lang1[1] | descriptors, lang2[1] | descriptors
            else:
                raise ValueError("type {} not yet supported.".format(type(lang2[1])))
        elif direction == (1,2):
            newLang2 = lang2[0] | requiredWordsToMerge
            if type(lang2[1]) is list:
                x2 = lang2[1] + descriptors
            elif type(lang2[1]) is set:
                x2 = lang2[1] | descriptors
            else:
                raise ValueError("type {} not yet supported.".format(type(lang2[1])))
        else:
            newLang1 = lang1[0] | requiredWordsToMerge
            if type(lang1[1]) is list:
                x = lang1[1] + descriptors
            elif type(lang1[1]) is set:
                x = lang1[1] | descriptors
            else:
                raise ValueError("type {} not yet supported.".format(type(lang1[1])))

        if returnType == "lang": return (newLang1, x), (newLang2, x2)
        return (newLang1, x), (newLang2, x2), (requiredWordsToMerge, descriptors)

def Language_Sample():
    languages = LanguageMaker.get_languages(2, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
    L = Language(5, languages[0])
    return L

def Language_GetTfidfMeasure():
    languages = LanguageMaker.get_languages(2, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
    l1, l2 = ' '.join(languages[0][1]), ' '.join(languages[1][1])
    tm = Language.get_tfidf_measure(l1,l2)
    return tm

def Language_GetCosineSimilarityMeasure():
    languages = LanguageMaker.get_languages(2, minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
    l1, l2 = languages[0], languages[1] # centers, and sprawl
    lx1, lx2 = ' '.join(l1[1]), ' '.join(l2[1])

    tm = Language.get_cosine_similarity_measure_(l1[1],lx2[1])
    return tm

def LanguageMaker_GetCosineSimilarityMeasure_():
    x3 = LanguageMaker_GetLanguagesByContentSamples()
    l1, l2 = x3[0], x3[1]
    lx1, lx2 = ' '.join(l1[1]), ' '.join(l2[1])
    print("* l1:\n")
    print(l1)
    print("\n*l2:\n")
    print(l2)

    tm = Language.get_cosine_similarity_measure_(l1[1],lx2[1])
    print("cosine similarity :\t{}".format(tm))
    return

def Language_MateLanguages():
    x3 = LanguageMaker_GetLanguagesByContentSamples()
    l1, l2 = x3[0], x3[1] # get languages for (dog,whale), and (cat,rhino)
    # mate "rhino" : l2->l1
    ml = Language.mate_languages(l1, l2, (2,1), {"rhino"}, returnType = "lang+additions")
    
    # get cosine intersection
    cm = Language.get_cosine_similarity_measure_(ml[0][1], ml[1][1])
    print("cosine intersection between [0],[1] : {}".format(cm))

#tm = Language_GetTfidfMeasure()
#tm2 = Language_GetCosineSimilarityMeasure()
#tm3 = LanguageMaker_GetCosineSimilarityMeasure_()
tm4 = Language_MateLanguages()
