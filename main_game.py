from tkinter import *
from tkinter import messagebox, simpledialog
import random
import datetime
import time
import os
from asteroid import Asteroid
from bullet import Bullet
import constants
from player import Player
from timer import Timer





class Logistics: 
    def __init__(self,game):
        self.time_of_last_bullet = 0 # cooldown timer
        self.game = game
        

    def right_press(self,event):
        if not self.game.player.move_right:
            self.game.player.move_right = True
        

    def right_release(self,event):
        self.game.player.move_right = False
        

    def left_press(self,event):
        if not self.game.player.move_left:
            self.game.player.move_left = True


    def left_release(self,event):
        self.game.player.move_left = False


    def up_press(self,event):
        if not self.game.player.move_forward:
            self.game.player.move_forward = True


    def up_release(self,event):
        self.game.player.move_forward = False
        


    def space_press(self,event):
        # setting a cooldown on fireing bullets
        if self.time_of_last_bullet + 0.25 > time.time():
            return
        else:
            self.game.create_bullets()
            self.time_of_last_bullet = time.time()
            

class game_mechanics:
    def __init__(self,root,w,main_menu):
        self.root = root
        self.canvas = w
        constants.SCREEN_WIDTH = self.root.winfo_screenwidth()
        constants.SCREEN_HEIGHT = self.root.winfo_screenheight()
        self.main_menu = main_menu
        self.end_game = False
        self.level = 0
        self.level_text = None
        self.points = 0
        self.score = 0
        self.entry1 = ''
        self.name = ''
        self.grace = False
        self.max_highscores = 252
        self.asteroid_list = []
        self.bullet_list = []
        self.player = Player(random.randint(0,constants.SCREEN_WIDTH),random.randint(0,constants.SCREEN_HEIGHT),0,10,w)    
        self.player.create_player()
        self.log = Logistics(self)
        self.timer = Timer(self)
        self.timer.update_timer()
        self.root.bind('<Right>', self.log.right_press)
        self.root.bind('<KeyRelease-Right>', self.log.right_release)
        self.root.bind('<Left>', self.log.left_press)
        self.root.bind('<KeyRelease-Left>', self.log.left_release)
        self.root.bind('<Up>', self.log.up_press)
        self.root.bind('<KeyRelease-Up>', self.log.up_release)
        self.root.bind('<space>', self.log.space_press)
        

    def update(self):
        if self.end_game == False:
            new_bullet_list = []
            for bullet in self.bullet_list:
                bullet.update_bullet()
                if bullet.needs_deleted:
                    bullet.delete()
                else:
                    new_bullet_list.append(bullet)
            self.bullet_list = new_bullet_list
            self.bullet_collision()
            new_bullet_list = []
            for bullet in self.bullet_list:
                if bullet.needs_deleted:
                    bullet.delete()
                else:
                    new_bullet_list.append(bullet)
            self.bullet_list = new_bullet_list
            for asteroid in self.asteroid_list:
                asteroid.update_asteroid()
            self.collision_detection()
            self.player.update_player()
            self.update_level()
            self.canvas.delete(self.timer.text)
            self.timer.text = self.canvas.create_text(15,15,text=self.timer.timer_text,font=("Fixedsys",7,"bold"),fill='red')
            self.root.after(20,self.update)
        

    def level_progression(self):
        if self.asteroid_list == []:
            self.level += 1
            self.generate_asteroids(self.level * 2 + 1)
            self.grace_period()
            self.update_level()
            return self.level

    
    def grace_period(self):
        self.grace =  True
        self.root.after(4000,self.cancel_grace_period)
        return self.grace

    
    def cancel_grace_period(self):
        self.grace = False
        return self.grace

    
    ############################################################################
    # ASTEROIDS CODE
    ############################################################################


    def generate_asteroids(self,i):
        # creating a set of numbers for the random.choice to choose a radius for the asteroids
        sequence = [constants.LITTLE_ASTEROID_SIZE,constants.MEDIUM_ASTEROID_SIZE,constants.LARGE_ASTEROID_SIZE]
        for _ in range(i):
            new_asteroid = Asteroid(random.randint(0,constants.SCREEN_WIDTH),random.randint(0,constants.SCREEN_HEIGHT),random.randint(0,365),random.choice(sequence),self.canvas)
            self.asteroid_list.append(new_asteroid)
        for asteroid in self.asteroid_list:
            asteroid.create_asteroids()
        return self.asteroid_list


    def collision_detection(self):
        if self.grace == False:
            for asteroid in self.asteroid_list:
                coordsx = (asteroid.x - asteroid.radius,asteroid.x + asteroid.radius)
                coordsy = (asteroid.y - asteroid.radius,asteroid.y + asteroid.radius)
                nx,px = coordsx
                ny,py = coordsy
                p1x,p2x,p3x,p4x = self.player.pointx
                p1y,p2y,p3y,p4y = self.player.pointy
                if (p1x > nx and p1x < px and p1y > ny and p1y < py) or (p2x > nx and p2x < px and p2y > ny and p2y < py) or (p3x > nx and p3x < px and p3y > ny and p3y < py) or (p4x > nx and p4x < px and p4y > ny and p4y < py):
                    self.Game_end()


    ############################################################################
    # BULLET CODE
    ############################################################################           

    def create_bullets(self):
        self.Bullet = Bullet(min(5,2 + self.player.speed),self.player.x,self.player.y,self.player.angle + 90,self.canvas)
        self.bullet_list.append(self.Bullet)
        self.current_time = time.time()
        self.Bullet.create_bullets()
        return self.Bullet,self.bullet_list


    def bullet_collision(self):
            for k,asteroid in enumerate(self.asteroid_list):
                nx = asteroid.x - asteroid.radius
                px = asteroid.x + asteroid.radius
                ny = asteroid.y - asteroid.radius
                py = asteroid.y + asteroid.radius
                for bullet in self.bullet_list:
                    if bullet.x > nx and bullet.x < px and bullet.y > ny and bullet.y < py:
                        bullet.needs_deleted = True
                        self.asteroid_list.pop(k)
                        self.canvas.delete(asteroid.physical_asteroid)
                        if asteroid.radius == constants.MEDIUM_ASTEROID_SIZE:
                            new_asteroid = Asteroid(asteroid.x - 10,asteroid.y - 10,random.randint(0,365),constants.LITTLE_ASTEROID_SIZE,self.canvas)
                            self.asteroid_list.append(new_asteroid)
                            new_asteroid = Asteroid(asteroid.x + 10,asteroid.y + 10,random.randint(0,365),constants.LITTLE_ASTEROID_SIZE,self.canvas)
                            self.asteroid_list.append(new_asteroid)
                        if asteroid.radius == constants.LARGE_ASTEROID_SIZE:
                            new_asteroid = Asteroid(asteroid.x - 10,asteroid.y - 10,random.randint(0,365),constants.MEDIUM_ASTEROID_SIZE,self.canvas)
                            self.asteroid_list.append(new_asteroid)
                            new_asteroid = Asteroid(asteroid.x + 10,asteroid.y + 10,random.randint(0,365),constants.MEDIUM_ASTEROID_SIZE,self.canvas)
                            self.asteroid_list.append(new_asteroid)
                        self.points += 1
                        self.level_progression()


    def update_level(self):
        # TODO: If level_text is None, created else just update
        self.canvas.delete(self.level_text)
        self.level_text = self.canvas.create_text(75, 15, text="Level " + str(self.level),font=("Fixedsys",7,"bold"),fill='green')
        return self.level_text
        

    def end_game_options(self): 
        #self.canvas.delete('all') 
        self.entry1 = Entry (self.root)
        self.score = self.points * 3.5
        self.canvas.create_window(constants.SCREEN_WIDTH / 2 - 100, constants.SCREEN_HEIGHT / 2 - 320, window=self.entry1)
        Submit_button = Button(text='Submit', command=self.Get_name,font=('Fixedsys',10,'bold'))
        Submit_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        _ = self.canvas.create_window(constants.SCREEN_WIDTH / 2 - 110, constants.SCREEN_HEIGHT - 800,window=Submit_button)


    def Get_name(self):
        self.name = self.entry1.get()
        print(str(self.name))
        if self.name == '':
            self.name = 'Ryan'
            # self.canvas.create_text(constants.SCREEN_WIDTH / 2 - 110, constants.SCREEN_HEIGHT - 900, text="You must enter a name",font=("Fixedsys",7,"bold"),fill='green')
            # self.end_game_options()
        if not os.path.isdir('./highscores'):
            os.mkdir('./highscores')
        filename = "highscores.txt"
        current_highscore_list = []
        if os.path.isfile('./highscores/{}'.format(filename)):
            file = open('./highscores/{}'.format(filename),mode='r')
            current_highscores_file = file.read()
            file.close()
            current_highscores_file = current_highscores_file.split('\n')
            for entry in current_highscores_file:
                if entry != '':
                    entry = entry.split('-')
                    entry[0] = float(entry[0])
                    current_highscore_list.append(entry)
        user_place = -1
        for i in range(len(current_highscore_list)):
            item = current_highscore_list[i]
            if self.score > item[0]:
                user_place = i
                break
        else:
            if len(current_highscore_list) < self.max_highscores:
                user_place = len(current_highscore_list)
        if user_place >= 0:
            current_highscore_list.insert(user_place, [self.score,self.name])
            current_highscore_list = current_highscore_list[:self.max_highscores]
            file = open('./highscores/{}'.format(filename),mode='w')
            lines = []
            for item in current_highscore_list:
                item[0] = str(item[0])
                lines.append("-".join(item))
            file.write('\n'.join(lines))
            file.close()
            self.return_or_retry()


    def return_or_retry(self):
        self.canvas.delete('all') 
        self.canvas.create_text(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 1000,font=('Fixedsys',30,'bold'), text=" You lose \nTry again?" )
        Retry_button = Button(self.root,text='Retry?',command=self.main_menu.try_again,font=('Fixedsys',30,'bold'))
        Retry_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        _ = self.canvas.create_window(constants.SCREEN_WIDTH / 2 - 90, constants.SCREEN_HEIGHT - 900, anchor=NW, window=Retry_button)
        Menu_button = Button(self.root,text='Menu',command=self.main_menu.return_to_menu,font=('Fixedsys',30,'bold'))
        Menu_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        _ = self.canvas.create_window(constants.SCREEN_WIDTH / 2 - 100, constants.SCREEN_HEIGHT - 800, anchor=NW, window=Menu_button)
    
    
    def Game_end(self):
            self.end_game = True
            self.player.speed = 0
            self.end_game_options()