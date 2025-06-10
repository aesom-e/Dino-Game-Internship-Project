# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

from typing import NoReturn
import pygame
import random
import constants
import state
import handlers
import state_handler
import input_handler
import text_handler
import sprite_handler
import sound

# Object functions. No docstrings for the ones that I consider to be self-explanitory
# Do you really want to read """Resumes the game""" below _resume_game?
def _resume_game() -> None:
    state_handler.current_state = state_handler.PLAYING
    sound.music.play()

def _main_menu() -> None:
    # Reset all state
    handlers.reset_state()
    
    state_handler.current_state = state_handler.MENU

def _egg_collision() -> None:
    """Handles everything to do with the player collision with the egg"""
    # Check if the god mode is active
    if state.god_mode_frames: return

    # Play the sound
    sound.play("hit.wav")

    # Move the egg back
    sprite_handler.set_sprite_position(EGG_SPRITE, (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE),
                                                    constants.GROUND_Y - constants.EGG_SIZE))
    
    # Handle the player lives
    if state.player_lives > 1:
        state.player_lives -= 1
        return
    handlers.handle_death()

def _chicken_collision() -> None:
    """Handles everything to do with the player collision with the chickent"""
    # Check if god mode is active
    if state.god_mode_frames: return

    # Play the sound
    sound.play("hit.wav")

    # Move the chicken back
    sprite_handler.set_sprite_position(CHICKEN_SPRITE, (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE),
                                                        constants.GROUND_Y - constants.CHICKEN_SIZE - constants.CHICKEN_HEIGHT))

    # Create a delay before the chicken spawns again
    state.chicken_spawn_delay = random.randint(30, 90)
    sprite_handler.set_sprite_status(CHICKEN_SPRITE, False)

    # Handle the player lives
    if state.player_lives > 1:
        state.player_lives -= 1
        return
    handlers.handle_death()

def _play_game() -> None:
    state_handler.current_state = state_handler.PLAYING
    sound.music.set("music.mp3")

def _how_to() -> None:
    state_handler.current_state = state_handler.HOW_TO

def _quit_game() -> NoReturn:
    pygame.quit()
    exit(0)

RESUME_GAME_BUTTON = input_handler.register_button((constants.WINDOW_WIDTH/2,
                                                   90,
                                                   None,
                                                   constants.MENU_FONT_SIZE,
                                                   "centered"),
                                                  (0, 0, 0),
                                                  (25, 100, 40),
                                                  None,
                                                  constants.MENU_FONT_SIZE,
                                                  "Resume Game",
                                                  _resume_game)

PAUSED_GAME_MENU_TEXT = text_handler.register_text((constants.WINDOW_WIDTH/2, 50),
                                                   (0, 0, 0),
                                                   constants.MENU_TITLE_FONT_SIZE,
                                                   "Game Paused")

PAUSE_MAIN_MENU_BUTTON = input_handler.register_button((constants.WINDOW_WIDTH/2,
                                                       130,
                                                       None,
                                                       constants.MENU_FONT_SIZE,
                                                       "centered"),
                                                       (0, 0, 0),
                                                       (100, 25, 25),
                                                       None,
                                                       constants.MENU_FONT_SIZE,
                                                       "Main Menu",
                                                       _main_menu)

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

PLAY_AGAIN_BUTTON = input_handler.register_button((200,
                                                   constants.WINDOW_HEIGHT/2+50,
                                                   None,
                                                   constants.SMALL_FONT_SIZE,
                                                   "centered"),
                                                  (255, 255, 255),
                                                  (237, 210, 31),
                                                  None,
                                                  constants.SMALL_FONT_SIZE,
                                                  "Play Again",
                                                  _resume_game)

DEATH_MAIN_MENU_BUTTON = input_handler.register_button((200,
                                                        constants.WINDOW_HEIGHT/2+90,
                                                        None,
                                                        constants.SMALL_FONT_SIZE,
                                                        "centered"),
                                                       (255, 255, 255),
                                                       (255, 120, 120),
                                                       None,
                                                       constants.SMALL_FONT_SIZE,
                                                       "Main Menu",
                                                       _main_menu)

LEADERBOARD_TEXT = text_handler.register_text((600, 50),
                                              constants.LEADERBOARD_TEXT_COLOUR,
                                              constants.SMALL_FONT_SIZE,
                                              "High Scores")

POWER_UP_SPRITE = sprite_handler.register_sprite((0, 0, constants.POWER_UP_SIZE, constants.POWER_UP_SIZE),
                                                 "graphics/powerups/god_mode.png",
                                                 True,
                                                 None)

EGG_SPRITE = sprite_handler.register_sprite((0, constants.GROUND_Y, constants.EGG_SIZE, constants.EGG_SIZE),
                                            ["graphics/enemies/tweaking_egg_1.png",
                                             "graphics/enemies/tweaking_egg_2.png",
                                             "graphics/enemies/tweaking_egg_3.png",
                                             "graphics/enemies/tweaking_egg_4.png"],
                                            True,
                                            _egg_collision)

CHICKEN_SPRITE = sprite_handler.register_sprite((0, constants.GROUND_Y-constants.CHICKEN_HEIGHT, constants.CHICKEN_SIZE, constants.CHICKEN_SIZE),
                                                ["graphics/enemies/chicken_1.png", "graphics/enemies/chicken_2.png"],
                                                True,
                                                _chicken_collision)

MAIN_MENU_TITLE = text_handler.register_text((400, constants.MENU_TITLE_FONT_SIZE),
                                             (0, 0, 0),
                                             constants.MENU_TITLE_FONT_SIZE,
                                             constants.WINDOW_TITLE)

MENU_PLAY_BUTTON = input_handler.register_button((400, 260, None, constants.MENU_FONT_SIZE, "centered"),
                                                 (0, 0, 0),
                                                 (180, 120, 20),
                                                 None,
                                                 constants.MENU_FONT_SIZE,
                                                 "Play",
                                                 _play_game)


MENU_QUIT_BUTTON = input_handler.register_button((400, 340, None, constants.MENU_FONT_SIZE, "centered"),
                                                 (0, 0, 0),
                                                 (30, 30, 120),
                                                 None,
                                                 constants.MENU_FONT_SIZE,
                                                 "Quit",
                                                 _quit_game)

MENU_HOW_TO_BUTTON = input_handler.register_button((400, 300, None, constants.MENU_FONT_SIZE, "centered"),
                                                   (0, 0, 0),
                                                   (30, 120, 30),
                                                   None,
                                                   constants.MENU_FONT_SIZE,
                                                   "How To Play",
                                                   _how_to)

HOW_TO_TITLE = text_handler.register_text((400, constants.MENU_TITLE_FONT_SIZE),
                                          (0, 0, 0),
                                          constants.MENU_TITLE_FONT_SIZE,
                                          "How To Play")

HOW_TO_BACK_BUTTON = input_handler.register_button((400, 360, None, constants.MENU_FONT_SIZE, "centered"),
                                                   (0, 0, 0),
                                                   (120, 30, 30),
                                                   None,
                                                   constants.MENU_FONT_SIZE,
                                                   "Back",
                                                   _main_menu)

# This is more time efficient than writing another handler for columns of text
HOW_TO_ENTRIES = [text_handler.register_text((150, 100),
                                             (0, 0, 0),
                                             constants.MENU_MINOR_TITLE_FONT_SIZE,
                                             "The Game"),
                  text_handler.register_text((150, 140),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "Jump by clicking or"),
                  text_handler.register_text((150, 160),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "pressing space or W"),
                  text_handler.register_text((150, 180),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "to avoid hitting"),
                  text_handler.register_text((150, 200),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "enemies"),
                  text_handler.register_text((150, 230),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "Everything speeds"),
                  text_handler.register_text((150, 250),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "up as the game"),
                  text_handler.register_text((150, 270),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "progresses"),
                  text_handler.register_text((150, 300),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "Press esc to pause"),
                  text_handler.register_text((150, 320),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "the game, A and D"),
                  text_handler.register_text((150, 340),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "or arrows to strafe,"),
                  text_handler.register_text((150, 360),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "and S or down to"),
                  text_handler.register_text((150, 380),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "quickfall"),
                  
                  text_handler.register_text((400, 100),
                                             (0, 0, 0),
                                             constants.MENU_MINOR_TITLE_FONT_SIZE,
                                             "Enemies"),
                  text_handler.register_text((410, 162.5),
                                             (0, 0, 0),
                                             constants.MENU_TINY_FONT_SIZE,
                                             "The Egg"),
                  text_handler.register_text((410, 215),
                                             (0, 0, 0),
                                             constants.MENU_TINY_FONT_SIZE,
                                             "The Chicken"),
                  text_handler.register_text((410, 235),
                                             (0, 0, 0),
                                             constants.MENU_TINY_FONT_SIZE,
                                             "(spawns at"),
                  text_handler.register_text((415, 255),
                                             (0, 0, 0),
                                             constants.MENU_TINY_FONT_SIZE,
                                             "1000 points)"),

                  text_handler.register_text((650, 100),
                                             (0, 0, 0),
                                             constants.MENU_MINOR_TITLE_FONT_SIZE,
                                             "Powerups"),
                  text_handler.register_text((660, 155),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "Extra heart"),
                  text_handler.register_text((660, 175),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "up to 5"),
                  text_handler.register_text((660, 225),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "X2 Score"),
                  text_handler.register_text((660, 245),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "for 4 secs"),
                  text_handler.register_text((660, 295),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "God Mode"),
                  text_handler.register_text((660, 315),
                                             (0, 0, 0),
                                             constants.MENU_SMALL_FONT_SIZE,
                                             "for 2 secs")]

HOW_TO_SPRITES = [sprite_handler.register_sprite((320, 140, 50, 50),
                                                 ["graphics/enemies/tweaking_egg_1.png", "graphics/enemies/tweaking_egg_2.png",
                                                  "graphics/enemies/tweaking_egg_3.png", "graphics/enemies/tweaking_egg_4.png"],
                                                 True,
                                                 None),
                  sprite_handler.register_sprite((320, 210, 50, 50),
                                                 ["graphics/enemies/chicken_1.png", "graphics/enemies/chicken_2.png"],
                                                 True,
                                                 None),
                   
                  sprite_handler.register_sprite((550, 140, 50, 50),
                                                 "graphics/level/heart.png",
                                                 True,
                                                 None),
                  sprite_handler.register_sprite((550, 210, 50, 50),
                                                 "graphics/powerups/double_score.png",
                                                 True,
                                                 None),
                  sprite_handler.register_sprite((550, 280, 50, 50),
                                                 "graphics/powerups/god_mode.png",
                                                 True,
                                                 None)]

def register_objects_states() -> None:
    """Registers the objects with the state handler. Needs to be in a function or python complains"""
    state_handler.register_object_state(SCORE_TEXT, "text", state_handler.PLAYING)
    state_handler.register_object_state(EGG_SPRITE, "sprite", [state_handler.PLAYING, state_handler.PAUSED])
    state_handler.register_object_state(GAME_OVER_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(GAME_OVER_SCORE_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(PLAY_AGAIN_BUTTON, "button", state_handler.DEAD)
    state_handler.register_object_state(DEATH_MAIN_MENU_BUTTON, "button", state_handler.DEAD)
    state_handler.register_object_state(LEADERBOARD_TEXT, "text", state_handler.DEAD)
    state_handler.register_object_state(MAIN_MENU_TITLE, "text", state_handler.MENU)
    state_handler.register_object_state(MENU_PLAY_BUTTON, "button", state_handler.MENU)
    state_handler.register_object_state(MENU_QUIT_BUTTON, "button", state_handler.MENU)
    state_handler.register_object_state(MENU_HOW_TO_BUTTON, "button", state_handler.MENU)
    state_handler.register_object_state(HOW_TO_TITLE, "text", state_handler.HOW_TO)
    state_handler.register_object_state(HOW_TO_BACK_BUTTON, "button", state_handler.HOW_TO)
    for entry in HOW_TO_ENTRIES:
        state_handler.register_object_state(entry, "text", state_handler.HOW_TO)
    for sprite in HOW_TO_SPRITES:
        state_handler.register_object_state(sprite, "sprite", state_handler.HOW_TO)