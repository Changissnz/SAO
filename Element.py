# todo : add a descriptor->level mapping
# there should be an integer that corresponds to descriptor when called

class Element:

    def __init__(self, idn, language):
        self.idn = idn
        self.language = language
        self.set_language_stats()

    '''
    description:
    - calculates the size of centroid over its descriptor
    '''
    def centroid_to_descriptor_ratio(self):
        return -1

    '''
    description:
    - sets the word count for language
    '''
    def set_language_stats(self):
        if type(self.language.language[1]) is list:
            self.wordCount = len(list(self.language.language[0]) + self.language.language[1])
        else:
            self.wordCount = len(self.language.language[0] | self.language.language[1])

    def get_alignments():
        return -1


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

    ################## START : language
