import pygame
import random
import init
import constants
import assets
import state
import power_ups

# Helper functions
def can_jump() -> bool:
    """Checks if the player can jump
    
    Returns:
        bool: True if the player can jump, False if not
    """
    if assets.player_rectangle.bottom >= constants.GROUND_Y:
        return True
    elif not state.double_jumped:
        return True
    return False


def die() -> None:
    """Handles resetting all state variables when the player dies"""
    state.player_is_alive = False
    state.score = 0
    state.item_speed = 5
    state.player_lives = constants.PLAYER_SPAWN_LIVES

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
            if state.player_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.player_walk_frames = 0
                state.player_animation = "walk_2"
        case "walk_2":
            state.player_walk_frames += 1
            if state.player_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.player_walk_frames = 0
                state.player_animation = "walk_1"
    
    assets.player_surface = assets.player_animations[state.player_animation]

def update_egg_sprite() -> None:
    """Updates the egg's sprite. Called each frame"""
    match state.egg_animation:
        case "1":
            state.egg_walk_frames += 1
            if state.egg_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.egg_walk_frames = 0
                state.egg_animation = "2"
        case "2":
            state.egg_walk_frames += 1
            if state.egg_walk_frames == constants.WALK_ANIMATION_DELAY:
                state.egg_walk_frames = 0
                state.egg_animation = "1"
    
    assets.egg_surface = assets.egg_animations[state.egg_animation]

def draw_hearts() -> None:
    """Draws the player's lives to the top left corner of the screen"""
    for _ in range(state.player_lives):
        heart_rectangle = (_*constants.HEART_SIZE, 0)
        assets.screen.blit(assets.HEART_SURFACE, heart_rectangle)

# Main loop (I'm sorry for this code)
while True:
    # Handle pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif state.player_is_alive:
            # Handle jumping
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN) and can_jump():
                if assets.player_rectangle.bottom < constants.GROUND_Y:
                    state.double_jumped = True
                state.player_y_speed = constants.JUMP_GRAVITY_START_SPEED
        else:
            # Handle restarting the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state.player_is_alive = True
                assets.egg_rectangle.left = constants.WINDOW_WIDTH
    
    # Handle the game itself
    if state.player_is_alive:
        # Adjust the score
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

        # Decrement the frame counters
        if state.double_score_frames:
            state.double_score_frames -= 1
        if state.god_mode_frames:
            state.god_mode_frames -= 1

        # Wipe the screen
        assets.screen.fill(constants.ALIVE_BACKGROUND_COLOUR)

        # Draw the constant-positioned assets to the screen
        assets.screen.blit(assets.SKY_SURFACE, (0, 0))
        assets.screen.blit(assets.GROUND_SURFACE, (0, constants.GROUND_Y))
        assets.screen.blit(assets.score_surface, assets.score_rectangle)
        draw_hearts()

        # Handle then draw the egg
        assets.egg_rectangle.x -= state.item_speed
        if assets.egg_rectangle.right <= 0:
            assets.egg_rectangle.left = constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE)
            if state.item_speed < constants.ITEM_SPEED_CAP:
                state.item_speed += 1 # Increase the egg speed each loop to make the game harder
        update_egg_sprite()
        assets.screen.blit(assets.egg_surface, assets.egg_rectangle)

        # Handle then draw the player
        state.player_y_speed -= 1
        update_player_sprite()
        assets.player_rectangle.y -= state.player_y_speed # y=0 is at the top
        if assets.player_rectangle.bottom >= constants.GROUND_Y:
            # Handle the player hitting the ground
            assets.player_rectangle.bottom = constants.GROUND_Y
            state.double_jumped = False
        assets.screen.blit(assets.player_surface, assets.player_rectangle)

        # Handle then draw power ups
        if state.current_power_up is not None:
            assets.power_up_rectangle.x -= state.item_speed
            if assets.power_up_rectangle.right <= 0:
                state.current_power_up = None
                assets.power_up_rectangle = None
            else:
                assets.screen.blit(state.current_power_up[0], assets.power_up_rectangle)
        else:
            # Roll for a power up
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

        # Handle collisions
        if assets.egg_rectangle.colliderect(assets.player_rectangle) and not state.god_mode_frames:
            state.player_lives -= 1
            # Reset the egg position to avoid multiple collisions
            assets.egg_rectangle.left = constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE)
            if not state.player_lives:
                die()
        if assets.power_up_rectangle is not None and assets.power_up_rectangle.colliderect(assets.player_rectangle):
            # Trigger the powerup then delete it
            state.current_power_up[1]()
            state.current_power_up = None
            assets.power_up_rectangle = None
    else:
        # Draw the death screen
        assets.screen.fill(constants.DEAD_BACKGROUND_COLOUR)
        assets.screen.blit(assets.GAME_OVER_TEXT, assets.GAME_OVER_TEXT_RECTANGLE)
    
    # Draw to the physical screen and enforce the FPS cap
    pygame.display.flip()
    assets.clock.tick(constants.FPS_CAP)