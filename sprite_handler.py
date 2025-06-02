# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

from collections.abc import Callable
import pygame
import assets
import rectangle

# Sprite C typedef:
# Rectangle rectangle;
# const char* imagePath;
# SDL_Surface image;
# void (*onCollision)(void);
# int active

_sprites = []
_drawn_this_frame = []

def register_sprite(sprite_rectangle: tuple[float, float, float, float, str | None],
                    image_path: str,
                    transparent: bool,
                    on_collision: Callable[[None], None]) -> int:
    """Registers a new sprite with the sprite handler
    
    Args:
        sprite_rectangle (tuple[float, float, float, float, str | None]): The sprite's rectangle
        image_path (str): The path to the sprite's image
        transparent (bool): Whether the sprite's image contains transparency
        on_collision (Callable[[None], None]): The function to call on collision with the player
        
    Returns:
        int: The ID of the new sprite
    """
    # Get the true rectangle
    true_rectangle = rectangle.get_rectangle(sprite_rectangle)

    # Preconstruct the sprite's image to save time later
    if transparent:
        sprite_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),
                                              (true_rectangle[2], true_rectangle[3]))
    else:
        sprite_image = pygame.transform.scale(pygame.image.load(image_path).convert(),
                                              (true_rectangle[2], true_rectangle[3]))

    _sprites.append([true_rectangle, image_path, sprite_image, on_collision, False])
    return len(_sprites)-1

def modify_sprite(sprite_id: int,
                  sprite_rectangle: tuple[float, float, float, float, str | None] = None,
                  image_path: str = None,
                  transparent: bool = None,
                  on_collision: Callable[[None], None] = False) -> None:
    """Modifies a sprite based on its ID
    
    Args:
        sprite_id (int): The ID of the sprite to modify
        sprite_rectangle (tuple[float, float, float, float, str | None]): The new rectangle for the sprite;
                                                                          leave blank to not modify
        image_path (str): The path of the sprite's image; leave blank to not modify
        transparent (bool): True if the sprite's image is transparent, False if not. Needs to be set if image_path is not None
        on_collision (Callable[[None], None]): The function to call upon player collision with the sprite; leave blank to not modify
    """
    if sprite_rectangle is not None:
        true_rectangle = rectangle.get_rectangle(sprite_rectangle)
        
        # Don't waste compute time
        if image_path is None:
            sprite_image = pygame.transform.scale(pygame.image.load(_sprites[sprite_id][1]).convert_alpha(),
                                                  (true_rectangle[2], true_rectangle[3]))
            _sprites[sprite_id][2] = sprite_image
        
        _sprites[sprite_id][0] = true_rectangle
    if image_path is not None:
        if transparent is None:
            raise ValueError(f"If image_path is set, transparent must be as well")
        _sprites[sprite_id][1] = image_path
        if transparent:
            _sprites[sprite_id][2] = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),
                                                            (_sprites[sprite_id][0][2], _sprites[sprite_id][0][3]))
        else:
            _sprites[sprite_id][2] = pygame.transform.scale(pygame.image.load(image_path).convert(),
                                                            (_sprites[sprite_id][0][2], _sprites[sprite_id][0][3]))
    if on_collision is not False:
        _sprites[sprite_id][3] = on_collision

def move_sprite(sprite_id: int, move: tuple[float, float]) -> None:
    """Moves a sprite
    
    Args:
        sprite_id (int): The ID of the sprite to move
        move (tuple[float, float]): The move to make (x, y)
    """
    _sprites[sprite_id][0] = (_sprites[sprite_id][0][0] + move[0],
                              _sprites[sprite_id][0][1] + move[1],
                              _sprites[sprite_id][0][2],
                              _sprites[sprite_id][0][3])

def get_sprite_position(sprite_id: int) -> tuple[float, float]:
    """Gets the current position of the specified sprite
    
    Args:
        sprite_id (int): The ID of the sprite to query
    
    Returns:
        tuple[float, float]: The position of the sprite as x, y
    """
    return (_sprites[sprite_id][0][0], _sprites[sprite_id][0][1])

def set_sprite_status(sprite_id: int, active: bool) -> None:
    """Sets the status of a single sprite
    
    Args:
        sprite_id (int): The ID of the sprite to modify
        active (bool): True to make the sprite draw, False to make it not
    """
    _sprites[sprite_id][4] = active

def draw_sprites() -> None:
    """Draws all the active sprites"""
    for sprite in _sprites:
        rectangle, image_path, surface, on_collision, active = tuple(sprite)
        if active:
            assets.screen.blit(surface, rectangle)

def handle_collisions() -> None:
    """Handles all the collisions with the player"""
    global _drawn_this_frame
    for _, sprite in enumerate(_sprites):
        rectangle, image_path, surface, on_collision, active = tuple(sprite)
        if active or _ in _drawn_this_frame:
            if assets.player_rectangle.colliderect(rectangle):
                if on_collision is not None: on_collision()
    _drawn_this_frame = []

def draw_specifically(sprite_id: int) -> None:
    """Draws the specified sprite whether it's active or not"""
    assets.screen.blit(_sprites[sprite_id][2], _sprites[sprite_id][0])
    _drawn_this_frame.append(sprite_id)