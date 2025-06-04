# Protection against running this file on its own
if __name__ == "__main__":
    raise RuntimeError(f"The {__file__.split('\\')[-1][:-3]} module should not be run on its own. Please run main.py instead")

import pygame
import importlib

_sound_cache = []
music = importlib.import_module("music") # This allows me to write soud.music.<func>()

def play(sound_name: str) -> None:
    """Plays the specified sound
    
    Args:
        sound_name (str): The sound file to play
    """

    # First check if it's in the cache to avoid loading another sound
    for entry in _sound_cache:
        if entry[0] == sound_name:
            pygame.mixer.Sound.play(entry[1])
            return
    
    # Load the sound, play it, and add it to the cache
    sound = pygame.mixer.Sound("sounds/effects/" + sound_name)
    pygame.mixer.Sound.play(sound)
    _sound_cache.append((sound_name, sound))