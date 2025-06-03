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

### The event handler

`handlers.handle_events` handles all pygame events. It chooses what to do based on the game's current state (see the section on the state handler)

### The state handler (state_handler.py)

The state handler handles most of the code. It has a state variable which controls what part of the game is currently running. It also handles which objects are active (objects are discussed later)

The majority of the game loop is run with `state_handler.handle`. It calls on a series of subhandlers to do its work for it

### Objects

This whole concept was based on code I've previously written in C for SDL. The idea is that there are different types of game objects, each with their own respective handler, and they should be as easy to create and modify as possible.

The 3 different object's I've written code for here are buttons (input_handler.py), text (text_handler.py), and sprites (sprite_handler.py).

Each object is assigned an ID and with that ID, the user can modify the object. Each handler also handles drawing and processing of objects. For example, in input_handler.py, the handle_click function is called whenever a click is processed and checks if the user clicked on a valid button.

The reason I've done this is to increase the modularity of my program. I've sacraficed a couple of hours to allow me to create new pieces in seconds. With this method, creating new UI elements takes literally a single minute, processing and all. 