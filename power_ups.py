# Protection for running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import state

def power_up_extra_life() -> None:
    if state.player_lives < constants.MAX_LIVES:
        state.player_lives += 1

def power_up_god_mode() -> None:
    state.god_mode_frames += 120
    pass

def power_up_double_score() -> None:
    state.double_score_frames += 240
    pass

# All defined power ups
table = [(pygame.transform.scale(pygame.image.load("graphics/level/heart.png").convert_alpha(),
            (constants.POWER_UP_SIZE, constants.POWER_UP_SIZE)),
            power_up_extra_life
            ),
        (pygame.transform.scale(pygame.image.load("graphics/powerups/god_mode.png").convert_alpha(),
            (constants.POWER_UP_SIZE, constants.POWER_UP_SIZE)),
            power_up_god_mode
            ),
        (pygame.transform.scale(pygame.image.load("graphics/powerups/double_score.png").convert_alpha(),
            (constants.POWER_UP_SIZE, constants.POWER_UP_SIZE)),
            power_up_double_score
            )
        ]