# The purpose of this module is to manage the game's current state (like PLAYING, DEAD, PAUSED, MENU)
# and run the majority of the game code

# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import handlers
import display
import input_handler
import objects

# Used so that code can be written like state_handler.current_state = state_handler.DEAD
PLAYING = "_playing"
DEAD    = "_dead"
PAUSED  = "_paused"
MENU    = "_menu"

current_state = PLAYING

def handle() -> None:
    """Catch-all function for handling the different possible game states"""
    global current_state
    match current_state:
        case "_playing":
            # Handle the game logic
            handlers.handle_score()
            handlers.handle_frame_counters()
            handlers.handle_moving_objects()
            handlers.handle_player_movement()
            handlers.handle_power_up_roll()
            handlers.handle_collisions()

            # Hide buttons that shouldn't be shown
            input_handler.set_button_status(objects.RESUME_GAME_BUTTON, False)

            # Draw the frame
            display.wipe()
            display.draw_background()
            display.draw_objects()

            handlers.handle_collisions()
        case "_dead":
            # Draw the death screen
            display.wipe()
            display.draw_death_screen()
        case "_paused":
            # Draw the frame like normal
            display.wipe()
            display.draw_background()
            display.draw_objects(update_sprites=False)

            # Blur the screen
            display.blur()

            # Show the pause menu buttons
            input_handler.set_button_status(objects.RESUME_GAME, True)
        case "_menu":
            pass
        case _:
            raise ValueError(f"current_state is an unknown value: {current_state}")