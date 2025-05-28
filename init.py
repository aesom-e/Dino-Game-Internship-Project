# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import random
import time
import pygame
import constants

# This file exists to make the code in main look nicer.
# When we import a file, the preprocessor (or whatever the eqivilent in Python is)
# copies the contents of the import. In an interpreted language, this means that the
# contents of a file are executed.
# Because of how I've structured this, the code "import init" initializes everything other imports may need

random.seed(time.time())
pygame.init()
pygame.display.set_caption(constants.WINDOW_TITLE)

# This also needs to be here in the initialization.
# We put this into assets so that they may be accessed as assets.<item> not init.<item>
# Importing assets before the pygame display mode has been set raises pygame.error
# so we have to do it like this. I hate python
_screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
_clock  = pygame.time.Clock()
import assets
assets.screen = _screen
assets.clock = _clock