# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import random
import constants
import state
import handlers
import state_handler
import input_handler
import text_handler
import sprite_handler

# Object functions. No docstrings for these
def _resume_game() -> None:
    state_handler.current_state = state_handler.PLAYING

def _egg_collision() -> None:
    # First, move the egg back
    sprite_handler.set_sprite_position(EGG_SPRITE, (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE),
                                                    constants.GROUND_Y - constants.EGG_SIZE))
    
    if state.player_lives > 1:
        state.player_lives -= 1
        return
    handlers.handle_death() 

RESUME_GAME_BUTTON = input_handler.register_button((constants.WINDOW_WIDTH/2,
                                                   130,
                                                   220,
                                                   constants.MENU_FONT_SIZE,
                                                   "centered"),
                                                  (0, 0, 0),
                                                  None,
                                                  constants.MENU_FONT_SIZE,
                                                  "Resume Game",
                                                  _resume_game)

PAUSED_GAME_MENU_TEXT = text_handler.register_text((constants.WINDOW_WIDTH/2, 50),
                                                   (0, 0, 0),
                                                   constants.MENU_TITLE_FONT_SIZE,
                                                   "Game Paused")

SCORE_TEXT = text_handler.register_text((constants.WINDOW_WIDTH/2, 50),
                                        (0, 0, 0),
                                        constants.DEFAULT_FONT_SIZE,
                                        "0")

GAME_OVER_TEXT = text_handler.register_text((200, constants.WINDOW_HEIGHT/2-25),
                                            (255, 255, 255),
                                            constants.DEFAULT_FONT_SIZE,
                                            "Game Over!")

GAME_OVER_SCORE_TEXT = text_handler.register_text((200, constants.WINDOW_HEIGHT/2+25),
                                                  (255, 255, 255),
                                                  constants.SMALL_FONT_SIZE,
                                                  "Your Score: 0")

LEADERBOARD_TEXT = text_handler.register_text((600, 50),
                                              constants.LEADERBOARD_TEXT_COLOUR,
                                              constants.SMALL_FONT_SIZE,
                                              "High Scores")

POWER_UP_SPRITE = sprite_handler.register_sprite((0, 0, constants.POWER_UP_SIZE, constants.POWER_UP_SIZE),
                                                 "graphics/powerups/god_mode.png",
                                                 True,
                                                 None)

EGG_SPRITE = sprite_handler.register_sprite((0, constants.GROUND_Y, constants.EGG_SIZE, constants.EGG_SIZE),
                                            ["graphics/egg/egg_1.png", "graphics/egg/egg_2.png"],
                                             True,
                                             _egg_collision)


def register_objects_states() -> None:
    """Registers the objects with the state handler. Needs to be in a function or python complains"""
    state_handler.register_object_state(RESUME_GAME_BUTTON, "button", state_handler.PAUSED)
    state_handler.register_object_state(PAUSED_GAME_MENU_TEXT, "text", state_handler.PAUSED)
    state_handler.register_object_state(SCORE_TEXT, "text", state_handler.PLAYING)
    state_handler.register_object_state(EGG_SPRITE, "sprite", [state_handler.PLAYING, state_handler.PAUSED])
    state_handler.register_object_state(GAME_OVER_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(GAME_OVER_SCORE_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(LEADERBOARD_TEXT, "text", state_handler.DEAD)