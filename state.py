import pygame
import constants

player_y_speed      = 0
player_is_alive     = True
player_animation    = "walk_1"
player_walk_frames  = 0
egg_animation       = "1"
egg_walk_frames     = 0
score               = 0
item_speed          = 5
double_jumped       = False
player_lives        = constants.PLAYER_SPAWN_LIVES
current_power_up    = None
god_mode_frames     = 0
double_score_frames = 0