"""Improvement on the dino game left by the last intern
Read how_it_all_works.md for more detail

Author: @aesom-e @bassemfarid
"""

import init
from handlers import handle_events
import display
import state_handler
import objects

if __name__ == "__main__":
    # Once Python has figured everything out with the other files,
    # register the objects' states with the state handler
    objects.register_objects_states()

    while True:
        # Handle PyGame events
        handle_events()
        
        # Let the state handler do its job
        state_handler.handle()

        # Draw to the physical screen and enforce the FPS cap
        display.draw_frame_to_screen()
else:
    raise RuntimeError("The main.py file cannot be imported")