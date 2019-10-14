
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from random import shuffle, choice, choices
from string import punctuation

## problem : encoding a bag-of-words
"""
popular approach is to use frequency measures (tf-idf for example)
but since these are just bag-of-words, then have to find a way to `extract their meaning` first.

`Tree-Algorithm`
Take the following approach:
- for each word w, get d = definition(w).
- descriptorForWord = {d.split()}
- for each relevant word r in definition, get that definition d1.
- loop above steps until minimum number of descriptors is obtained for each Language
"""
#



'''
could add a `fetchByTopics` variable
'''
class LanguageMaker:

    def __init__(self, topics = None):
        self.topics = topics

    '''
    description:
    - fetches nonstop words from NLTK corpus of size n

    arguments:
    - n := int
    - byTopic := bool

    return:
    - set(str)
    '''
    def fetch_nonstop_words(self, n, byTopic = False):

        if byTopic: raise NotImplementedError("fetching words by topic has not yet been implemented")

        """
        description:
        - performs random shuffling of words and returns x of them

        arguments:
        - x := int

        return:
        - set(str)
        """
        def fetch_words(x):
            q = words.words()
            shuffle(q)
            return set(q[:n])

        """
        description:
        - filters words that have empty synsets

        arguments:
        - words, set(str)

        return:
        - set(str)
        """
        def filter_irrelevant(words):
            newWords = set()
            for w in words:
                q = wn.synsets(w)
                if len(q) != 0: newWords |= {w}
            return newWords

        r = filter_irrelevant(LanguageMaker.filter_nonstop_words(fetch_words(n)))
        while True:
            diff = n - len(r)
            if diff == 0: break
            r_ = filter_irrelevant(LanguageMaker.filter_nonstop_words(fetch_words(diff * 300)))
            diff2 = len(r_) - diff
            if diff2 > 0:
                r_ = set(list(r_)[:diff])
            r |= r_
        return r

    @staticmethod
    def filter_nonstop_words(allWords):
        return {w for w in allWords if w not in stopwords.words("english")}

    '''
    description:
    - runs scikit-learn's k-means algorithm on the encodings of bagOfWords' definitions.
    '''
    def cluster_words_by_definition(self, bagOfWords, numClusters):
        return -1

    '''
    description:
    - gets the descriptors for the words.

    arguments:
    - word := str
    - minDescriptors := int
    '''
    def get_descriptors_for_word(self, word):
        try:
            q = wn.synsets(word)[0]
        except:
            return False
        lq = q.definition()
        exclude = set(punctuation) - {" "}
        lq = ''.join(ch for ch in lq if ch not in exclude)
        lq = lq.split(" ")
        defQ =  LanguageMaker.filter_nonstop_words(lq)
        return defQ


    """
    description:
    - gets the descriptors for the words in the `Tree-Algorithm` described above

    arguments:
    - bagOfWords := set(str)
    - minDescriptors := int
    - mode := geq | const, geq outputs a descriptor set of minimum size `minDescriptors`
                       const outputs a descriptor set of constant size `minDescriptors`

    return:
    - set(str)
    """
    def get_descriptors_for_bag(self, bagOfWords, minDescriptors, mode = "geq"):
        assert mode in {"geq", "const"}, "invalid mode {}".format(mode)

        """
        description:
        - chooses appropriate number of random descriptors from set

        arguments:
        - ds := set(str), descriptor set
        - cd := set(str), collected descriptors
        - numWords := int

        return:
        - set(str), random words
        - set(str), collected descriptors
        """
        def choose_random_words(ds, cd, numWords:int = 10):
            x = set()
            termination = 100
            setTerm = False
            while len(x) < numWords:
                rw = set(choices(list(ds), k = numWords))
                rw -= cd
                if len(rw) == 0: break
                x |= rw
                cd |= rw
            return x, cd

        """
        description:
        ~

        arguments:
        - ds := set(str), descriptor set
        - maxL := int

        return:
        - set(str)
        """
        def get_descriptors_for_bag_of_words_(ds, maxL = None):
            # get initial descriptors for bagOfWords
            additionalDescriptors = set()
            n = 0
            for b in ds:
                d = self.get_descriptors_for_word(b)
                if d is False: break
                additionalDescriptors |= d
                n += len(d)
                if maxL != None:
                    if n >= maxL:
                        break
            if maxL != None:
                return set(list(additionalDescriptors)[:maxL])
            return additionalDescriptors

        numUniqueDescriptors = 0
        descriptorSet = set() # dict. : word -> descriptor
        collectedDescriptors = set() # already ran
        descriptorSet = get_descriptors_for_bag_of_words_(bagOfWords, minDescriptors if mode == "const" else None)

        # for required remaining descriptors, run above
        while True:
            x = len(descriptorSet) - minDescriptors
            if x >= 0: break
            q, collectedDescriptors = choose_random_words(descriptorSet, collectedDescriptors, 5)
            desc = get_descriptors_for_bag_of_words_(q, -x)
            descriptorSet |= desc
        return descriptorSet

'''
description:
- checks the size of descriptors of bag for minimum size requirement
'''
def LanguageMaker_GetDescriptorsForBagTest():
    x = LanguageMaker()

    bow = x.fetch_nonstop_words(100)
    desc = x.get_descriptors_for_bag(bow, 100)
    assert len(desc) >= 100, "desc is len {}, want at least 100".format(len(desc))
    
    bow = x.fetch_nonstop_words(100)
    desc = x.get_descriptors_for_bag(bow, 100, "const")
    assert len(desc) == 100, "desc is len {}, want exactly 100".format(len(desc))


LanguageMaker_GetDescriptorsForBagTest()
