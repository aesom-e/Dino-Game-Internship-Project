# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import constants
import assets
import state
import power_ups
import random
import state_handler
import input_handler
import text_handler
import sprite_handler
import objects
import sound

def handle_events() -> None:
    """Handles PyGame events within the game"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        
        # Pass any clicks to the input handler
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_handler.handle_click(pygame.mouse.get_pos()):
                return
        
        # Handle any outstanding events
        match state_handler.current_state:
            case state_handler.PLAYING:
                # Handle jumping
                if ((event.type == pygame.KEYDOWN and
                     (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP))
                   or event.type == pygame.MOUSEBUTTONDOWN) and state.can_jump():
                    if assets.player_rectangle.bottom < constants.GROUND_Y:
                        state.double_jumped = True
                    state.player_y_speed = constants.JUMP_GRAVITY_START_SPEED
                    sound.play("jump.wav")

                # Handle quickfalling
                elif event.type == pygame.KEYDOWN and \
                     (event.key == pygame.K_s or event.key == pygame.K_DOWN) and \
                     assets.player_rectangle.bottom < constants.GROUND_Y:
                    state.player_y_speed = -constants.QUICKFALL_SPEED
                
                # Handle pausing
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state_handler.current_state = state_handler.PAUSED
            case state_handler.DEAD:
                # Handle restarting the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    state.player_is_alive = True
                    reset_state()
                    state_handler.current_state = state_handler.PLAYING
            case state_handler.PAUSED:
                # Handle unpausing
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state_handler.current_state = state_handler.PLAYING
            case state_handler.MENU:
                pass
            case state_handler.HOW_TO:
                # Handle going back
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state_handler.current_state = state_handler.MENU
            case _:
                raise ValueError(f"Unknown current_state: {state_handler.current_state}")

def handle_score() -> None:
    """Handles the score incrementing each frame"""
    if state.double_score_frames:
        state.score += 2
        text_handler.modify_text(objects.SCORE_TEXT, colour=(247, 216, 10), text=str(state.score))
    else:
        state.score += 1
        text_handler.modify_text(objects.SCORE_TEXT, colour=(0, 0, 0), text=str(state.score))

def handle_frame_counters() -> None:
    """Handles the frame counters"""
    if state.double_score_frames:
        state.double_score_frames -= 1
    if state.god_mode_frames:
        state.god_mode_frames -= 1

def handle_moving_objects() -> None:
    """Handles the movement of objects like the egg and power-ups"""
    # Handle the movement of the egg
    sprite_handler.move_sprite(objects.EGG_SPRITE, (-state.item_speed, 0))
    if sprite_handler.get_sprite_position(objects.EGG_SPRITE)[0] <= -constants.EGG_SIZE:
        sprite_handler.set_sprite_position(objects.EGG_SPRITE, (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE),
                                                                constants.GROUND_Y - constants.EGG_SIZE - 8))
        if state.item_speed < constants.ITEM_SPEED_CAP:
            state.item_speed += 1 # Increase the egg speed each loop to make the game harder
    
    # Handle the movement of the chicken
    if state.score > constants.CHICKEN_SPAWN_SCORE and not state.chicken_spawn_delay:
        sprite_handler.set_sprite_status(objects.CHICKEN_SPRITE, True)
        sprite_handler.move_sprite(objects.CHICKEN_SPRITE, (-state.item_speed*0.75, 0))
        if sprite_handler.get_sprite_position(objects.CHICKEN_SPRITE)[0] <= -constants.CHICKEN_SIZE:
            sprite_handler.set_sprite_position(objects.CHICKEN_SPRITE, (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE),
                                                                        constants.GROUND_Y - constants.CHICKEN_SIZE - constants.CHICKEN_HEIGHT))
            # Create a delay before the chicken spawns again
            state.chicken_spawn_delay = random.randint(30, 90)
            sprite_handler.set_sprite_status(objects.CHICKEN_SPRITE, False)
    else:
        sprite_handler.set_sprite_status(objects.CHICKEN_SPRITE, False)
        if state.chicken_spawn_delay: state.chicken_spawn_delay -= 1

    # Handle the movement of the power-ups
    if state.current_power_up is not None:
        sprite_handler.move_sprite(objects.POWER_UP_SPRITE, (-state.item_speed, 0))
        if sprite_handler.get_sprite_position(objects.POWER_UP_SPRITE)[0] <= 0:
            sprite_handler.set_sprite_status(objects.POWER_UP_SPRITE, False)
            state.current_power_up = None

def handle_player_movement() -> None:
    """Handle the player's movement"""
    state.player_y_speed -= 1
    assets.update_player_sprite()
    assets.player_rectangle.y -= state.player_y_speed # y=0 is at the top
    if assets.player_rectangle.bottom >= constants.GROUND_Y:
        # Handle the player hitting the ground
        assets.player_rectangle.bottom = constants.GROUND_Y
        state.double_jumped = False

def handle_power_up_roll() -> None:
    """Handle the rolling for a power-up"""
    if state.current_power_up is None:
        if not random.randint(0, constants.POWER_UP_CHANCE):
            state.current_power_up = random.choice(power_ups.table)
            
            # Make sure an extra life doesn't spawn when the player can't collect one
            if state.current_power_up == power_ups.table[0] and state.player_lives == constants.MAX_LIVES:
                state.current_power_up = power_ups.table[random.randint(1, len(power_ups.table)-1)]

            rectangle_position = (constants.WINDOW_WIDTH - random.randint(0, constants.ITEM_RESPAWN_VARIANCE) + constants.POWER_UP_SIZE,
                                  constants.GROUND_Y - constants.POWER_UP_SIZE)
            
            # Modift the power up object and spawn it
            sprite_handler.modify_sprite(objects.POWER_UP_SPRITE, sprite_rectangle=(rectangle_position[0], rectangle_position[1],
                                                                                    constants.POWER_UP_SIZE, constants.POWER_UP_SIZE),
                                                                  image_path=state.current_power_up[0],
                                                                  transparent=True,
                                                                  on_collision=state.current_power_up[1])
            sprite_handler.set_sprite_status(objects.POWER_UP_SPRITE, True)

def handle_player_strafing() -> None:
    """Handles the left and right strafing of the player"""
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and assets.player_rectangle.left > 0:
        assets.player_rectangle.left -= constants.PLAYER_RUN_SPEED
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and assets.player_rectangle.right < constants.PLAYER_RUN_BOUNDARY:
        assets.player_rectangle.left += constants.PLAYER_RUN_SPEED

def handle_death() -> None:
    """Called when the player dies. Handles the resetting of state variables and leaderboard"""    
    # Update the score display
    text_handler.modify_text(objects.GAME_OVER_SCORE_TEXT, text=f"Your Score: {state.score}")

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
    reset_state()

    # Set the game state
    state_handler.current_state = state_handler.DEAD

def reset_state() -> None:
    """Resets all the state variables and destroy temporary objects"""
    # Destroy temporary objects
    sprite_handler.set_sprite_status(objects.POWER_UP_SPRITE, False)
    state.current_power_up = None
    sprite_handler.set_sprite_status(objects.CHICKEN_SPRITE, False)

    # Reset state
    state.player_is_alive = False
    state.score = 0
    state.item_speed = 5
    state.player_lives = constants.PLAYER_SPAWN_LIVES
    state.player_y_speed = 0
    state.double_jumped = False
    assets.player_rectangle = assets.player_surface.get_rect(bottomleft=(25, constants.GROUND_Y))
    sprite_handler.set_sprite_position(objects.EGG_SPRITE, (-1000, 0))
    sprite_handler.set_sprite_position(objects.CHICKEN_SPRITE, (-1000, 0))
    state.god_mode_frames = 0
    state.double_score_frames = 0
    sprite_handler.set_sprite_status(objects.POWER_UP_SPRITE, False)
    state.current_power_up = False
    state.player_animation = "walk_1"
    state.background_x = 0