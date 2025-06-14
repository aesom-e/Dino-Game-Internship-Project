# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

WINDOW_HEIGHT               = 400
WINDOW_WIDTH                = 800
WINDOW_TITLE                = "Farm Run"
FPS_CAP                     = 60
GROUND_Y                    = 315
ANIMATION_FPS               = 10            # For all animations
JUMP_GRAVITY_START_SPEED    = 15            # The speed at which the player jumps
QUICKFALL_SPEED             = 20
DEFAULT_FONT_SIZE           = 50
SMALL_FONT_SIZE             = 26
MENU_TITLE_FONT_SIZE        = 40
MENU_MINOR_TITLE_FONT_SIZE  = 35
MENU_FONT_SIZE              = 30
MENU_SMALL_FONT_SIZE        = 20
MENU_TINY_FONT_SIZE         = 15
ITEM_RESPAWN_VARIANCE       = 100
PLAYER_SPAWN_LIVES          = 3
MAX_LIVES                   = 5
ITEM_SPEED_CAP              = 15
HEART_SIZE                  = 40
POWER_UP_SIZE               = 50
EGG_SIZE                    = 50
CHICKEN_SIZE                = 50
CHICKEN_HEIGHT              = 100
CHICKEN_SPAWN_SCORE         = 1000
POWER_UP_CHANCE             = 300           # There is a 1/POWER_UP_CHANCE each frame for a powerup to spawn
BLUR_POWER                  = 2.5
PLAYER_RUN_BOUNDARY         = 150
PLAYER_RUN_SPEED            = 3
LEADERBOARD_TEXT_COLOUR     = (3, 115, 252)
MAIN_MENU_BACKGROUND_COLOUR = (37, 93, 184)