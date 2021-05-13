# Asteroids
A asteroids remake in python

This game is finished with a fully working and trainable AI.

# Setup

Due to unknown issues regarding the method of running through the command prompt we will be using the anaconda navigator method instead. This of course requires that you have Anaconda installed. you can acquire this here... https://www.anaconda.com/products/individual

> Anaconda Navigator

Firstly open anaconda navitator and navigate to environment section. press import and import .yml. Then after this navigate to the folder and import the Asteroids.yml file. After this anaconda will begin to add the environment. This process will take some time. After this however the environment will change, if not please click on the asteroids environemtn that has just been imported. 

Next go back to the home page and run Spyder. after drag and drop the gui.py into spyder. after this you will be able to run the application by clicking the green arrow.

Beware the kernel has a tendency to restart after every run. I believe this is an issue to do with pygame moreso than my actual code.

# The basics of how to play
> Settings

The game has a variety of options. 
The first set of options are the colours of asteroids aswell as the player ships. this is to help those with potential colour blindness, or perhaps those with a preference customise their game to suit them.

There is also a debug option, which will show a variety of information such as player ship hitbox, closeness from asteroids. and vision lines from the AI drone. Be warned this will cause a decrease in performance towards the late stages of the game.

Next you are given the option between training and playing. Training trains the AI in a simulation where the only ship in the game is itself. It will learn after every death and update the rules it uses.

Whereas play involves you shooting asteroids with the help of a AI companion.

> Training

One of the options presented to the user is the train button. clicking this will cause the AI to play the game repeatedly, learning after each iteration. This process takes time, after all there are over 4000 rules to work with. However after closing the window the AI is automatically updated and ready to be used in play.

> The controls

This game uses the arrow keys to move.

- up: Move the ship forward
- left and right: Turns the ship left and right respectivly.
- down: Slows the ship down
- F: Summon AI drone (Limited supply of 2 drones per game)
- Space: Shoot a shot
