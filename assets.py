# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import state
import input_handler

# Constant assets
BACKGROUND_SURFACE         = pygame.transform.scale(pygame.image.load("graphics/level/background.png").convert(), (1200, 400))
HEART_SURFACE              = pygame.transform.scale(pygame.image.load("graphics/level/heart.png").convert_alpha(),
                                                    (constants.HEART_SIZE, constants.HEART_SIZE))
GOLD_HEART_SURFACE         = pygame.transform.scale(pygame.image.load("graphics/level/heart_gold.png").convert_alpha(),
                                                    (constants.HEART_SIZE, constants.HEART_SIZE))
GAME_FONT                  = pygame.font.Font(pygame.font.get_default_font(), constants.DEFAULT_FONT_SIZE)
SMALL_FONT                 = pygame.font.Font(pygame.font.get_default_font(), constants.SMALL_FONT_SIZE)
LEADERBOARD_TEXT           = SMALL_FONT.render("Top Scores", True, 0)
LEADERBOARD_TEXT_RECTANGLE = LEADERBOARD_TEXT.get_rect(center=(600, 50))

# Non-constant assets
score_surface     = None
score_rectangle   = None
player_animations = {"walk_1": pygame.transform.scale(pygame.image.load("graphics/player/player_walk_1.png").convert_alpha(), (48, 64)),
                     "walk_2": pygame.transform.scale(pygame.image.load("graphics/player/player_walk_2.png").convert_alpha(), (48, 64)),
                     "jump":   pygame.transform.scale(pygame.image.load("graphics/player/player_jump.png").convert_alpha(),   (48, 64))}
player_surface    = player_animations["walk_1"]
player_rectangle  = player_surface.get_rect(bottomleft=(25, constants.GROUND_Y))

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
            if state.player_walk_frames == constants.FPS_CAP / constants.ANIMATION_FPS:
                state.player_walk_frames = 0
                state.player_animation = "walk_2"
        case "walk_2":
            state.player_walk_frames += 1
            if state.player_walk_frames == constants.FPS_CAP / constants.ANIMATION_FPS:
                state.player_walk_frames = 0
                state.player_animation = "walk_1"
    
    global player_surface, player_animations
    player_surface = player_animations[state.player_animation]