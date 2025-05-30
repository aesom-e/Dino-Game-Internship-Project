# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import assets

# If you're reading this and are wondering about the C typedefs, I've already written exactly this system in C with SDL.
# I had everything here. Text, buttons, and geometry. I just have to rewrite this system in Python.
# The typedefs are modified for use with pygame. Without abstraction (that I can write myself), everything becomes messy

# Point C typedef:
# double x;
# double y;

# Colour C typedef:
# unsigned char red;
# unsigned char green;
# unsigned char blue;

# Text C typedef:
# Point center;
# Colour colour;
# unsigned fontSize;
# const char* text;
# int active;

_registered_texts = []

def register_text(text_center: tuple[float, float],
                  colour: tuple[int, int, int],
                  font_size: int,
                  text: str) -> int:
    """Registers a new text object
    
    Args:
        text_center (tuple[float, float]): The text's center.
        colour (tuple[int, int, int]): The text's colour
        font_size (int): The font size of the text
        text (str): The text itself
    
    Returns:
        int: The text object's ID
    """
    # Construct the font now to save time rendering
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)

    _registered_texts.append([text_center, colour, font, text, False])
    return len(_registered_texts)-1

def modify_text(text_id: int,
                text_center: tuple[float, FloatingPointError] = None,
                colour: tuple[int, int, int] = None,
                font_size: int = None,
                text: str = None) -> None:
    """Modifies a text object given its ID
    
    Args:
        text_id (int): The text object's ID
        text_center (tuple[float, float]): The text's center; leave blank to not modify
        colour (tuple[int, int, int]): The text's colour; leave blank to not modify
        font_size (int): The text's font size; leave blank to not modify
        text (str): The text itself; leave blank to not modify
    """
    if text_center is not None:
        _registered_texts[text_id][0] = text_center
    if colour is not None:
        _registered_texts[text_id][1] = colour
    if font_size is not None:
        _registered_texts[text_id][2] = pygame.font.Font(pygame.font.get_default_font(), font_size)
    if text is not None:
        _registered_texts[text_id][3] = text

def set_text_status(text_id: int, active: bool):
    """Sets the status of a single text object
    
    Args:
        text_id (int): The ID of the text to modify
        active (bool): True to make the text draw, False to make it not
    """
    _registered_texts[text_id][4] = active

def draw_text_objects() -> None:
    """Draws the registered text objects"""
    for text_object in _registered_texts:
        center, colour, font, text, active = tuple(text_object)
        if active:
            text_surface = font.render(text, True, colour)
            text_rectangle = text_surface.get_rect()
            text_rectangle.center = center
            assets.screen.blit(text_surface, text_rectangle)