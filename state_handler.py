# The purpose of this module is to manage the game's current state (like PLAYING, DEAD, PAUSED, MENU)
# and run the majority of the game code

# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import handlers
import display
import input_handler
import text_handler
import objects

# Used so that code can be written like state_handler.current_state = state_handler.DEAD
PLAYING = "_playing"
DEAD    = "_dead"
PAUSED  = "_paused"
MENU    = "_menu"

current_state = PLAYING

_object_states = {}
def register_object_state(object_id: int, object_type: str, show_on_states: str | list[str] | None) -> None:
    """Registers an object's associated game state.
    Objects registered with a game state will be shown when the game is in that state; otherwise, they will be hidden
    
    Args:
        object_id (int): The ID of the object to register
        object_type (str): The type of object ("button", "text")
        show_on_states (str | list[str] | None): The states to show the object on. Hide on all others
    """
    # Get the function that is used to set the object's status
    match object_type:
        case "button":
            object_status_function = input_handler.set_button_status
        case "text":
            object_status_function = text_handler.set_text_status
        case _:
            raise ValueError(f"Unknown object type: {object_type}")
    
    # Add the object to the dictionary
    if not "all" in _object_states.keys():
        _object_states["all"] = []
    _object_states["all"].append([object_id, object_status_function])
    if show_on_states is not None:
        if isinstance(show_on_states, str):
            if not show_on_states in _object_states.keys():
                _object_states[show_on_states] = []
            _object_states[show_on_states].append([object_id, object_status_function])
        else:
            for state in show_on_states:
                if not state in _object_states.keys():
                    _object_states[state] = []
                _object_states[state].append([object_id, object_status_function])

def update_objects_state() -> None:
    """Updates the objects' states based on the current game state"""
    # Check that _object_states has even been populated
    if not "all" in _object_states.keys():
        return
    
    # Check if the current state has been populated, else hide everything
    if not current_state in _object_states.keys():
        for _object in _object_states["all"]:
            _object[1](_object[0], False)


    # Hide all objects that shouldn't be shown in the current state
    for _object in _object_states["all"]:
        _object[1](_object[0], _object in _object_states[current_state])

def handle() -> None:
    """Catch-all function for handling the different possible game states"""
    # Wipe the screen and update the objects' states
    display.wipe()
    update_objects_state()

    # Handle the current state's logic
    match current_state:
        case "_playing":
            # Handle the game logic
            handlers.handle_score()
            handlers.handle_frame_counters()
            handlers.handle_moving_objects()
            handlers.handle_player_movement()
            handlers.handle_power_up_roll()
            handlers.handle_collisions()

            # Draw the frame
            display.draw_background()
            display.draw_objects()

            handlers.handle_collisions()
        case "_dead":
            # Draw the frame
            display.update_death_screen()
            display.draw_objects()
        case "_paused":
            # Draw the frame like normal
            display.draw_background()
            display.draw_objects(update_sprites=False)

            # Blur the screen
            display.blur()

            # Draw the menu objects after the blur
            input_handler.draw_specifically(objects.RESUME_GAME_BUTTON)
            text_handler.draw_specifically(objects.PAUSED_GAME_MENU_TEXT)
        case "_menu":
            pass
        case _:
            raise ValueError(f"current_state is an unknown value: {current_state}")