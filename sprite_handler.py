# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

from collections.abc import Callable
import pygame
import constants
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
                    image_path: str | list[str],
                    transparent: bool,
                    on_collision: Callable[[None], None]) -> int:
    """Registers a new sprite with the sprite handler
    
    Args:
        sprite_rectangle (tuple[float, float, float, float, str | None]): The sprite's rectangle
        image_path (str | list[str]): The path to the sprite's image or list of images in its animation
        transparent (bool): Whether the sprite's image contains transparency. If it is an animation, it must be consistant
        on_collision (Callable[[None], None]): The function to call on collision with the player
        
    Returns:
        int: The ID of the new sprite
    """
    # Get the true rectangle
    true_rectangle = rectangle.get_rectangle(sprite_rectangle)

    # Preconstruct the sprite's image to save time later
    if isinstance(image_path, list):
        if transparent:
            sprite_image = [pygame.transform.scale(pygame.image.load(path).convert_alpha(),
                                                  (true_rectangle[2], true_rectangle[3]))
                            for path in image_path]
        else:
            sprite_image = [pygame.transform.scale(pygame.image.load(path).convert(),
                                                  (true_rectangle[2], true_rectangle[3]))
                            for path in image_path]
        frame_number = 0
    else:
        frame_number = None
        if transparent:
            sprite_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),
                                                 (true_rectangle[2], true_rectangle[3]))
        else:
            sprite_image = pygame.transform.scale(pygame.image.load(image_path).convert(),
                                                 (true_rectangle[2], true_rectangle[3]))

    _sprites.append([true_rectangle, image_path, transparent, sprite_image, on_collision, False, frame_number])
    return len(_sprites)-1

def modify_sprite(sprite_id: int,
                  sprite_rectangle: tuple[float, float, float, float, str | None] = None,
                  image_path: str | list[str] = None,
                  transparent: bool = None,
                  on_collision: Callable[[None], None] = False) -> None:
    """Modifies a sprite based on its ID
    
    Args:
        sprite_id (int): The ID of the sprite to modify
        sprite_rectangle (tuple[float, float, float, float, str | None]): The new rectangle for the sprite;
                                                                          leave blank to not modify
        image_path (str | list[str]): The path of the sprite's image or list of images; leave blank to not modify
        transparent (bool): True if the sprite's image is transparent, False if not. Needs to be set if image_path or rectangle is not None
        on_collision (Callable[[None], None]): The function to call upon player collision with the sprite; leave blank to not modify
    """
    if sprite_rectangle is not None:
        true_rectangle = rectangle.get_rectangle(sprite_rectangle)
        
        # Don't waste compute time
        if image_path is None:
            if isinstance(image_path, list):
                if _sprites[sprite_id][2]:
                    sprite_image = [pygame.transform.scale(pygame.image.load(path).convert_alpha(),
                                                          (true_rectangle[2], true_rectangle[3]))
                                    for path in image_path]
                else:
                    sprite_image = [pygame.transform.scale(pygame.image.load(path).convert_alpha(),
                                                          (true_rectangle[2], true_rectangle[3]))
                                    for path in image_path]
                _sprites[sprite_id][6] = 0 # Reset the frame count
            else:
                if _sprites[sprite_id][2]:
                    sprite_image = pygame.transform.scale(pygame.image.load(_sprites[sprite_id][1]).convert_alpha(),
                                                         (true_rectangle[2], true_rectangle[3]))
                else:
                    sprite_image = pygame.transform.scale(pygame.image.load(_sprites[sprite_id][1]).convert(),
                                                         (true_rectangle[2], true_rectangle[3]))
            _sprites[sprite_id][3] = sprite_image
        
        _sprites[sprite_id][0] = true_rectangle
    if image_path is not None:
        if transparent is None:
            raise ValueError(f"If image_path is set, transparent must be as well")
        _sprites[sprite_id][1] = image_path
        
        if isinstance(image_path, list):
            if transparent:
                sprite_image = [pygame.transform.scale(pygame.image.load(path).convert_alpha(),
                                                      (true_rectangle[2], true_rectangle[3]))
                                for path in image_path]
            else:
                sprite_image = [pygame.transform.scale(pygame.image.load(path).convert(),
                                                      (true_rectangle[2], true_rectangle[3]))
                                for path in image_path]
            _sprites[sprite_id][6] = 0 # Reset the frame count
        else:
            if transparent:
                _sprites[sprite_id][3] = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),
                                                                (_sprites[sprite_id][0][2], _sprites[sprite_id][0][3]))
            else:
                _sprites[sprite_id][3] = pygame.transform.scale(pygame.image.load(image_path).convert(),
                                                                (_sprites[sprite_id][0][2], _sprites[sprite_id][0][3]))
    if on_collision is not False:
        _sprites[sprite_id][4] = on_collision

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

def set_sprite_position(sprite_id: int, position: tuple[float, float]) -> None:
    """Sets the specified sprite's position
    
    Args:
        sprite_id (int): The ID of the sprite to modify
        position (tuple[float, float]): The new position as x, y
    """
    _sprites[sprite_id][0] = (position[0],
                              position[1],
                              _sprites[sprite_id][0][2],
                              _sprites[sprite_id][0][3])

def set_sprite_status(sprite_id: int, active: bool) -> None:
    """Sets the status of a single sprite
    
    Args:
        sprite_id (int): The ID of the sprite to modify
        active (bool): True to make the sprite draw, False to make it not
    """
    _sprites[sprite_id][5] = active

def draw_sprites() -> None:
    """Draws all the active sprites"""
    for _, sprite in enumerate(_sprites):
        rectangle, image_path, transparent, image, on_collision, active, frame = tuple(sprite)
        if active:
            # Check if the image is a list; then process accordingly
            if isinstance(image, list):
                assets.screen.blit(image[int(frame / (constants.FPS_CAP/constants.ANIMATION_FPS))], rectangle)
                
                # Increment the frame counter if the game is not paused
                import state_handler # Needs to be done here for Python reasons
                if state_handler.current_state != state_handler.PAUSED:
                    _sprites[_][6] += 1
                    if _sprites[_][6] >= len(image) * (constants.FPS_CAP / constants.ANIMATION_FPS):
                        _sprites[_][6] = 0
            else:
                assets.screen.blit(image, rectangle)

def handle_collisions() -> None:
    """Handles all the collisions with the player"""
    global _drawn_this_frame
    for _, sprite in enumerate(_sprites):
        rectangle, image_path, transparent, surface, on_collision, active, frame = tuple(sprite)
        if active or _ in _drawn_this_frame:
            if assets.player_rectangle.colliderect(rectangle):
                if on_collision is not None: on_collision()
    _drawn_this_frame = []

def draw_specifically(sprite_id: int) -> None:
    """Draws the specified sprite whether it's active or not"""
    assets.screen.blit(_sprites[sprite_id][3], _sprites[sprite_id][0])
    _drawn_this_frame.append(sprite_id)