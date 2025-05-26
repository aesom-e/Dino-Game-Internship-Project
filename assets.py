import pygame
import constants

# Constant assets
SKY_SURFACE              = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURFACE           = pygame.image.load("graphics/level/ground.png").convert()
HEART_SURFACE            = pygame.transform.scale(pygame.image.load("graphics/level/heart.png").convert_alpha(), (constants.HEART_SIZE, constants.HEART_SIZE))
GAME_FONT                = pygame.font.Font(pygame.font.get_default_font(), constants.DEFAULT_FONT_SIZE)
GAME_OVER_TEXT           = GAME_FONT.render("Game Over!", True, constants.GAME_OVER_TEXT_COLOUR)
GAME_OVER_TEXT_RECTANGLE = GAME_OVER_TEXT.get_rect(center=(constants.WINDOW_WIDTH/2, constants.WINDOW_HEIGHT/2))

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