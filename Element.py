from Language import *
from GameBoardHandler import *
from math import ceil

class Element:

    def __init__(self, idn, language):
        self.idn = idn
        self.language = language
        self.setInitial = False
        self.set_language_stats()
        self.prohibitedSpeech = set()
        self.reproduceCounter = 1
        self.mute = False

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
        self.centroidCount = len(self.language.get_centroids())
        self.activeCentroidCount = len(self.language.get_centroids())
        self.descriptorCount = len(self.language.get_descriptors())
        self.activeDescriptorCount = len(self.language.get_descriptors())
        assert self.centroidCount != 0 and self.descriptorCount != 0, "invalid initial language : cannot be empty"
        self.wordCount = self.centroidCount + self.descriptorCount
        self.activeWordCount = self.centroidCount + self.descriptorCount
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

    '''
    description:
    -
    '''
    def get_language_stats_on_centroid_with_prohibition(self):
        return len(self.get_active_centroids())

    ## TODO : add arguments for call to mute
    '''
    description:
    - updates language statistic variables
    '''
    def update_language_stats(self):
        self.activeCentroidCount = self.get_language_stats_on_centroid_with_prohibition()
        self.activeDescriptorCount = self.get_language_stats_on_descriptor_with_prohibition()
        self.activeWordCount = self.activeCentroidCount + self.activeDescriptorCount
        self.centroidCount = len(self.language.get_centroids())
        self.descriptorCount = len(self.language.get_descriptors())
        self.wordCount =self.centroidCount + self.descriptorCount
        self.mute = self.is_mute()

    """
    description:
    ~

    return:
    - set(`active centroids`)
    """
    def get_active_centroids(self):
        funk = lambda x : False if x in self.prohibitedSpeech else True
        return set(filter(funk, self.language.get_centroids()))

    """
    description:
    ~

    return:
    - set|list, `active centroids`
    """
    def get_active_descriptors(self):
        funk = lambda x : False if x in self.prohibitedSpeech else True
        if type(self.language.get_descriptors()) is list:
            return list(filter(funk, self.language.get_descriptors()))
        else:
            return set(filter(funk, self.language.get_descriptors()))

    '''
    description:
    ~

    return:
    - int, count of active descriptor
    '''
    def get_language_stats_on_descriptor_with_prohibition(self):
        q = self.get_active_descriptors()
        return len(q)

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
        self.language.language[0].update(toAdd)
        self.language.language[0].difference_update(toRemove)

    ################## END : language modification methods

    # TODO : test below methods
    """
    description:
    -

    arguments:
    - reproduceFrequency := int, interval between reproduction
    - reproduceDegree := float, 0 <= x <= 1

    return:
    - int::(>= 0 change in size)
    """
    def do_self_actions_standard(self, reproduceFrequency, reproduceDegree):
        # reproduce if on time
        if reproduceFrequency == 0: return
        c = 0
        if self.reproduceCounter % reproduceFrequency == 0:
            c += self.self_reproduce(reproduceDegree)
            self.reproduceCounter = 1
        else:
            self.reproduceCounter += 1

        # generate 1 round
        c += self.self_generate()
        return c


    """
    description:
    - adds x new centroids to language.centroid based on `reproduceDegree`, and
      their corresponding descriptors to language.descriptors.

    arguments:
    - reproduceDegree := 0 <= float <= 1

    return:
    - int::(>= 0 change in size)
    """
    def self_reproduce(self, reproduceDegree):
        self.update_language_stats()
        q = ceil(self.activeCentroidCount * reproduceDegree)
        x = LanguageMaker.fetch_nonstop_words(q)
        self.update_language_centroids(x, set())

        d = LanguageMaker.get_descriptors(x, type(self.language.get_descriptors()))
        self.update_language_descriptors(d, set())
        return len(x) + len(d)

    """
    description:
    - updates descriptors for centroid

    arguments:
    - typeGeneration := recursive|static, the type of content to use for generation
    - numGenerations := int, number of times to add descriptors for centroids to descriptors

    return:
    - int::(>=0 difference in size)
    """
    def self_generate(self, typeGeneration = "recursive", numGenerations = 0):
        assert typeGeneration in {"recursive", "static"}, "typeGeneration {}".format(typeGeneration)
        self.update_language_stats()

        x = LanguageMaker.get_descriptors(self.language.get_centroids(),\
            output = type(self.language.get_descriptors()))

        c = 0
        self.update_language_descriptors(x, set())
        c += len(x)

        while numGenerations > 0:
            if typeGeneration == "recursive":
                self.update_language_centroids(x)
                x = LanguageMaker.get_descriptors(x,\
                    output = type(self.language.get_descriptors()))

            self.update_language_descriptors(x, set())
            c += len(x)
            numGenerations -= 1
        return c

    """
    description:
    ~

    arguments:
    - criteria := centroid|descriptor
    - minThreshold := 0 <= x <= 1, minimum threshold for non-mute

    return:
    - bool, mute
    """
    def is_mute(self, criteria = {"centroid", "descriptor"}, minThreshold = 0):
        assert minThreshold >= 0 and minThreshold <= 1, "invalid minThreshold {}".format(minThreshold)

        if "descriptor" in criteria:
            return True if self.activeDescriptorCount/self.descriptorCount <= minThreshold else False
        if "centroid" in criteria:
            return True if self.activeCentroidCount/self.centroidCount <= minThreshold else False
        return True if self.activeWordCount/self.wordCount <= minThreshold else False
