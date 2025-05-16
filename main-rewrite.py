# Note that this project is meant to be done in a single file. I'm sorry for this code
# I also can't use classes, so it makes everything more messy

# Imports
import pygame
import random
import time

# Constants
WINDOW_HEIGHT               = 400
WINDOW_WIDTH                = 800
WINDOW_TITLE                = "Dino Game"
FPS_CAP                     = 60
GROUND_Y                    = 300
WALK_ANIMATION_DELAY        = 6
JUMP_GRAVITY_START_SPEED    = 15         # The speed at which the player jumps
DEFAULT_FONT_SIZE           = 50
ITEM_RESPAWN_VARIANCE       = 100
PLAYER_SPAWN_LIVES          = 3
MAX_LIVES                   = 5
ITEM_SPEED_CAP              = 15
HEART_SIZE                  = 40
POWER_UP_SIZE               = 50
POWER_UP_CHANCE             = 300        # There is a 1/POWER_UP_CHANCE each frame for a powerup to spawn
ALIVE_BACKGROUND_COLOUR     = 0xA020F0   # The background colour when the player is alive
DEAD_BACKGROUND_COLOUR      = 0x000000   # The background colour when the player is dead
SCORE_TEXT_COLOUR           = 0x000000
GAME_OVER_TEXT_COLOUR       = 0xFFFFFFFF # I don't know why, but 0xFFFFFF results in it being cyan, not white
                                         # If this were an alpha issue, I'd think it'd happen to other colours

# Initialize pygame and set the random seed
random.seed(time.time())
pygame.init()
pygame.display.set_caption(WINDOW_TITLE)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock  = pygame.time.Clock()

# Constant assets
SKY_SURFACE              = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURFACE           = pygame.image.load("graphics/level/ground.png").convert()
HEART_SURFACE            = pygame.transform.scale(pygame.image.load("graphics/level/heart.png").convert_alpha(), (HEART_SIZE, HEART_SIZE))
GAME_FONT                = pygame.font.Font(pygame.font.get_default_font(), DEFAULT_FONT_SIZE)
GAME_OVER_TEXT           = GAME_FONT.render("Game Over!", True, GAME_OVER_TEXT_COLOUR)
GAME_OVER_TEXT_RECTANGLE = GAME_OVER_TEXT.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
POWER_UPS                = []

# Non-constant assets
score_surface    = None
score_rectangle  = None
player_surface   = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(bottomleft=(25, GROUND_Y))
egg_surface      = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rectangle    = egg_surface.get_rect(bottomleft=(WINDOW_WIDTH, GROUND_Y))

# State variables
player_y_speed     = 0
player_is_alive    = True
player_animation   = "walk_1"
player_walk_frames = 0
player_animations  = {"walk_1": pygame.image.load("graphics/player/player_walk_1.png").convert_alpha(),
                      "walk_2": pygame.image.load("graphics/player/player_walk_2.png").convert_alpha(),
                      "jump":   pygame.image.load("graphics/player/player_jump.png").convert_alpha()}
egg_animation      = "1"
egg_animations     = {"1": pygame.image.load("graphics/egg/egg_1.png").convert_alpha(),
                      "2": pygame.image.load("graphics/egg/egg_2.png").convert_alpha()}
egg_walk_frames    = 0
score              = 0
item_speed         = 5
double_jumped      = False # Because 0 is not "pythonic"
player_lives       = PLAYER_SPAWN_LIVES
current_power_up   = None
power_up_rectangle = None

# Helper functions
def can_jump() -> bool:
    """Checks if the player can jump
    
    Returns:
        bool: True if the player can jump, False if not
    """
    global player_rectangle, double_jumped
    if player_rectangle.bottom >= GROUND_Y:
        return True
    elif not double_jumped:
        return True
    return False


def die() -> None:
    """Handles resetting all state variables when the player dies"""
    global player_is_alive, score, item_speed, player_lives, PLAYER_SPAWN_LIVES
    player_is_alive = False
    score = 0
    item_speed = 5
    player_lives = PLAYER_SPAWN_LIVES

def update_player_sprite() -> None:
    """Updates the player's sprite. Called each frame"""
    # God I hate python
    global player_walk_frames, WALK_ANIMATION_DELAY, player_animations, \
           player_surface, player_animation, player_y_speed
    if not player_y_speed:
        player_animation = "walk_2"
    elif player_y_speed > 0:
        player_animation = "jump"
    
    # Switch the walk animation
    match player_animation:
        case "walk_1":
            player_walk_frames += 1
            if player_walk_frames == WALK_ANIMATION_DELAY:
                player_walk_frames = 0
                player_animation = "walk_2"
        case "walk_2":
            player_walk_frames += 1
            if player_walk_frames == WALK_ANIMATION_DELAY:
                player_walk_frames = 0
                player_animation = "walk_1"
    
    player_surface = player_animations[player_animation]

def update_egg_sprite() -> None:
    """Updates the egg's sprite. Called each frame"""
    global egg_animation, WALK_ANIMATION_DELAY, egg_surface, \
           egg_animations, egg_walk_frames
    
    match egg_animation:
        case "1":
            egg_walk_frames += 1
            if egg_walk_frames == WALK_ANIMATION_DELAY:
                egg_walk_frames = 0
                egg_animation = "2"
        case "2":
            egg_walk_frames += 1
            if egg_walk_frames == WALK_ANIMATION_DELAY:
                egg_walk_frames = 0
                egg_animation = "1"
    
    egg_surface = egg_animations[egg_animation]

def draw_hearts() -> None:
    """Draws the player's lives to the top left corner of the screen"""
    global HEART_SURFACE, player_lives, HEART_SIZE
    for _ in range(player_lives):
        heart_rectangle = (_*HEART_SIZE, 0)
        screen.blit(HEART_SURFACE, heart_rectangle)

# Power up functions and list
def power_up_extra_life() -> None:
    global player_lives
    if player_lives < MAX_LIVES:
        player_lives += 1

def power_up_god_mode() -> None:
    pass

def power_up_double_score() -> None:
    pass


power_ups = [(pygame.transform.scale(pygame.image.load("graphics/level/heart.png").convert_alpha(), (POWER_UP_SIZE, POWER_UP_SIZE)), power_up_extra_life),
             (pygame.transform.scale(pygame.image.load("graphics/powerups/god_mode.png").convert_alpha(), (POWER_UP_SIZE, POWER_UP_SIZE)), power_up_god_mode),
             (pygame.transform.scale(pygame.image.load("graphics/powerups/double_score.png").convert_alpha(), (POWER_UP_SIZE, POWER_UP_SIZE)), power_up_double_score)]

# Main loop (again, I'm sorry for this code)
while True:
    # Handle pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif player_is_alive:
            # Handle jumping
            # REWRITE THIS DOGSHIT
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN) and can_jump():
                if player_rectangle.bottom < GROUND_Y:
                    double_jumped = True
                player_y_speed = JUMP_GRAVITY_START_SPEED
        else:
            # Handle restarting the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_is_alive = True
                egg_rectangle.left = WINDOW_WIDTH
    
    # Handle the game itself
    if player_is_alive:
        # Adjust the score
        score += 1
        score_surface = GAME_FONT.render(str(score), True, SCORE_TEXT_COLOUR)
        score_rectangle = score_surface.get_rect(center=(WINDOW_WIDTH/2, 50))

        # Wipe the screen
        screen.fill(ALIVE_BACKGROUND_COLOUR)

        # Draw the constant-positioned assets to the screen
        screen.blit(SKY_SURFACE, (0, 0))
        screen.blit(GROUND_SURFACE, (0, GROUND_Y))
        screen.blit(score_surface, score_rectangle)
        draw_hearts()

        # Handle then draw the egg
        egg_rectangle.x -= item_speed
        if egg_rectangle.right <= 0:
            egg_rectangle.left = WINDOW_WIDTH - random.randint(0, ITEM_RESPAWN_VARIANCE)
            if item_speed < ITEM_SPEED_CAP:
                item_speed += 1 # Increase the egg speed each loop to make the game harder
        update_egg_sprite()
        screen.blit(egg_surface, egg_rectangle)

        # Handle then draw the player
        player_y_speed -= 1
        update_player_sprite()
        player_rectangle.y -= player_y_speed # y=0 is at the top
        if player_rectangle.bottom >= GROUND_Y:
            # Handle the player hitting the ground
            player_rectangle.bottom = GROUND_Y
            double_jumped = False
        screen.blit(player_surface, player_rectangle)

        # Handle then draw power ups
        if current_power_up is not None:
            power_up_rectangle.x -= item_speed
            if power_up_rectangle.right <= 0:
                current_power_up = None
                power_up_rectangle = None
            else:
                screen.blit(current_power_up[0], power_up_rectangle)
        else:
            # Roll for a power up
            if not random.randint(0, POWER_UP_CHANCE):
                current_power_up = random.choice(power_ups)
                
                # Make sure an extra life doesn't spawn when the player can't collect one
                if current_power_up == power_ups[0] and player_lives == MAX_LIVES:
                    current_power_up = power_ups[random.randint(1, len(power_ups)-1)]

                rectangle_position = (WINDOW_WIDTH - random.randint(0, ITEM_RESPAWN_VARIANCE), GROUND_Y)
                power_up_rectangle = current_power_up[0].get_rect(bottomleft=rectangle_position)
                
                # Ensure the egg won't collide with the rectangle
                if egg_rectangle.colliderect(power_up_rectangle):
                    current_power_up = None
                else:
                    screen.blit(current_power_up[0], power_up_rectangle)

        # Handle collisions
        if egg_rectangle.colliderect(player_rectangle):
            player_lives -= 1
            # Reset the egg position to avoid multiple collisions
            egg_rectangle.left = WINDOW_WIDTH - random.randint(0, ITEM_RESPAWN_VARIANCE)
            if not player_lives:
                die()
        if power_up_rectangle and power_up_rectangle.colliderect(player_rectangle):
            # Trigger the powerup then delete it
            current_power_up[1]()
            current_power_up = None
            power_up_rectangle = None
    else:
        # Draw the death screen
        screen.fill(DEAD_BACKGROUND_COLOUR)
        screen.blit(GAME_OVER_TEXT, GAME_OVER_TEXT_RECTANGLE)
    
    # Draw to the physical screen and enforce the FPS cap
    pygame.display.flip()
    clock.tick(FPS_CAP)