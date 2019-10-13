###
"""
pipeline:
    action(element, other) -> effect(other) -> reaction(other)
"""
###
"""
uses the data structure, bag-of-words, to represent
"""
###
"""
a measure of influence that does not use direct intersection:
"functionality" : definitional capacity.
    - FUNC(definitions(Element.bagOfWords), (otherElement.bagOfWords)) => 0 <= float <= 1
    - will use similarity scores
    - FUNC should not be commutative
"""
###


class Element:
    
    '''
    
    idn := int, identifier
    language := set, bag-of-words
    '''
    def __init__(self, idn, language):
        self.idn = idn
        self.language = language
        self.locations = [] # list of coordinates
        
    # TODO
    def set_locations(self, locations = None):
        if locations == None: return # random
        return -1

class Language:
    
    def __init__(self, idn, bagOfWords):
        self.idn = idn
        self.bagOfWords = bagOfWords
        self.prohibited = set() # prohibited words
    
    '''
    description:
    - gets the influence of this language over some other
    '''
    def get_influence_over(self, otherLanguage):
        return -1
    
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
    def output_string_based_on_effect(self, factors):
        return -1

'''
description:
- each class instance is associated with some Element.
- Element will use this variable when it receives some message from some element/s
- Reaction will modify Element's language according to Effect

- Possible Reactions:
-   1. get new language/speech from other
-   2. obey
-   3. retaliate
'''
class Reaction:
    
    def __init__(self, idn, reactionDictionary):
        self.idn = idn
        self.set_reactions(reactionDictionary)
        
    '''
    description:
    ~
    '''
    def set_reactions(self, reactionDictionary):
        return -1

'''
description:
- each class instance is associated with some Element.
- Effect modifies based on effect from some message.

- Effects:
-   1. speech is prohibited
-   2. language is merged with other

'''
class Effect:
    
    def __init__(self, idn):
        return -1
        
'''
description:
- each class instance is associated with some World
- this class will be used to send messages to other elements

- messages will be of the following classifications:
-   align
-   shame

- "align" and "shame" are based on other Element's language and languageAssociativities (dict., key is language id, each value b/t -1 and 1)
- "align" : >= 0, and if 1, merge all with other Element's speech
- "shame" : < 0, and if -1, prohibit all other Element's speech

- "directness" is a measure that influences the contents of exact message to be sent
- a content is simply a word/phrase that can be assigned a score that is with respect to respondee

- the degree of directness is based on some threshold function f
- f : otherElement.threat_payoff_measure
-
'''
class Actions:
    
    def __init__(self, idn):
        self.idn = idn
        
"""
description:
- each class instance is associated with some World.
- class is to modify the Language of any Element in World from factors other than Element's Action's.
- factors to take into account
-   current size of language
-   language functionality compared to others

- introducing new words based on current contents of bag-of-words.
    - implies if language == SILENCE, Evolution produces null results.
- removing old elements is based on:
    -  rate of usage : use it or lose it
"""
class Evolution:
    def __init__(self):
        return
    
    '''
    description:
    - adds new words to language

    arguments:
    - element := Element, to add new words to language
    - growthFunc := function, takes as arguments (elementSize, languageFunctionality)
    '''
    def introduce_new_words(self, element, growthFunc):
        return
    

#-----------------------------------#-----------------------------------#-----------------------------------#-----------------------------------#-----------------------------------
'''
description:
- assigns initial languages to Elements

arguments:
- mode := disjoint|random
'''
def set_initial_languages(Elements, mode = "disjoint"):
    return -1
    
import random
def words_to_romantic(words):
    romantic = ["ia", "io", "o", "a", "ni", "li", "sa", "la", "si", "zzi"]
    for w in words:
        yield w + random.choice(romantic)
        

"""
this is the data structure that will contain all info for display window

display window is a m x n grid. each coordinate will be marked by a color.

interface should also have feature that allows user to get exact color value pressing a coordinate
"""
class World:
    
    def __init__(self, idn):
        self.idn = idn
        self.gridColors = None # TODO
        
    def run_one_round():
        return -1
        
'''
this will log all pertinent Element history to folder

of greater concern is the following:
-   each Element has a History, but how sad is this that not all Histories have Elements?
'''
class EventHistory:
    
    def __init__(self, idn, folder):
        self.idn = idn