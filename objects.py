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
    # Check if the god mode is active
    if state.god_mode_frames: return

    # Move the egg back
    sprite_handler.set_sprite_position(EGG_SPRITE, (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE),
                                                    constants.GROUND_Y - constants.EGG_SIZE))
    
    if state.player_lives > 1:
        state.player_lives -= 1
        return
    handlers.handle_death()

def _play_game() -> None:
    state_handler.current_state = state_handler.PLAYING

RESUME_GAME_BUTTON = input_handler.register_button((constants.WINDOW_WIDTH/2,
                                                   130,
                                                   220,
                                                   constants.MENU_FONT_SIZE,
                                                   "centered"),
                                                  (0, 0, 0),
                                                  (30, 30, 30),
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

PLAY_AGAIN_BUTTON = input_handler.register_button((200, constants.WINDOW_HEIGHT/2+50, 130, constants.SMALL_FONT_SIZE, "centered"),
                                                  (255, 255, 255),
                                                  (237, 210, 31),
                                                  None,
                                                  constants.SMALL_FONT_SIZE,
                                                  "Play Again",
                                                  _resume_game)

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

MAIN_MENU_TITLE = text_handler.register_text((400, 50),
                                             (0, 0, 0),
                                             constants.MENU_TITLE_FONT_SIZE,
                                             constants.WINDOW_TITLE)

MENU_PLAY_BUTTON = input_handler.register_button((400, 300, 60, constants.MENU_FONT_SIZE, "centered"),
                                                 (0, 0, 0),
                                                 (30, 30, 30),
                                                 None,
                                                 constants.MENU_FONT_SIZE,
                                                 "Play",
                                                 _play_game)


def register_objects_states() -> None:
    """Registers the objects with the state handler. Needs to be in a function or python complains"""
    state_handler.register_object_state(RESUME_GAME_BUTTON, "button", state_handler.PAUSED)
    state_handler.register_object_state(PAUSED_GAME_MENU_TEXT, "text", state_handler.PAUSED)
    state_handler.register_object_state(SCORE_TEXT, "text", state_handler.PLAYING)
    state_handler.register_object_state(EGG_SPRITE, "sprite", [state_handler.PLAYING, state_handler.PAUSED])
    state_handler.register_object_state(GAME_OVER_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(GAME_OVER_SCORE_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(PLAY_AGAIN_BUTTON, "button", state_handler.DEAD)
    state_handler.register_object_state(LEADERBOARD_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(MAIN_MENU_TITLE, "text", state_handler.MENU)
    state_handler.register_object_state(MENU_PLAY_BUTTON, "button", state_handler.MENU)