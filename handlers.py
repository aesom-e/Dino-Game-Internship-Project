# Protection for running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import assets
import state
import power_ups
import random

def handle_events() -> None:
    """Handles pygame events within the game"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif state.player_is_alive:
            # Handle jumping
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN) and state.can_jump():
                if assets.player_rectangle.bottom < constants.GROUND_Y:
                    state.double_jumped = True
                state.player_y_speed = constants.JUMP_GRAVITY_START_SPEED
        else:
            # Handle restarting the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state.player_is_alive = True
                assets.egg_rectangle.left = constants.WINDOW_WIDTH

def handle_score() -> None:
    """Handles the score incrementing each frame"""
    if state.double_score_frames:
        state.score += 2
        assets.score_surface = assets.GAME_FONT.render(str(state.score),
                                                        True,
                                                        constants.POWER_UP_TEXT_COLOUR)
    else:
        state.score += 1
        assets.score_surface = assets.GAME_FONT.render(str(state.score),
                                                        True,
                                                        constants.SCORE_TEXT_COLOUR)
    assets.score_rectangle = assets.score_surface.get_rect(center=(constants.WINDOW_WIDTH/2, 50))

def handle_frame_counters() -> None:
    """Handles the frame counters"""
    if state.double_score_frames:
        state.double_score_frames -= 1
    if state.god_mode_frames:
        state.god_mode_frames -= 1

def handle_moving_objects() -> None:
    """Handles the movement of objects like the egg and power-ups"""
    # Handle the movement of an egg
    assets.egg_rectangle.x -= state.item_speed
    if assets.egg_rectangle.right <= 0:
        assets.egg_rectangle.left = constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE)
        if state.item_speed < constants.ITEM_SPEED_CAP:
            state.item_speed += 1 # Increase the egg speed each loop to make the game harder
    
    # Handle the movement of the power-ups
    if assets.power_up_rectangle is not None:
        assets.power_up_rectangle.x -= state.item_speed
        if assets.power_up_rectangle.right <= 0:
            state.current_power_up = None
            assets.power_up_rectangle = None

def handle_player_movement() -> None:
    """Handle the player's movement"""
    state.player_y_speed -= 1
    assets.update_player_sprite()
    assets.player_rectangle.y -= state.player_y_speed # y=0 is at the top
    if assets.player_rectangle.bottom >= constants.GROUND_Y:
        # Handle the player hitting the ground
        assets.player_rectangle.bottom = constants.GROUND_Y
        state.double_jumped = False

def handle_collisions() -> None:
    """Self-explanatory. I think most of these don't even need docstrings"""
    if assets.egg_rectangle.colliderect(assets.player_rectangle):
        if not state.god_mode_frames:
            state.player_lives -= 1
        # Reset the egg position to avoid multiple collisions
        assets.egg_rectangle.left = constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE)
        if not state.player_lives:
            handle_death()
    if assets.power_up_rectangle is not None and assets.power_up_rectangle.colliderect(assets.player_rectangle) and state.current_power_up:
        # Trigger the powerup then delete it
        state.current_power_up[1]()
        state.current_power_up = None
        assets.power_up_rectangle = None

def handle_power_up_roll() -> None:
    """Handle the rolling for a power-up"""
    if state.current_power_up is None:
        if not random.randint(0, constants.POWER_UP_CHANCE):
            state.current_power_up = random.choice(power_ups.table)
            
            # Make sure an extra life doesn't spawn when the player can't collect one
            if state.current_power_up == power_ups.table[0] and state.player_lives == constants.MAX_LIVES:
                state.current_power_up = power_ups.table[random.randint(1, len(power_ups.table)-1)]

            rectangle_position = (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE), constants.GROUND_Y)
            assets.power_up_rectangle = state.current_power_up[0].get_rect(bottomleft=rectangle_position)
            
            # Ensure the egg won't collide with the rectangle
            if assets.egg_rectangle.colliderect(assets.power_up_rectangle):
                state.current_power_up = None
            else: 
                assets.screen.blit(state.current_power_up[0], assets.power_up_rectangle)

def handle_death() -> None:
    """Called when the player dies. Handles the resetting of state variables and leaderboard"""
    # Handle the leaderboard
    leaderboard = open("leaderboard.txt", "r")
    # Read the current records
    records = [int(_) for _ in leaderboard.read().split('\n') if _]

    # Add the current score into records if it fits
    records.append(state.score)
    records.sort(reverse=True)
    if len(records) > 10:
        records.pop()

    # Clear leaderboards.txt
    leaderboard.close()
    leaderboard = open("leaderboard.txt", "w")

    # Write the updated records
    for _, record in enumerate(records):
        leaderboard.write(str(record))
        if _ != len(records)-1:
            leaderboard.write('\n')
    leaderboard.close()

    # Reset state variables
    state.player_is_alive = False
    state.score = 0
    state.item_speed = 5
    state.player_lives = constants.PLAYER_SPAWN_LIVES