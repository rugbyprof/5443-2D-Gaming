## P01.3 - Project 1  Part 3 Helper Files


Remember to do a `diff` between consecutive files. 

- [sprites_001.py](P01.3/sprites_001.py)
  - Loading a sprite animation and displaying it.
- [sprites_002.py](P01.3/sprites_002.py)
  - Dealing with single instance sprite problem
- [sprites_003.py](P01.3/sprites_003.py)
  - Robust file org and class design can make life a little easier.
  - LoadSpriteImages loads multiple sprites and displays as long as a format is followed.
  - Doesn't have to be my format, create your own.
- [sprites_004.py](P01.3/sprites_004.py)
  - Moving a sprite around without animation
  - Choices on how to handle movement:
    - Rememeber previous movement and let them keep moving
    - Stop when keys aren't pressed
    - There are issues with both and its not as trivial as it sounds.
- [sprites_005.py](P01.3/sprites_005.py)
  - This adds a `choose_animation` method to the player class.
  - This allows the class to play specific animations based on direction of movement.
  - Loading animations is easy using the organizational methods I have employed.
    - Naming conventions
    - Json files that store sprite information.
    - Etc.
  - There are problems with this file with the way it chooses "actions" it will error.
  - It's fixed in 006 ... see if you can fix it.
- [sprites_006.py](P01.3/sprites_006.py)
  - Fix of 005
  - But still a problem. Only one sequence of the animation place and it dies.
  - Can you fix it?
- [sprites_007.py](P01.3/sprites_007.py)
  - Fix of 006
  - Adds explosion animation when screen clicked.
  - Explodes where mouse is clicked. Can you make it so it only explodes when player is clicked?
  - After lesson 11 and 12 you should be able to, but what about now?
- [sprites_008.py](P01.3/sprites_008.py)
  - Added a few more sprite sheets to the configuration
  - Just 
  - Added an endlife method to player with class variables to handle that event.