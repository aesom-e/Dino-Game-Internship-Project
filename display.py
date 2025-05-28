# Protection for running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

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

    # Draw the player's score
    player_score = assets.SMALL_FONT.render(f"Your Score: {state.score_on_death}",
                                            True,
                                            constants.GAME_OVER_TEXT_COLOUR)
    player_score_rectangle = player_score.get_rect(center=(200, constants.WINDOW_HEIGHT/2+50))
    assets.screen.blit(player_score, player_score_rectangle)
    
    # Draw the leaderboard
    assets.screen.blit(assets.LEADERBOARD_TEXT, assets.LEADERBOARD_TEXT_RECTANGLE)
    with open("leaderboard.txt", "r") as f:
        records = sorted([int(_) for _ in f.read().split('\n') if _], reverse=True)
    for _, record in enumerate(records):
        record_text = assets.SMALL_FONT.render(str(record), True, constants.LEADERBOARD_TEXT_COLOUR)
        record_text_rectangle = record_text.get_rect(center=(600, 30*_+80))
        assets.screen.blit(record_text, record_text_rectangle)

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