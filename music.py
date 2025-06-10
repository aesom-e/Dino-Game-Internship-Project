# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame

def set(music_name: str) -> None:
    """Sets the music to play
    
    Args:
        music_name (str): The name of the music file to play
    """
    pygame.mixer.music.load("sounds/music/" + music_name)
    pygame.mixer.music.play(-1)

def pause() -> None:
    """Pauses the music"""
    pygame.mixer.music.pause()

def play() -> None:
    """Unpauses the music"""
    pygame.mixer.music.unpause()