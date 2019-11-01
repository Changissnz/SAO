from sklearn.feature_extraction.text import TfidfVectorizer
from random import choice, choices, sample
from nltk import word_tokenize
from LanguageMaker import *

class Language:

    def __init__(self, idn, language):
        self.idn = idn
        self.language = language
        self.prohibited = [] # prohibited words

    def __len__(self):
        q = LanguageMaker.get_language_type(self.language)
        if q == "standard":
            return len(self.language[0]) + len(self.language[1])
        elif q == "ripple":
            raise NotImplementedError("IMPLEMENT HERE")

    def __str__(self):
        q = LanguageMaker.get_language_type(self.language)
        x = "* language {} : size {}\n".format(self.idn, len(self.language[0])\
            + len(self.language[1]))
        if q == "standard":
            x += "\t**centroids : {}**\n".format(len(self.language[0]))
            for l in self.language[0]:
                x += l + " "
            x += "\n\n"
            x += "\t**description : {}**\n".format(len(self.language[1]))
            for l in self.language[1]:
                x += l + " "
            return x
        elif q == "ripple":
            raise NotImplementedError("IMPLEMENT HERE")

    """
    description:
    - outputs a random language of specified size
    """
    @staticmethod
    def random(idn = "numero-unetas", minSizeInfo = 100, startSizeInfo = 5, mode = "geq"):
        languageContents = LanguageMaker.get_languages_standard(1, minSizeInfo, startSizeInfo, mode)[0]
        return Language(idn, languageContents)

    @staticmethod
    def random_by_centroid(idn = "numero-unetas", centroids = set(), languageOutput = list,\
        minSizeInfo = 100, startSizeInfo = 5, mode = "geq"):
        languageContents = LanguageMaker.get_languages_by_content_standard([centroids], outputForEach = list)[0]
        return Language(idn, languageContents)

    def get_centroids(self):
        return deepcopy(self.language[0])

    def is_centroid(self, d):
        return True if d in self.language[0] else False

    def get_descriptors(self):
        return deepcopy(self.language[1])

    def is_descriptor(self, d):
        return True if d in self.language[1] else False

    def get_content(self, output = list):
        assert output in {list, set}, "invalid output {}".format(output)

        c, d = self.get_centroids(), self.get_descriptors()
        if output == list:
            return list(c) + list(d)
        return c + set(d)

    def add_to_centroid(self, additions):
        q = LanguageMaker.get_language_type(self.language)
        if q == "standard":
            self.language[0].update(additions)
        elif q == "ripple":
            raise NotImplementedError("IMPLEMENT HERE")
        else:
            raise NotImplementedError("IMPLEMENT HERE")

    def remove_from_centroid(self, subtractions):
        return -1

    # TODO : test below 2 methods
    '''
    description:
    - adds to language descriptors
    '''
    def add_to_language_descriptors(self, additions):
        q = LanguageMaker.get_language_type(self.language)
        if q == "standard":
            if type(self.language[1]) is list:
                for a in additions: self.language[1].extend(additions)
            elif type(self.language[1]) is set:
                self.language[1].update(additions)
            else:
                raise ValueError("language type {} is invalid".format(type(self.language[1])))
        elif q == "ripple":
            raise NotImplementedError("IMPLEMENT HERE")
        else:
            raise NotImplementedError("IMPLEMENT HERE")

    def remove_from_language_descriptors(self, subtractions):
        q = LanguageMaker.get_language_type(self.language)
        if q == "standard":
            if type(self.language[1]) is list:
                # removes one copy, not all
                """
                for s in subtractions:
                    try:
                        i = self.language[1].index(s)
                        self.language[1].pop(i)
                    except:
                        print("word {} not found".format(s))
                        pass
                """
                # removes all copies
                funk = lambda x : False if x in subtractions else True
                nl = list(filter(funk, self.language[1]))
                self.language = (self.language[0], nl)
            elif type(self.language[1]) is set:
                self.language[1].difference_update(subtractions)
            else:
                raise ValueError("language type {} is invalid".format(type(self.language[1])))
        elif q == "ripple":
            raise NotImplementedError("IMPLEMENT HERE")
        else:
            raise NotImplementedError("IMPLEMENT HERE")

    '''
    description:
    - compares 2 languages

    arguments:(self.language) i

    arguments:
    - mode := tf-idf | cosine
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
    ~

    arguments:
    - l1,l2 := str

    return:
    ~
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

    '''
    description:
    - outputs a random string, consists of words from bagOfWords separated by whitespace
    '''
    def output_random_string(self):
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
