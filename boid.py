class Boid:
    
    def __init__(self):
        self.x = random(width)
        self.y = random(height)
        self.heading = random(2 * PI)
        self.velocity = 3
        self.angular_velocity = PI / 12
        self.color = random(255)
        self.theta = 0
  
    def __correct_heading(self):
        '''Keep heading within [0, 2PI).'''
        if self.heading < 0:
            self.heading += 2 * PI
        elif self.heading > 2 * PI:
            self.heading -= 2 * PI
            
    def __on_left(self, rel_x, rel_y):
        '''Is rel_x and rel_y to the left of us, relative to our heading?'''
        tangent = atan(rel_y / (rel_x + 0.000001))    
        rel_heading = tangent
        if rel_x > 0 and tangent < 0:
            # top right
            rel_heading = tangent + 2 * PI
        elif rel_x < 0:
            # top and bottom left
            rel_heading = tangent + PI
        theta = rel_heading - self.heading
        if theta < -PI:
            theta += 2 * PI
        if theta > PI:
            theta -= 2 * PI
        
        return theta < 0
 
    def separate(self, boids, separation):
        for b in boids:
            if b != self:
                rel_x = b.x - self.x
                rel_y = b.y - self.y
                distance = sqrt(sq(rel_x) + sq(rel_y))
                    
                if distance < separation:
                    urgency = ((separation - distance) / separation)
                    turn = self.angular_velocity * urgency
                    
                    if self.__on_left(rel_x, rel_y):
                        self.heading += turn
                    else:
                        self.heading -= turn
        self.__correct_heading()
        
    def align(self, boids, sight):
        flockmates = []
        for b in boids:
            if b != self:
                rel_x = b.x - self.x
                rel_y = b.y - self.y
                distance = sqrt(sq(rel_x) + sq(rel_y))
                if distance < sight:
                    flockmates.append(b)
        
        if len(flockmates) > 0:
            avg_heading = 0
            for f in flockmates:
                avg_heading += f.heading
            avg_heading /= len(flockmates)
        
            theta = avg_heading - self.heading
            if theta < -PI:
                theta += 2 * PI
            if theta > PI:
                theta -= 2 * PI
            if theta < 0:
                # to our left
                self.heading -= self.angular_velocity * 0.1
            else:
                # to our right
                self.heading += self.angular_velocity * 0.1
            
        self.__correct_heading()
        
    def cohere(self, boids, sight):
        flockmates = []
        for b in boids:
            if b != self:
                rel_x = b.x - self.x
                rel_y = b.y - self.y
                distance = sqrt(sq(rel_x) + sq(rel_y))
                if distance < sight:
                    flockmates.append(b)
        
        if len(flockmates) > 0:
            avg_x = 0
            avg_y = 0
            for f in flockmates:
                avg_x += f.x
                avg_y += f.y
            avg_x /= len(flockmates)
            avg_y /= len(flockmates)
        
            if self.__on_left(avg_x, avg_y):
                # to our left
                self.heading -= self.angular_velocity * 0.1
            else:
                # to our right
                self.heading += self.angular_velocity * 0.1
        
    def update(self, boids):
        noise = 0.1
        # self.heading += random(noise) - noise / 2
        self.__correct_heading()
        
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
