# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import state
import sprite_handler
import objects

def power_up_extra_life() -> None:
    if state.player_lives < constants.MAX_LIVES:
        state.player_lives += 1
    sprite_handler.set_sprite_status(objects.POWER_UP_SPRITE, False)

def power_up_god_mode() -> None:
    state.god_mode_frames += 120
    sprite_handler.set_sprite_status(objects.POWER_UP_SPRITE, False)

def power_up_double_score() -> None:
    state.double_score_frames += 240
    sprite_handler.set_sprite_status(objects.POWER_UP_SPRITE, False)

# All defined power ups
table = [("graphics/level/heart.png", power_up_extra_life),
         ("graphics/powerups/god_mode.png", power_up_god_mode),
         ("graphics/powerups/double_score.png", power_up_double_score)]