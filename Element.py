from Language import *

class Element:

    def __init__(self, idn, language):
        self.idn = idn
        self.language = language
        self.setInitial = False
        self.set_language_stats()
        self.prohibitedSpeech = {}

    '''
    description:
    - calculates the size of centroid over its descriptor
    '''
    def centroid_to_descriptor_ratio(self):
        return len(self.language[0]) / len(self.language[1])

    '''
    description:
    - sets the word count for language
    '''
    def set_language_stats(self):
        assert self.setInitial != True, "cannot set language stats after initial"

        self.descriptorCount = len(self.language.language[1])

        if type(self.language.language[1]) is list:
            self.wordCount = len(list(self.language.language[0]) + self.language.language[1])
        else:
            self.wordCount = len(self.language.language[0] | self.language.language[1])
        self.setInitial = True


    # TODO : test this
    """
    description:
    - determines size of language that factors in prohibited words

    return:
    - float
    """
    def get_language_stats_with_prohibition(self):

        funk = lambda x : False if x in self.prohibitedSpeech else True

        centroidSize = len(list(filter(funk, self.language.language[0])))
        descriptorSize = len(list(filter(funk, self.language.language[1])))
        return centroidSize + descriptorSize

    # TODO : future
    def get_language_stats_unique_with_prohibition(self):
        return -1

    '''
    description:
    - pops subset of bagOfWords to prohibited
    '''
    def prohibit_speech(self, subsetBagOfWords):
        self.prohibitedSpeech.update(subsetBagOfWords)

    ################## START : language modification methods
    '''
    description:
    - updates language descriptors

    arguments:
    - newAdditions := set | list, new terms to add
    - newSubtractions := set | list, new terms to add

    return:
    -
    '''
    def update_language_descriptors(self, newAdditions, newSubtractions):
        q = LanguageMaker.get_language_type(self.language.language)
        self.language.add_to_language_descriptors(newAdditions)
        self.language.remove_from_language_descriptors(newAdditions)

    '''
    description:
    - updates language centroids

    arguments:
    - toAdd := set, words (should not be in toRemove)
    - toRemove := set, words (should not be in toAdd)

    return:
    -
    '''
    def update_language_centroids(self, toAdd, toRemove):
        self.language.language[0].update(toAdd)
        self.language.language[0].difference_update(toRemove)

    '''
    description:
    -

    arguments:
    - otherElement :=
    - mateDetails := TODO

    return:
    - updated elements
    '''
    def mate_method1(self, otherElement, mateDetails):
        return -1

    ################## END : language modification methods
