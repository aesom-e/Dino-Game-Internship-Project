# Protection for running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import constants
import assets

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

def can_jump() -> bool:
    """Checks if the player can jump
    
    Returns:
        bool: True if the player can jump, False if not
    """
    global double_jumped
    if assets.player_rectangle.bottom >= constants.GROUND_Y:
        return True
    elif not double_jumped:
        return True
    return False