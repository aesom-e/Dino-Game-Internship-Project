import constants
import state_handler
import input_handler
import text_handler

# Button functions. No docstrings for these
def _resume_game() -> None:
    state_handler.current_state = state_handler.PLAYING

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


def register_objects_states() -> None:
    """Registers the objects with the state handler. Needs to be in a function or python complains"""
    state_handler.register_object_state(RESUME_GAME_BUTTON, "button", state_handler.PAUSED)
    state_handler.register_object_state(PAUSED_GAME_MENU_TEXT, "text", state_handler.PAUSED)
    state_handler.register_object_state(SCORE_TEXT, "text", state_handler.PLAYING)
    state_handler.register_object_state(GAME_OVER_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(GAME_OVER_SCORE_TEXT, "text", state_handler.DEAD)