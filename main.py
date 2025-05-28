import init
from handlers import handle_events
import display
import state_handler

if __name__ == "__main__":
    while True:
        # Handle pygame events
        handle_events()
        
        # Let the state handle do its job
        state_handler.handle()
        
        # Draw to the physical screen and enforce the FPS cap
        display.draw_frame_to_screen()
else:
    raise RuntimeError("The main.py file cannot be imported")