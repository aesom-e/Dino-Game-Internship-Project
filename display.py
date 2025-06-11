# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import assets
import state
import input_handler
import text_handler
import sprite_handler
import state_handler

def wipe() -> None:
    """Wipes the screen"""
    assets.screen.fill(0)

def draw_solid_background(colour: tuple[int, int, int]) -> None:
    """Draws a solid background to the screen
    
    Args:
        colour (tuple[int, int, int]): The colour to fill the background with
    """
    assets.screen.fill(colour)

def draw_background() -> None:
    """Draws the background of the game"""
    assets.screen.blit(assets.BACKGROUND_SURFACE, (state.background_x, 0))

    # Move the background
    if state_handler.current_state != state_handler.PAUSED:
        state.background_x -= 1
        if state.background_x < -399:
            assets.screen.blit(assets.BACKGROUND_SURFACE, (state.background_x + 1199, 0))
        if state.background_x < -1199:
            state.background_x += 1200

    # Draw the hearts
    for _ in range(state.player_lives):
        heart_rectangle = (_*constants.HEART_SIZE, 0)
        assets.screen.blit(assets.GOLD_HEART_SURFACE if state.god_mode_frames else assets.HEART_SURFACE,
                           heart_rectangle)

def draw_objects(draw_player: bool=True) -> None:
    """Draw the objects on screen
    
    Args:
        draw_player (bool): True to draw the player, False to not. Default True
    """    
    # Draw the player
    if draw_player: assets.screen.blit(assets.player_surface, assets.player_rectangle)

    # Draw the objects registered with the different handlers
    input_handler.draw_buttons()
    text_handler.draw_text_objects()
    sprite_handler.draw_sprites()

def draw_frame_to_screen() -> None:
    """Draws the frame in the frame buffer onto the screen and performs other tasks for the new frame"""
    pygame.display.flip()
    assets.clock.tick(constants.FPS_CAP)

def draw_leaderboard() -> None:
    """Draws the leaderboard text"""
    with open("leaderboard.txt", "r") as f:
        records = sorted([int(_) for _ in f.read().split('\n') if _], reverse=True)
    
    # This doesn't use the text handler for pure simplicity
    for _, record in enumerate(records):
        record_text = assets.SMALL_FONT.render(f"#{_+1} {record}", True, constants.LEADERBOARD_TEXT_COLOUR)
        record_text_rectangle = record_text.get_rect(center=(600, 30*_+80))
        assets.screen.blit(record_text, record_text_rectangle)

def blur() -> None:
    """Blurs the screen"""
    # The way we go about this is to downscale the screen and then re-upscale it,
    # losing information and bluring the screen
    downscale_size = (int(constants.WINDOW_WIDTH*(1/constants.BLUR_POWER)), int(constants.WINDOW_HEIGHT*(1/constants.BLUR_POWER)))
    downscaled_surface = pygame.transform.smoothscale(assets.screen.copy(), downscale_size)
    blurred_surface = pygame.transform.smoothscale(downscaled_surface, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))

    # Now draw the blurred surface
    assets.screen.blit(blurred_surface, (0, 0))