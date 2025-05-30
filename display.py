# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import assets
import state
import input_handler
import text_handler
import objects

def wipe() -> None:
    """Wipes the screen"""
    assets.screen.fill(0)

def draw_background() -> None:
    """Draws the background of the game"""
    assets.screen.blit(assets.SKY_SURFACE, (0, 0))
    assets.screen.blit(assets.GROUND_SURFACE, (0, constants.GROUND_Y))

    # Draw the hearts
    for _ in range(state.player_lives):
        heart_rectangle = (_*constants.HEART_SIZE, 0)
        assets.screen.blit(assets.HEART_SURFACE, heart_rectangle)

def update_death_screen() -> None:
    """Updates the objects associated with the death screen"""
    # Update the player's score
    #text_handler.modify_text(objects.GAME_OVER_SCORE_TEXT, text=f"Your Score: {state.score_on_death}")
    
    # Draw the leaderboard
    """assets.screen.blit(assets.LEADERBOARD_TEXT, assets.LEADERBOARD_TEXT_RECTANGLE)
    with open("leaderboard.txt", "r") as f:
        records = sorted([int(_) for _ in f.read().split('\n') if _], reverse=True)
    for _, record in enumerate(records):
        record_text = assets.SMALL_FONT.render(str(record), True, constants.LEADERBOARD_TEXT_COLOUR)
        record_text_rectangle = record_text.get_rect(center=(600, 30*_+80))
        assets.screen.blit(record_text, record_text_rectangle)"""

def draw_objects(update_sprites: bool=True) -> None:
    """Draw the objects on screen
    
    Args:
        update_sprites (bool): True to update animations, False to not. Default True
    """
    # Draw the egg
    if update_sprites:
        assets.update_egg_sprite()
    assets.screen.blit(assets.egg_surface, assets.egg_rectangle)
    
    # Draw the player
    assets.screen.blit(assets.player_surface, assets.player_rectangle)

    # Draw the power-up
    if state.current_power_up is not None:
        if assets.power_up_rectangle.right > 0:
            assets.screen.blit(state.current_power_up[0], assets.power_up_rectangle)

    # Draw the objects registered with the different handlers
    input_handler.draw_buttons()
    text_handler.draw_text_objects()

def draw_frame_to_screen() -> None:
    """Draws the frame in the frame buffer onto the screen and performs other tasks for the new frame"""
    pygame.display.flip()
    assets.clock.tick(constants.FPS_CAP)

def blur() -> None:
    """Blurs the screen"""
    # The way we go about this is to downscale the screen and then re-upscale it,
    # losing information and bluring the screen
    downscale_size = (int(constants.WINDOW_WIDTH*(1/constants.BLUR_POWER)), int(constants.WINDOW_HEIGHT*(1/constants.BLUR_POWER)))
    downscaled_surface = pygame.transform.smoothscale(assets.screen.copy(), downscale_size)
    blurred_surface = pygame.transform.smoothscale(downscaled_surface, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))

    # Now draw the blurred surface
    assets.screen.blit(blurred_surface, (0, 0))