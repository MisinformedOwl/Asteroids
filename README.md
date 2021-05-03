# Asteroids
A asteroids remake in python

This game is finished with a fully working and trainable AI.

# How to play

> the .py file

For this i used anaconda. So the first requirement is to have anaconda installed.
Step 2 is to import Asteroids.yml into the anaconda navigator in the environments tab.

Once these are available you can play it by launching the anaconda command prompt and navigating to the folder location type in...

```
  python gui.py
```

# The basics of how to play
> Settings

The game has a variety of options. 
The first set of options are the colours of asteroids aswell as the player ships. this is to help those with potential colour blindness, or perhaps those with a preference customise their game to suit them.

There is also a debug option, which will show a variety of information such as player ship hitbox, closeness from asteroids. and vision lines from the AI drone. Be warned this will cause a decrease in performance towards the late stages of the game.

Next you are given the option between training and playing. Training trains the AI in a simulation where the only ship in the game is itself. It will learn after every death and update the rules it uses.
Whereas play involves you shooitng asteroids with the help of a AI companion.

> The controls

This game uses the typical WASD settings to move.

- W: Move the ship forward
- A and D: Turns the ship left and right respectivly.
- S: Quickly grinds the ship to a halt.
- F: Summon AI drone
- Space: Shoot a shot
