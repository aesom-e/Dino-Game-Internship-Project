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