# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

from collections.abc import Callable
import pygame
import assets
import rectangle

# Okay, so here's how it's going to work. There are going to be buttons. They are going to be clickable.
# This module will manage them. When you create a button, you are given its ID. You can modify a button with its ID.
# Buttons are linked to functions. When you click them, it calls the (void)(*function)(void) or whatever
# in this language.

# We are not allowed to use any higher level datatypes, so I have to structure it like this

# Colour C typedef:
# unsigned char red;
# unsigned char green;
# unsigned char blue;

# Button C typedef:
# Rectangle rectangle;
# Colour textColour;
# Colour backgroundColour;
# unsigned char fontSize;
# const char* text;
# void (*onClick)(void);
# int active; // If active is 0, it's hidden and clicking does not call onClick()

_buttons = []

def register_button(button_rectangle: tuple[float, float, float, float, str | None],
                    text_colour: tuple[int, int, int],
                    background_colour: tuple[int, int, int] | None,
                    font_size: int,
                    text: str,
                    on_click: Callable[[None], None]) -> int:
    """Registers a button with the input handler
    
    Args:
        button_rectangle (tuple[float, float, float, float, str | None]): The button's rectangle
        text_colour (tuple[int, int, int]): The colour of the button's text
        background_colour (tuple[int, int, int] | None): The colour of the button's background. None to make it transparent
        font_size(int): The font size of the button's text
        text (str): The button's text
        on_click (Callable[[None], None]): The function to call when the button is clicked

    Returns:
        int: The ID of the button which was just created
    """
    # Construct the font now to save time rendering
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)

    _buttons.append([rectangle.get_rectangle(button_rectangle), text_colour, background_colour, font, text, on_click, False])
    return len(_buttons)-1

def modify_button(button_id: int,
                  button_rectangle: tuple[float, float, float, float, str | None] = None,
                  text_colour: tuple[int, int, int] = None,
                  background_colour: tuple[int, int, int] | None = False, # Because None is an acceptable argument, I use False as default
                  font_size: int = None,
                  text: str = None,
                  on_click: Callable[[None], None] = None) -> None:
    """Modifies a button given its ID
    
    Args:
        button_id (int): The ID of the button to modify
        button_rectangle (tuple[float, float, float, float, str | None]): The new rectangle, leave blank to not modify
        text_colour (tuple[int, int, int]): The new text colour; leave blank to not modify
        background_colour (tuple[int, int, int] | None): The new background colour; leave blank to not modify
        font_size (int): The new font size; leave blank to not modify
        text (str): The new text; leave blank to not modify
        on_click (Callable[[None], None]): The new function to call on click; leave blank to not modify
    """
    if rectangle is not None:
        _buttons[button_id][0] = rectangle.get_rectangle(button_rectangle)
    if text_colour is not None:
        _buttons[button_id][1] = text_colour
    if background_colour is not False:
        _buttons[button_id][2] = background_colour
    if font_size is not None:
        _buttons[button_id][3] = pygame.font.Font(pygame.font.get_default_font(), font_size)
    if text is not None:
        _buttons[button_id][4] = text
    if on_click is not None:
        _buttons[button_id][5] = on_click

def set_button_status(button_id: int, active: bool) -> None:
    """Sets the status of a single button
    
    Args:
        button_id (int): The ID of the button to modify
        active (bool): True to make the button active, False to deactivate it
    """
    _buttons[button_id][6] = active

def draw_buttons() -> None:
    """Draws the active buttons"""
    for button in _buttons:
        # Get all of the different properties of the button
        rectangle, text_colour, background_colour, font, text, on_click, active = tuple(button)

        if active:
            # Draw the button background
            if background_colour is not None:
                pygame.draw.rect(assets.screen, background_colour, rectangle)

            # Render the button text
            text_surface = font.render(text, True, text_colour)
            text_rectangle = text_surface.get_rect()
            text_rectangle.center = (rectangle[0] + rectangle[2] // 2, rectangle[1] + rectangle[3] // 2)
            assets.screen.blit(text_surface, text_rectangle)


def handle_click(click_pos: tuple[int, int]) -> bool:
    """Handles a pygame click and calls any button the user clicked on
    
    Args:
        click_pos (tuple[int, int]): The position of the click on the screen
    
    Returns:
        bool: True to cancel the event, False to allow it
    """
    cancel_event = False
    for button in _buttons:
        # Check if the button is active
        if button[6]:
            # Check if the click was on the button
            if button[0][0] <= click_pos[0] <= button[0][0] + button[0][2] and \
               button[0][1] <= click_pos[1] <= button[0][1] + button[0][3]:
                # Call the function associated with the button
                if button[5] is not None:
                    button[5]()

                    # Tell the event handler to cancel the event
                    cancel_event = True
    return cancel_event