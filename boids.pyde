'''
2D swarming
- Particles with constant forward motion try to swarm cursor and avoid conflict?
- ‘esc’’ to pause and adjust parameters
- Boid (bird-oid) Rules:
    - Cohesion: steer to move to average position of flockmates (cursor?)
    - https://www.youtube.com/watch?v=QbUPfMXXQIY
        - Noise?
    - Automatically color code flocks?
'''
from random import shuffle
from boid import Boid

# Parameters
boid_size = 20
enable_separation = True
separation = 30 # distance to try to keep from nearby boids
enable_alignment = True
sight = 50 # distance to track flockmates
enable_cohesion = False
cohesion_distance = 200
noise = True

boids = []
        
def setup():
    size(500, 500)
    colorMode(HSB)
    noStroke()

def draw():  
    fill(0)
    rect(0, 0, width, height)
    for b in boids:
        if enable_separation:
            b.separate(boids, separation)
        if enable_alignment:
            b.align(boids, sight)
        if enable_cohesion:
            b.cohere(boids, cohesion_distance)
        b.update(boids)
    
    for b in boids:
        fill(b.color, 255, 255)
        translate(b.x, b.y)
        rotate(b.heading)
        triangle(-boid_size//2, -boid_size//2, -boid_size//2, boid_size//2, boid_size, 0)
        resetMatrix()
    
def mouseClicked():
    global boids
    if mouseButton == LEFT:
        b = Boid()
        b.x = mouseX
        b.y = mouseY
        boids.append(b)
    elif mouseButton == RIGHT:
        boids += [Boid() for i in range(10)]
    else:
        boids = []
