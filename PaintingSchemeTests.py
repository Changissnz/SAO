from PaintingScheme import *
import unittest

class PaintingSchemeMethodsTest(unittest.TestCase):

    @staticmethod
    def demonstrate_PaintImageGivenRegionAndColor():
        pixelRes = (500, 400)
        region = ((0,0), (100,100))
        color = (125,125,125)

        q = make_blanko(pixelRes, saveFile = "defaultPitcherOfEmotions.png")
        paint_image_given_region_and_color(region, color)

if __name__ == '__main__':
    unittest.main()
