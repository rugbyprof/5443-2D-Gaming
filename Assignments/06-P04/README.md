## Adventure - Collaborative Level Game
#### Due: 04-24-2023 (Monday @ 2:30 p.m.)

### Group Programming

Between 1 and 3 individuals can collaborate. However, the more individuals in the group means the more material / levels your game must contain. I will decide on a more specific metric soon, But I wanted to warn you that a 3 person group must turn in a noticeably larger and more refined game than a single individual.


### Overview

If the multiplayer backend aka: rabbitmq proves to be usable, which I think it is, then we will create a slower paced adventure style game in which players will be loaded onto a game level that has an "adventure" type theme. I've been having some trouble re-learning "tiled", but that doesn't mean we can't use a tiled based layout for our game. Even something as rudimentary as this can work:

```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
x000xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxx0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx00000000000000000xxxxxxxxxx
xxx0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx0xxxxxxxxxxxxxxx0xxxxxxxxxx
xxx0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx0xxxxxxxxxxxxxxx0xxxxxxxxxx
xxx0000000000000000000000000000000000xxxxxxxxxxxxxxx0xxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx0xxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx0xxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx00000000000
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Where the x's are tiles with a brick pattern and the 0's are a tile
with a black color so it looks like a "path". 

Typically we use tiles of size: 16x16 / 24x24 / 32x32. The above snippet is 10 rows and 64 columns, so the overall size would be (10 * tileSize) x (64 * tileSize).

Your game should have a minimum of three levels if you're working alone, and 3 * number of group members / 1.5 if you are in a group (6 levels for a group of 3 and 4 levels for a group of 2). \

Each level should be very different from the previous level, if not in layout, then in the objects / monsters / traps that exist within the level. There should be a minimum of 5 different "things" on each level, whether it be an object to collect, a trap, a monster, etc. At least one of each category should be included. The categories are:

- Monsters (attacks player in some basic way)
- Objects (collectable kind for powerups or points)
- Traps (injure or kill a player)
- Doors / Portals (moves player between levels OR transports them to some location)


### Levels

Your game will have multiple levels. A level is an entirely different map or tile layout with its own secrets or specific game-play. Your levels can be whatever you want as long as you incorporate a limited view showing only the immediate area around your player, and not the whole game level. Its ok to have each level be of the same style as the previous, but make it unique. This means, if you have three maze levels, each maze should be different. 

What should you incorporate in your levels? Whatever you want, but you must incorporate things similar to the following ideas: 

- Maze 
- Path's or cave system
- Platforms

Each of these can have object to be collected:

- Coins
- Potions
- Health
- Power-ups 

Or bad things to be avoided:

- Traps
  - Arrows
  - Explosions
  - Bullets 
  - Missiles
  - etc.
- Monsters that attack

### Camera View

Your game world will have its own size. Each level should be similar in size, if not exact since we don't want to mess with a dynamic window size. Having said this, your player should only see a portion of the game world, more specifically a window showing the player their immediate area. If your game world is `((tileSize * 500) , (tileSize * 500))` for example, then the players view could be `tileSize * 50` or something similar. 

You can decide how to handle game world borders as you see fit, but it must make sense. For example if you are in a maze or cave system, then wrapping around the world and showing up inside a wall or rock doesn't make sense. So, either transform the player to a navigable point on the opposite side of the level, or stop them from leaving the level at all. 


### Player Corroboration

Some type of player corroboration should be incorporated into game play in which more than one player must be included in an effort to get past an obsticle. For example: 

- Two players shoot a monster within some threshold to kill it.
- Multiple players must interact (stand on a tiled, push against a tile, etc.) with the game world to unlock a door, or portal.
- Multiple players must be present, or within some distance from one another to trigger an event. 

### Players

Each player should have a unique sprite that has a basic set of animation frames. Player sprites don't have to have attack animations, but should show some rudimentary actions when moving. 

Players also need a power bar to show health. Their health can be upgraded or healed based on objects found. 

Each player should have some attack:
    - Punching
    - Kicking
    - Sword 
    - Knife
    - Axe
    - Arrows
    - Gun
    - Etc.

something that lets them kill things. 

Each player should be somewhat different incorporating at least 3 different classes. This means different sprites, and different attacks. 



## More or less as we discuss in class.....


#### Example tile loader in Python: 
https://qq.readthedocs.io/en/latest/






