import pygame, sys
from pygame.locals import *
from ShameAndObedienceGameBoard import *

class DisplayGameboard:

    BLACK = (0, 0, 0)
    GREEN = (0, 230, 0)

    """
    arguments:
    - gameboard := Gameboard, to be run
    """
    def __init__(self, gameboard):
        self.gameboard = gameboard
        self.displaySurf = None
        return

    """
    description:
    -
    """
    def set_up_display(self):
        pygame.init()
        self.displaySurf = pygame.display.set_mode(self.gameboard.pixelRes)
        pygame.display.set_caption('Hello Learned One')
        img = pygame.image.load("defaultPitcherOfEmotions.png")
        self.displaySurf.blit(img, (0,0))

    ## TOD0 : add criteria "ranking"
    """
    description:
    - updates scoreboard for interface
    """
    def update_display_scoreboard(self, criteria = "ordered"):
        assert criteria == "ordered", "criteria {} not implemented".format(criteria)

        def get_y_coord(index):
            return (index * 100) + 50

        def get_x_coord():
            q = ceil((self.gameboard.pixelRes[0] - self.gameboard.imageRes[0]) / 2)
            return q + self.gameboard.imageRes[0]

        if criteria == "ordered":
            keys = sorted(list(self.gameboard.elements.keys()))
        else:
            t = sorted(self.gameboard.elements.items(), key=lambda kv: kv[1])
            keys = [t_[0] for t_ in t]

        fontObj = pygame.font.Font("freesansbold.ttf", 12)
        x = get_x_coord()
        for i, k in enumerate(keys):
            y = get_y_coord(i)
            s = "element {} : active size {}".format(k, self.gameboard.elements[k].activeWordCount)
            textSurfaceObj = fontObj.render(s, True, DisplayGameboard.GREEN, DisplayGameboard.BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (x, y)
            self.displaySurf.blit(textSurfaceObj, textRectObj)
        return

    """
    description:
    - this is the loop to be called to visualize pygame gui

    argument:
    - calibrateSize := False|(int,float)
    - scoreboardCriteria := ordered|descending, ordered is by element id
                                descending is by element's active word count.

    """
    def run_loop(self, calibrateSize = (10 **10, 0.25), scoreboardCriteria = "ordered"):
        self.init_environment()
        self.set_up_display()
        end = False

        while True: #
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()

            # update one round here
            end = self.update_environment(end, scoreboardCriteria, calibrateSize)
            if end: print("DONE")

    def init_environment(self):
        self.gameboard.set_element_action_functions_uniform()
        # TODO : more here

    """
    description:
    -

    arguments:
    - past := boolean
    - scoreboardCriteria := ordered|descending
    """
    def update_environment(self, past = False, scoreboardCriteria = "ordered", calibrateSize = False):
        # run one round
        if past: return past

        self.gameboard.move_one(calibrateSize)
        q = self.update_display_scoreboard(criteria = "ordered")

        if self.gameboard.termination_condition_mute():
            return True
        return False
