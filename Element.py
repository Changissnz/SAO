from Language import *
from GameBoardHandler import *

class Element:

    def __init__(self, idn, language):
        self.idn = idn
        self.language = language #Language(idn, languageContents)
        self.setInitial = False
        self.set_language_stats()
        self.prohibitedSpeech = set()

    '''
    description:
    - calculates the size of centroid over its descriptor
    '''
    def centroid_to_descriptor_ratio(self):
        return len(self.language.language[0]) / len(self.language.language[1])

    '''
    description:
    - sets the word count for language
    '''
    def set_language_stats(self):
        assert self.setInitial != True, "cannot set language stats after initial"
        ##print("HERE0:\n{}\n".format(self.language.language))
        ##print("HERE:\n{}\n".format(self.language.language[1]))
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
        return self.get_language_stats_on_centroid_with_prohibition() +\
            self.get_language_stats_on_descriptor_with_prohibition()

    def get_language_stats_on_centroid_with_prohibition(self):
        funk = lambda x : False if x in self.prohibitedSpeech else True
        return len(list(filter(funk, self.language.language[0])))

    def get_language_stats_on_descriptor_with_prohibition(self):
        funk = lambda x : False if x in self.prohibitedSpeech else True
        return len(list(filter(funk, self.language.language[1])))

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
        self.language.remove_from_language_descriptors(newSubtractions)

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
        ##print("TO ADD:\t", toAdd)
        self.language.language[0].update(toAdd)
        ##print("HERE :\t", self.language.language[0])
        self.language.language[0].difference_update(toRemove)
        ##print("HERE2")

    ################## END : language modification methods
