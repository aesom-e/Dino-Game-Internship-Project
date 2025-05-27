import pygame
import constants
import assets
import state

def wipe() -> None:
    """Wipes the screen"""
    assets.screen.fill(constants.ALIVE_BACKGROUND_COLOUR)

def draw_background() -> None:
    """Draws the background of the game"""
    assets.screen.blit(assets.SKY_SURFACE, (0, 0))
    assets.screen.blit(assets.GROUND_SURFACE, (0, constants.GROUND_Y))
    assets.screen.blit(assets.score_surface, assets.score_rectangle)

    # Draw the hearts
    for _ in range(state.player_lives):
        heart_rectangle = (_*constants.HEART_SIZE, 0)
        assets.screen.blit(assets.HEART_SURFACE, heart_rectangle)

def draw_death_screen() -> None:
    """Draw the death screen"""
    assets.screen.fill(constants.DEAD_BACKGROUND_COLOUR)
    assets.screen.blit(assets.GAME_OVER_TEXT, assets.GAME_OVER_TEXT_RECTANGLE)

def draw_objects() -> None:
    """Draw the objects on screen"""
    # Draw the egg
    assets.update_egg_sprite()
    assets.screen.blit(assets.egg_surface, assets.egg_rectangle)
    
    # Draw the player
    assets.screen.blit(assets.player_surface, assets.player_rectangle)

    # Draw the power-up
    if state.current_power_up is not None:
        if assets.power_up_rectangle.right > 0:
            assets.screen.blit(state.current_power_up[0], assets.power_up_rectangle)

def draw_frame_to_screen() -> None:
    """Draws the frame in the frame buffer onto the screen and cap FPS"""
    pygame.display.flip()
    assets.clock.tick(constants.FPS_CAP)