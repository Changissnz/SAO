import pygame, sys
from pygame.locals import *
from ShameAndObedienceGameBoard import *
from time import sleep

def so_true():
    return True

class DisplayGameboard:

    WHITE = (255,255,255)
    BLACK = (0, 0, 0)
    GREEN = (0, 230, 0)

    """
    arguments:
    - gameboard := Gameboard, to be run
    """
    def __init__(self, gameboard, calibrateSize, imagePath = "defaultPitcherOfEmotions.png"):
        self.gameboard = gameboard
        self.calibrateSize = calibrateSize
        self.imagePath = imagePath
        return

    ###########################################################################

    def init_screen(self):
        pygame.init()
        self.displaySurf = pygame.display.set_mode(self.gameboard.pixelRes)
        pygame.display.set_caption('Hello Learned One')

        """
        print("awaiting computational results")
        print("*****\t", self.gameboard.assignElementsToRegion)
        self.gameboard.assign_elements(self.gameboard.assignElementsToRegion)
        """ 
        
        self.update_display_gameboard()
        self.update_display_scoreboard() 
        
        """
        img = pygame.image.load(self.imagePath)
        self.displaySurf.blit(img, (0,0))
        pygame.image.save(img, self.imagePath)

        # draw scoreboard here
        self.update_display_scoreboard(criteria = "id")
        """ 

    def run_loop(self, function = so_true):
        ## this is the loop
        # TODO : instead of True, input termination function
        #        input user keys in this loop
        # CAUTION 
        
        self.init_screen() 
        while function(): # run while-loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
            self.move_and_update()

    """
    description:
    - moves one, and updates display
    """
    def move_and_update(self, terminationCondition = "mute"):
        assert terminationCondition in {"mute"}, "terminationCondition {} not implemented".format(terminationCondition)

        if terminationCondition == "mute":
            q = self.gameboard.termination_condition_mute
        self.gameboard.move_one(calibrateSize = self.calibrateSize)
        self.update_display_scoreboard()
        self.update_display_gameboard()
        print("move round {}".format(self.gameboard.roundNumber)) 
        self.gameboard.roundNumber += 1 

    """
    description:
    ~
    """
    def update_display_gameboard(self):
        self.blank_gameboard()
        self.write_image()

    """
    description:
    - updates display scoreboard with current score.

    arguments:
    - criteria := id|score
    """
    def update_display_scoreboard(self, criteria = "id"):
        assert criteria in {"id", "score"}, "criteria {} not implemented".format(criteria)
        assert criteria == "id", "criteria {} not implemented".format(criteria) ## delete this when done

        def get_y_coord(index):
            return (index * 100) + 50

        def get_x_coord():
            q = ceil((self.gameboard.pixelRes[0] - self.gameboard.imageRes[0]) / 2)
            return q + self.gameboard.imageRes[0]

        if criteria == "id":
            keys = sorted(list(self.gameboard.elements.keys()))
        else:
            t = sorted(self.gameboard.elements.items(), key=lambda kv: kv[1])
            keys = [t_[0] for t_ in t]

        fontObj = pygame.font.Font("freesansbold.ttf", 12)
        x = get_x_coord()
        # blank scoreboard
        self.blank_scoreboard()
        sleep(0.4)
        
        for i, k in enumerate(keys):
            y = get_y_coord(i)
            s = "element {} : active size {}".format(k, self.gameboard.elements[k].activeWordCount)
            textSurfaceObj = fontObj.render(s, True, DisplayGameboard.GREEN, DisplayGameboard.BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (x, y)
            self.displaySurf.blit(textSurfaceObj, textRectObj)
        return True


    ###########################################################################
    '''
    description:
    - blanks scoreboard black.
    '''
    def blank_scoreboard(self):
        minX = self.gameboard.imageRes[0]
        self.displaySurf.fill(DisplayGameboard.BLACK,rect = (minX, 0, self.gameboard.imageRes[0], self.gameboard.imageRes[1]))

    '''
    description:
    - blanks gameboard image white

    arguments:
    -

    return:
    -
    '''
    def blank_gameboard(self):
        x, y = self.gameboard.imageRes
        img = Image.open(self.imagePath)
        data = img.getdata()

        for i in range(x):
            for j in range(y):
                try:
                    data[i,j] = DisplayGameboard.WHITE
                except: continue
        img.save(self.imagePath)

    """
    description:
    - writes image to display.
    """
    def write_image(self):
        # blank
        img = pygame.image.load(self.imagePath)
        self.displaySurf.blit(img, (0,0))
        pygame.image.save(img, self.imagePath)

