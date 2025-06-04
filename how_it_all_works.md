# How it all works

## main.py

Registers the objects states with the object handler and runs the infinite loop.
Everything is outsorced so main can be as tight as possible

## init.py

This contains the initialization script. It is imported once at the top of main.
This was the best way I thought of in python to cleanly initialize.

It initializes the random seed and pygame's screen and clock

## The player

The player is a basic pair of a sprite and rectangle defined in `assets.py`.
It has its own function for updating its animation and movement (`assets.update_player_sprite` and `handlers.handle_player_movement` respectivly)

## The event handler

`handlers.handle_events` handles all pygame events. It chooses what to do based on the game's current state (see the section on the state handler)

## The state handler (state_handler.py)

The state handler handles most of the code. It has a state variable which controls what part of the game is currently running. It also handles which objects are active (objects are discussed later)

The majority of the game loop is run with `state_handler.handle`. It calls on a series of subhandlers to do its work for it

## Objects

This whole concept was based on code I've previously written in C for SDL. The idea is that there are different types of game objects, each with their own respective handler, and they should be as easy to create and modify as possible.

The 3 different object's I've written code for here are buttons (input_handler.py), text (text_handler.py), and sprites (sprite_handler.py).

Each object is assigned an ID and with that ID, the user can modify the object. Each handler also handles drawing and processing of objects. For example, in input_handler.py, the handle_click function is called whenever a click is processed and checks if the user clicked on a valid button.

The reason I've done this is to increase the modularity of my program. I've sacraficed a couple of hours to allow me to create new pieces in seconds. With this method, creating new UI elements takes literally a single minute, processing and all.

### Buttons

Buttons contain their rectangle (where they draw and the area the user can click on it), their hover colour (colour of the text on mouse hover), regular colour, background colour, font size, text, and pointer to a function to call when it's clicked.

### Text

Text pretty much just abstracts the drawing of strings to the screen. Nothing special about this

### Sprites

Sprites are almost the same as buttons, except they have images instead of text. They support animations though just at a constant frame rate defined in constants.py. They also contain a function that calls on collision with the player, not on click.


### Non-object parts of the code

Some parts of the game which are rendered aren't made as objects, whether for simplicity or because of grandfathering.

The player is the most important of these. It contains more specialty code than my sprite objects allow for and it wouldn't be practical to change the rest of the object code to handle those edge cases

The leaderboard entries are also non-objects. It would be a bigger challenge for me to do it the "easier" way with objects than to use pygame objects

The last thing that is just a base pygame pair of sprite and rectangle are the hearts. I figured that it would be more effort than it would be worth to create a dynamic object registration to account for changes in the max number of lives.