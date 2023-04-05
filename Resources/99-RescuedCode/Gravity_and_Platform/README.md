## P02 - Part 1


Project overview [here](../README.md)

## Step 1

- I downloaded `dude.png` and will use him in my demonstration.
- I used "Spriter" (patent pending) to split his sheet into individual frames of 80x105
- He moves up down left and right

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/dude.png" width="200">



## Step 2

- Created a basic PyGame instance that is not as vanilla as I wanted but hey, I'm on 4 hours sleep in 60 hours! But who's counting. 

### Map Loading

### Gravity

All gravity is ... make the `y` direction always increase so you go down. When your player rectangle collides with something "solid" (as we define it),
then you turn gravity ... off (sounds wrong) which really means stop increasing your `y` coordinate. The tricky part is knowing when to turn it on and 
off, especially if we use some of my classes that "help" :) with animations and such. 

```python
def gravity(self):
    self.y += self.gravity_level
```

Jumping is a little more involved, but not too bad. 

### Jumping

[I found this method here:](https://www.geeksforgeeks.org/python-making-an-object-jump-in-pygame/)

I changed it up, organization wise and made it a function, but it works nice and you can configure it.

```python

# Pretend were in a class Player

self.v = 5              # Force
self.m = 1              # Mass
self.jumping = False    # Not yet!

## When space key is hit, set self.jumping to true
## Call jump from update instead of move if jumping == True


def jump(self):

    if self.jumping: 
        # calculate force (F). F = 1 / 2 * mass * velocity ^ 2. 
        F =(1/2) * self.m * (self.v**2) 
      
        # change in the y co-ordinate 
        self.rect.centery -= F 
        
        # decreasing velocity while going up and become negative while coming down 
        self.v = self.v-1
        
        # object reached its maximum height 
        if self.v<0: 
            
            # negative sign is added to counter negative velocity 
            self.m =-1

        # objected reaches its original state 
        if self.v == -6: 

            # making isjump equal to false  
            self.jumping = False

    
            # setting original values to v and m 
            self.v = 5
            self.m = 1
```

