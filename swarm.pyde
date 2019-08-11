'''
2D swarming
- Particles with constant forward motion try to swarm cursor and avoid conflict?
- ‘esc’’ to pause and adjust parameters
- Boid (bird-oid) Rules:
    - Separation: distance from flockmates
    - Alignment: average heading of flockmates
    - Cohesion: steer to move to average position of flockmates (cursor?)
    - https://www.youtube.com/watch?v=QbUPfMXXQIY
        - Noise?
    - Automatically color code flocks?
'''
# Parameters
boid_size = 20
enable_separation = True
separation = 500 # distance to try to keep from nearby boids
enable_alignment = True
sight = 300 # distance to track flockmates
sign = 1

class Boid:
    
    def __init__(self):
        self.x = random(width)
        self.y = random(height)
        global sign
        if sign == 1:
            self.heading = 0
            sign = -1
        else:
            self.heading = PI
            sign = 1
        #self.heading = random(2 * PI)
        self.velocity = 0.5
        self.angular_velocity = PI / 12
        self.color = 50 # random(255)
        self.theta = 0
        
    def update(self, boids):
        flockmates = []
        for b in boids:
            if b != self:
                distance = sqrt(sq(self.x - b.x) + sq(self.y - b.y))
                if distance < sight:
                    flockmates.append(b)
                if enable_separation and distance < separation:
                    urgency = ((separation - distance) / separation)**3
                    turn = self.angular_velocity * urgency
                
                    # add a negligible value to avoid the occasional divide by 0 error
                    rel_x = (b.x - self.x) + 0.00001 
                    rel_y = b.y - self.y
                    theta1 = atan(rel_y / rel_x) # angle wrt x-axis
                    theta2 = theta1 + PI
                    # that gives us +theta in quadrants 2 and 4
                    # and -theta in quadrants 1 and 3
                    # now we adjust so theta is in the range [0, 2*PI)
                    if rel_x > 0 and rel_y < 0:
                        # quadrant 1 (positive rel_x, negative rel_y)
                        theta += 2*PI
                    elif rel_x < 0 and rel_y < 0:
                        # quadrant 2 (negative rel_x and rel_y)
                        theta += PI
                    elif rel_x > 0 and rel_y < 0:
                        # quadrant 3 (negative rel_x, positive rel_y)
                        theta += PI
                    # quadrant 4 (positive rel_x and rel_y) has correct theta
                    
                    # now we get the angle from our heading to the other boid
                    theta -= self.heading
                        
                    if theta < 0:
                        # other boid is on our left
                        self.heading += turn
                    else:
                        # other boid is on our right
                        self.heading -= turn
                    
        # Keep heading within [0, 2PI)
        if self.heading < 0:
            self.heading += 2 * PI
        elif self.heading > 2 * PI:
            self.heading -= 2 * PI
        self.x += self.velocity * cos(self.heading)
        self.y += self.velocity * sin(self.heading)
        
        if self.x < 0:
            self.x = width
        if self.x > width:
            self.x = 0
        if self.y < 0:
            self.y = height
        if self.y > height:
            self.y = 0

boids = []
        
def setup():
    size(500, 500)
    colorMode(HSB)
    noStroke()

def draw():    
    fill(0)
    rect(0, 0, width, height)
    for b in boids:
        b.update(boids)
    i = 0
    for b in boids:
        fill(b.color, 255, 255)
        translate(b.x, b.y)
        rotate(b.heading)
        triangle(-boid_size//2, -boid_size//2, -boid_size//2, boid_size//2, boid_size, 0)
        resetMatrix()
        
        translate(50 + i * 100, 50)
        fill(255)
        circle(0, 0, 100)
        rotate(b.heading + b.theta - PI/2)
        fill(0, 255, 255)
        rect(0, 0, 50, 5)
        rotate(-(b.heading + b.theta - PI/2))
        fill(0)
        text(str(b.theta), 0, 0)
        i += 1
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
