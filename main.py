import pygame
import random
import init
import constants
import assets
import state
import power_ups
from handlers import *
import display

if __name__ == "__main__":
    while True:
        # Handle pygame events
        handle_events()
        
        # Handle the game itself
        if state.player_is_alive:
            # Handle the game logic
            handle_score()
            handle_frame_counters()
            handle_moving_objects()
            handle_player_movement()
            handle_power_up_roll()
            handle_collisions()

            # Draw the frame
            display.wipe()
            display.draw_background()
            display.draw_objects()

            handle_collisions()
        else:
            # Draw the death screen
            display.wipe()
            display.draw_death_screen()
        
        # Draw to the physical screen and enforce the FPS cap
        display.draw_frame_to_screen()