# Mall_Copper_Turf_Feud

## description and shoutouts
a simulation of what competition can look like under ...cerTain conditions, using things like the BuTTerfly EEffect.

Work inspired by a character called Tremworstensch (no relation), the specifics of which are forgotten due to the cyclic nature of the dawn of new things and the death of older things, not to sound cliche (or what not).

Although cerTain... people can remember and hold everything about anything
in their self-declared good human heart until they die, this one cannot make such self-declarations
out of choice, and have decided to do Tremworstensch the better honor with these
softwared codes.

Shoutout to that character Tremworstensch, that one whose remains were stomped, crushed, and incinerated, but who continues to live on through these softwared codes.

## code docs
---------------------------------------------------------------------------
Ideas for simulations.
Everything can bes.
- Rising Sun The Snake vs. Eddy The Eagle : two vastly different
                                            entities.
- Dead Walkers : Walking Dead Zombie and Rick the slick Copper Dick
                 Shit.
- Wasteland : terrain possesses cerTain... properties at ...cerTain times.
- Replacement : see below
- Right-hand next :  always a future. a better. a worst. a turn. an outcome.
- Shame and Obedience : civilization needs standards. so people make them. or
                        break them.
- Shameless Tactic : Who's to say, tis te One Caesar?
- Ethnic Harpy : think differences and charm. differences to complement.
                difference as the destination.
- Politzai Malakai: think police state.

---------------------------------------------------------------------------
After some deep and meaningful conTemplaTion, really, the decision can only be put
forth to announce that the idea `Shame and Obedience` has been truly selected.

- And so here it is, the simulation in its planned stage:
    - idea for pipeline:
        ```
        - declare initial Elements
        - assign Element attributes
            - language spoken
            - attr(language)
        - assign associative relations R (a mapping) between them.
        - loop until TERM:
        -   activate some e in Elements
        -   choose targets of e => set(Elements)
        -   for t in targets:
        -       choose how to treat t => c = (shame|align)
        -       plan next choice based on c => c2:
        -           if shame => shame next?
        -           if align => align next?
        -       apply c(t)
        -       get reactions => set(ElementReactions)
        -       t.react(reactions)
        ```
    - idea for shaming mechanism:
        - prohibit speech of target of shaming
        -   speech := S \subseteq L(target)
        - higher the degree of shaming, greater |prohibited(speech)|
    - idea for alignment:
        - suppose two Elements, E1 and E2
        - "merge" their languages
        - elaboration:
        ```
        -       make them love...to develop...to learn from one another...
        -       to grow old together doing great things!
        -       to die young together in the name of love!
        -       *start:srs tho:end*
        ```
        - subset of union(E1,E2) is S s.t.
        ```
        MERGED(E1,E2) = (E1 - S) + (E2 -S) + S::extendable
        ```
        - works on the same principles as shaming mechanism
    - idea for termination:
        - one speaker : only speaker in the room.
                        all others got silenced.
        - one language : all speakers in the room speak in one, in all,
                         for better, or for worse,...
    - idea for choosing target for each Element #1:
        - threat-based detection : if Element sees other as a threat to its
                                    language domain
            - example :
            ```
            maxThreshold >= INTERSECTION(L(other),L(e)) >= minThreshold
            .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
            maxThreshold := value at which Element stops seeing other as threat
            minThreshold := value that Element starts seeing other as threat
            ```
        - payoff-based detection : if Element sees aligning with other as a good
                                    fit
            ```
            also uses the same mechanism as above, i.e. the definition of hypocrisy.
            
            aka. An example is always the definition of hypocrisy.
            ```
    - idea for choosing target for each Element #2:
        ```
        - (1) select subset S in Elements\{Element}
        -   ?HOW? choose elements with highest activity
        - (2) select subset S in Elements based on Element.Language.AttributeX
        -       EX. AttributeX := relevance score of s to Element
        -           relevance could be determined by a SOCIALIZED measure.
        -           SOCIALIZED could mean the degree of Element.Language that intersections w/ other Elements.Languages.
        -           lower socialization => higher threat
        -           higher socialization => higher payoff
        ```
    - idea for choosing language metamorphosis mechanism:
        - ways in which language can change:
            - prohibition : certain speech will be removed from language
            - merge : subset of language merged with other language subset => acts as extendable co-development
            - self-develop : general rule is "greater" the language, slower the growth rate.
    - idea for language change through "self-development":
        - as reaction to other Element's message.
            ```
            - counteract
            -   add VARIANT(message) => self.language.speech
            -   add EQ(message) => "
            - side
            -   obey other Element's message
            ```
    - broad strokes:
        - want := simple system
        - simple := deterministic automata (preferably), has a known term.
        
        - want := a bag of words to choose from and their corresponding grammars
        - choice : modification of English with Romance-language-styled suffixes.

---------------------------------------------------------------------------
(trythissdfsdafkcthlcsasdfsasfd => TuMach) == ?deedum? -> new(TuMach)::future