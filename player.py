import constants
import math


class Player:
    def __init__(self, x,y,angle,radius,w):
        self.w = w
        self.x = x
        self.y = y
        self.movecounter = 0
        self.speed = 0
        self.max_speed = 15
        self.angle = angle
        self.travelling_angle = angle
        self.radius = radius
        self.coords1 = ()
        self.coords2 = ()
        self.coords3 = ()
        self.coords4 = ()
        self.pointx = ()
        self.pointy = ()
        self.square_1 = None
        self.square_2 = None
        self.square_3 = None
        self.square_4 = None
        self.move_forward = False
        self.move_right = False
        self.move_left = False
        

    def calculate_corners(self):
        angle = self.angle + 45
        opposite_leg = math.sin(math.radians(angle)) * self.radius
        adjacent_leg = math.cos(math.radians(angle)) * self.radius
        point_1x = (self.x + opposite_leg) 
        point_1y = (self.y + adjacent_leg)
        point_2x = (self.x + adjacent_leg) 
        point_2y = (self.y - opposite_leg)
        point_3x = (self.x - opposite_leg) 
        point_3y = (self.y - adjacent_leg)
        point_4x = (self.x - adjacent_leg) 
        point_4y = (self.y + opposite_leg)
        self.pointx = (point_1x,point_2x,point_3x,point_4x)
        self.pointy = (point_1y,point_2y,point_3y,point_4y)
        self.coords1 = (point_1x,point_1y,point_2x,point_2y)
        self.coords2 = (point_2x,point_2y,point_3x,point_3y)
        self.coords3 = (point_3x,point_3y,point_4x,point_4y)
        self.coords4 = (point_4x,point_4y,point_1x,point_1y)
        return self.coords1,self.coords2,self.coords3,self.coords4
        

    def do_rotate_right(self):
        if not self.move_right:
            return
        self.angle %= 360
        self.angle -= 6


    def do_rotate_left(self):
        if not self.move_left:
            return
        self.angle %= 360
        self.angle += 6
    
 
    def do_move_foward(self):
        # if not self.move_forward:
        #     self.speed = max(self.speed - 0.4, 0)
        #     if self.speed <= 0:
        #         return
        # else:
        #     self.speed = min(self.speed + 0.4, self.max_speed)
        # Draw a triangle if we are trying to move
        if self.move_forward:
            default_new_x = self.x + math.cos(math.radians(self.travelling_angle)) * self.speed
            default_new_y = self.y - math.sin(math.radians(self.travelling_angle)) * self.speed
            changing_new_x = default_new_x + math.cos(math.radians(self.angle)) * constants.ACCELERATION
            changing_new_y = default_new_y - math.sin(math.radians(self.angle)) * constants.ACCELERATION
            # Calculate angle to new points
            delta_x = changing_new_x - self.x
            delta_y = self.y - changing_new_y
            self.travelling_angle = abs(math.degrees(math.atan2(delta_y, delta_x) * -1) - 360) % 360
            distance_calculation = math.sqrt(delta_x ** 2 + delta_y ** 2)
            self.speed = min(self.max_speed, distance_calculation)

        self.x += math.cos(math.radians(self.travelling_angle)) * self.speed
        self.y -= math.sin(math.radians(self.travelling_angle)) * self.speed
        if self.x > constants.SCREEN_WIDTH:
            self.x = 5
        if self.x < 0:
            self.x = constants.SCREEN_WIDTH - 5
        if self.y > constants.SCREEN_HEIGHT:
            self.y = 5
        if self.y < 0:
            self.y = constants.SCREEN_HEIGHT - 5


    def update_player(self):
        self.do_move_foward()
        self.do_rotate_right()
        self.do_rotate_left()
        self.calculate_corners()
        self.w.coords(self.square_1,self.coords1)
        self.w.coords(self.square_2,self.coords2)
        self.w.coords(self.square_3,self.coords3)
        self.w.coords(self.square_4,self.coords4)


    def create_player(self):
        self.calculate_corners()
        self.w.delete(self.square_1)
        self.w.delete(self.square_2)
        self.w.delete(self.square_3)
        self.w.delete(self.square_4)
        self.square_1 = self.w.create_line(self.coords1,fill='red')
        self.square_2 = self.w.create_line(self.coords2)
        self.square_3 = self.w.create_line(self.coords3)
        self.square_4 = self.w.create_line(self.coords4)