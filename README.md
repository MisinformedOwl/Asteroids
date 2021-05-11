# Asteroids
A asteroids remake in python

This game is finished with a fully working and trainable AI.

# How to play

> Anaconda Navigator

Firstly open anaconda navitator and navigate to environment section. Given that you have installed the asteroids environment  you must activate the asteroids environment by clicking on it. after a few seconds/minutes the environment will change, go back to the home page and download Spyder. after this is downloaded open spyder and drag and drop the gui.py into spyder. after this you will be able to run the application by clicking the green arrow.

Beware the kernel has a tendency to restart after every run. I believe this is an issue to do with pygame moreso than my actual code.

# The basics of how to play
> Settings

The game has a variety of options. 
The first set of options are the colours of asteroids aswell as the player ships. this is to help those with potential colour blindness, or perhaps those with a preference customise their game to suit them.

There is also a debug option, which will show a variety of information such as player ship hitbox, closeness from asteroids. and vision lines from the AI drone. Be warned this will cause a decrease in performance towards the late stages of the game.

Next you are given the option between training and playing. Training trains the AI in a simulation where the only ship in the game is itself. It will learn after every death and update the rules it uses.
Whereas play involves you shooitng asteroids with the help of a AI companion.

> The controls

This game uses the arrow keys to move.

- up: Move the ship forward
- left and right: Turns the ship left and right respectivly.
- down: Slows the ship down
- F: Summon AI drone
- Space: Shoot a shot
