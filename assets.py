# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import state
import input_handler

# Constant assets
SKY_SURFACE                = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURFACE             = pygame.image.load("graphics/level/ground.png").convert()
HEART_SURFACE              = pygame.transform.scale(pygame.image.load("graphics/level/heart.png").convert_alpha(), (constants.HEART_SIZE, constants.HEART_SIZE))
GAME_FONT                  = pygame.font.Font(pygame.font.get_default_font(), constants.DEFAULT_FONT_SIZE)
SMALL_FONT                 = pygame.font.Font(pygame.font.get_default_font(), constants.SMALL_FONT_SIZE)
GAME_OVER_TEXT             = GAME_FONT.render("Game Over!", True, constants.GAME_OVER_TEXT_COLOUR)
GAME_OVER_TEXT_RECTANGLE   = GAME_OVER_TEXT.get_rect(center=(200, constants.WINDOW_HEIGHT/2-25))
LEADERBOARD_TEXT           = SMALL_FONT.render("Top Scores", True, constants.GAME_OVER_TEXT_COLOUR)
LEADERBOARD_TEXT_RECTANGLE = LEADERBOARD_TEXT.get_rect(center=(600, 50))

# Non-constant assets
score_surface     = None
score_rectangle   = None
player_surface    = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rectangle  = player_surface.get_rect(bottomleft=(25, constants.GROUND_Y))
player_animations = {"walk_1": pygame.image.load("graphics/player/player_walk_1.png").convert_alpha(),
                     "walk_2": pygame.image.load("graphics/player/player_walk_2.png").convert_alpha(),
                     "jump":   pygame.image.load("graphics/player/player_jump.png").convert_alpha()}
egg_surface       = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rectangle     = egg_surface.get_rect(bottomleft=(constants.WINDOW_WIDTH, constants.GROUND_Y))
egg_animations    = {"1": pygame.image.load("graphics/egg/egg_1.png").convert_alpha(),
                    "2": pygame.image.load("graphics/egg/egg_2.png").convert_alpha()}
power_up_rectangle  = None

def update_player_sprite() -> None:
    """Updates the player's sprite. Called each frame"""
    if not state.player_y_speed:
        state.player_animation = "walk_2"
    elif state.player_y_speed > 0:
        state.player_animation = "jump"
    
    # Switch the walk animation
    match state.player_animation:
        case "walk_1":
            state.player_walk_frames += 1
            if state.player_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.player_walk_frames = 0
                state.player_animation = "walk_2"
        case "walk_2":
            state.player_walk_frames += 1
            if state.player_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.player_walk_frames = 0
                state.player_animation = "walk_1"
    
    global player_surface, player_animations
    player_surface = player_animations[state.player_animation]

def update_egg_sprite() -> None:
    """Updates the egg's sprite. Called each frame"""
    match state.egg_animation:
        case "1":
            state.egg_walk_frames += 1
            if state.egg_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.egg_walk_frames = 0
                state.egg_animation = "2"
        case "2":
            state.egg_walk_frames += 1
            if state.egg_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.egg_walk_frames = 0
                state.egg_animation = "1"
    
    global egg_surface, egg_animations
    egg_surface = egg_animations[state.egg_animation]