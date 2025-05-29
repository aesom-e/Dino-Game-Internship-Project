from collections.abc import Callable
import pygame
import assets

# Okay, so here's how it's going to work. There are going to be buttons. They are going to be clickable.
# This module will manage them. When you create a button, you are given its ID. You can modify a button with its ID.
# Buttons are linked to functions. When you click them, it calls the (void)(*function)(void) or whatever
# in this language.

# We are not allowed to use any higher level datatypes, so I have to structure it like this

# Rectangle C typedef:
# unsigned short x;
# unsigned short y;
# unsigned short width;
# unsigned short height;

# Button C typedef:
# Rectangle rectangle;
# unsigned textColour;
# unsigned backgroundColour;
# unsigned char fontSize;
# const char* text;
# void (*onClick)(void);
# int active; // If active is 0, it's hidden and clicking does not call onClick()

buttons = []

def register_button(rectangle: tuple[int, int, int, int],
                    text_colour: int,
                    background_colour: int,
                    font_size: int,
                    text: str,
                    on_click: Callable[[None], None]) -> int:
    """Registers a button with the input handler
    
    Args:
        rectangle (tuple[int, int, int, int]): The button's rectangle
        text_colour (int): The colour of the button's text
        background_colour (int): The colour of the button's background
        font_size(int): The font size of the button's text
        text (str): The button's text
        on_click (Callable[[None], None]): The function to call when the button is clicked

    Returns:
        int: The ID of the button which was just created
    """
    # Construct the font now to save time rendering
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)

    buttons.append(rectangle, text_colour, background_colour, font, text, on_click, True)
    return len(buttons)-1

def modify_button(button_id: int,
                  rectangle: tuple[int, int, int, int] = None,
                  text_colour: int = None,
                  background_colour: int = None,
                  font_size: int = None,
                  text: str = None,
                  on_click: Callable[[None], None] = None) -> None:
    """Modifies a button given its ID
    
    Args:
        button_id (int): The ID of the button to modify
        rectangle (tuple[int, int, int, int]): The new rectangle, leave blank to not modify
        text_colour (int): The new text colour; leave blank to not modify
        background_colour (int): The new background colour; leave blank to not modify
        font_size (int): The new font size; leave blank to not modify
        text (str): The new text; leave blank to not modify
        on_click (Callable[[None], None]): The new function to call on click; leave blank to not modify
    """
    if rectangle is not None:
        buttons[button_id][0] = rectangle
    if text_colour is not None:
        buttons[button_id][1] = text_colour
    if background_colour is not None:
        buttons[button_id][2] = background_colour
    if font_size is not None:
        buttons[button_id][3] = pygame.font.Font(pygame.font.get_default_font(), font_size)
    if text is not None:
        buttons[button_id][4] = text
    if on_click is not None:
        buttons[button_id][5] = on_click

def set_button_status(button_id: int, active: bool) -> None:
    """Sets the status of a single button
    
    Args:
        button_id (int): The ID of the button to modify
        active (bool): True to make the button active, False to deactivate it
    """
    buttons[button_id][6] = active

def draw_buttons() -> None:
    """Draws the active buttons"""
    for button in buttons:
        # Get all of the different properties of the button
        rectangle, text_colour, background_colour, font, text, on_click, active = button

        if active:
            # Draw the button background
            pygame.draw.rect(assets.screen, background_colour, rectangle)

            # Render the button text
            text_surface = font.render(text, True, text_colour)
            text_rectangle = text_surface.get_rect()
            text_rectangle.center = (int(rectangle[0] + rectangle[2] / 2), int(rectangle[1] + rectangle[3] / 2))
            assets.screen.blit(text_surface, text_rectangle)


def handle_click(click_pos: tuple[int, int]) -> None:
    """Handles a pygame click and calls any button the user clicked on
    
    Args:
        click_pos (tuple[int, int]): The position of the click on the screen
    """
    for button in buttons:
        # Check if the button is active
        if button[6]:
            # Check if the click was on the button
            if button[0][0] <= click_pos[0] <= button[0][0] + button[0][2] and \
               button[0][1] <= click_pos[1] <= button[0][1] + button[0][3]:
                # Call the function associated with the button
                if button[5] is not None:
                    button[5]()