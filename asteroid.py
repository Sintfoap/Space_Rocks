import constants
import math


class Asteroid:
    def __init__(self,x,y,direction,radius,w):
        self.speed = 0
        self.coords = None
        self.w = w
        self.x = x
        self.y = y
        self.direction = direction
        self.radius = radius
        self.physical_asteroid = None
        self.calculate_speed()


    def create_asteroids(self):
        self.calculate_points()
        self.physical_asteroid = self.w.create_oval(self.coords)
        return self.physical_asteroid
    

    def calculate_points(self):
        x_1 = self.x + self.radius
        y_1 = self.y + self.radius
        x_2 = self.x - self.radius
        y_2 = self.y - self.radius
        self.coords = (x_1,y_1,x_2,y_2)
        return self.coords
    

    def calculate_speed(self):
        #scaling speed to size of asteroid
        if self.radius == constants.LITTLE_ASTEROID_SIZE:
            self.speed = 6
        if self.radius == constants.MEDIUM_ASTEROID_SIZE:
            self.speed = 4
        if self.radius == constants.LARGE_ASTEROID_SIZE:
            self.speed = 3


    def update_asteroid(self):
        self.x +=  math.cos(math.radians(self.direction)) * self.speed
        self.y -=  math.sin(math.radians(self.direction)) * self.speed
        if self.x > constants.SCREEN_WIDTH:
            self.x = 5
        if self.x < 0:
            self.x = constants.SCREEN_WIDTH - 5
        if self.y > constants.SCREEN_HEIGHT:
            self.y = 5
        if self.y < 0:
            self.y = constants.SCREEN_HEIGHT - 5
        self.calculate_points()
        self.w.delete(self.physical_asteroid)
        self.physical_asteroid = self.w.create_oval(self.coords)
        return self.physical_asteroid