import math
import constants


class Bullet:
    def __init__(self,speed,x,y,angle,w,length=5):
        self.length = length
        self.speed = speed
        self.w = w
        self.x = x
        self.y = y
        self.angle = angle
        self.coords = None 
        self.physical_bullet = None
        self.needs_deleted = False


    def delete(self):
        self.w.delete(self.physical_bullet)


    def redraw(self):
        self.calculate_points()
        self.w.coords(self.physical_bullet,self.coords)


    def create_bullets(self):
        self.calculate_points()
        self.physical_bullet = self.w.create_line(self.coords,width=3)


    def calculate_points(self):
        opposite_leg = math.sin(math.radians(self.angle)) * self.length
        adjacent_leg = math.cos(math.radians(self.angle)) * self.length
        x_1 = (self.x + opposite_leg)
        y_1 = (self.y + adjacent_leg)
        x_2 = (self.x - opposite_leg)
        y_2 = (self.y - adjacent_leg)
        self.coords = ((x_1,y_1,x_2,y_2))
        return self.coords

    
    def update_bullet(self):
        opposite_leg = math.sin(math.radians(self.angle)) * self.length
        adjacent_leg = math.cos(math.radians(self.angle)) * self.length
        self.x += opposite_leg * self.speed
        self.y += adjacent_leg * self.speed
        self.redraw()
        if self.x > constants.SCREEN_WIDTH or self.x < 0 or self.y > constants.SCREEN_HEIGHT or self.y < 0:
            self.needs_deleted = True