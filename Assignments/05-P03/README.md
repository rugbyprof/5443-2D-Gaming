## MultiPlayer Game - Space Battle
#### Due: 03-27-2023 (Monday @ 2:30 p.m.)

### Partner Programming

2 individuals can collaborate. No more. Don't ask. 

### Overview

The traditional asteroids game is a classic. Controlling the "ship" in the game was an innovative approach to moving a game object around in a vacuum. Since this will be a multi-player game, I don't want you to struggle with implementing ships in space, and so the asteroids code will be extremely helpful for us to implement our multiplayer version of this game. The code from [here](../../Resources/12-Asterioids/README.md) has an entire asteroids implementation. Removing the actual asteroids (or make them miniscule along with an extremely low occurance rate) would be helpful for this game. I want you to add multiple "ships" via the multi player class from [here](../../Lectures/04-MultiPlayer/ex_mul_02.py), along with a few more requirements (described below) dealing with gameplay. The big picture idea is many fighters in space, shooting at each other, where the winner is the ship with most kills in a set amount of time. 

### Minimum Requirements

Meeting these requirements will earn a max grade of B.

- 2 to N players playing at once where N can be some limit based on performance computer performance.
- Use a sprite spaceship that has obvious guns showing (or a pointy nose).
- Have a minimum of 10 different ships (I provide 6 already). I can lecture on resizing and or manipulating images for your game.
- When bullets objects are firedm they should visually leave from an "obvious" portion of the spaceship. This means the bullet should leave the sprite at a position that lines up with the nose of the ship, or a gun on the wings.
- Bullets striking another player does not kill the player, it reduces their health by 10%. 
- Ship health regenerates by 10% every 1 or 2 minutes of staying alive.
- Bullet sprite can be any shape or color.
- Ships movement determined by keyboard input where thrust is up arrow, and negative thrust is the down arrow.
- Score kept in one upper corner of the game. It can be just the score for the **local player**, where each local player see's their own score. Seeing scores for all players can be included for a better grade :)

### Additional Requirements

Meeting these requirements can boost your grade to an A.

- Scores for **each** player shown in an upper corner of the game. 
- Thrust for a ship can be stopped immediately by hitting a predefined key (making velocity = 0) but only a limited number of times per game. These can be earned, or given outright. 
- Stronger bullets can be earned after a certain acheivement (score, kills, time) where instead of 10% damage, they could be as strong as 25% or 50% damage. 
- Have game settings that allow for demonstration purposes. For example a preset score to allow localPlayer to earn stronger bullets very quickly. 
- You should plan ahead for your presentation and have shortcuts to show all aspects of your game if necessary.

### Bonus Features

Meeting these requirements will give you bragging rights.

- Showing scores in upper corner of all players, ordered by highest scores.
- Health "asteroids" that randomly appear and allow a ship to collide with to maximize health.
- Ship can upgrade after certain score that allow multiple bullets fired from ship. 
- Bullet strength degrades over distance. Normal damage is 10%, but after half the screen it starts to weaken. So a bullet less than half the screen is 10% damage, but weakens down from 10% at halfway to 1% on the edges of the screen. The bullet sprite also needs to change size and / or color the longer it travels as well to visually imply strength. 

## Deliverables

- Create a folder called P02 in your Assignments folder.
- Push all your code and assets into this folder.
- Prepare for a live presentation in class of your game with instructions to the class on how to download and connect to your specific game instance.




