from tkinter import *
from tkinter import messagebox
import os
import random
from main_game import game_mechanics
    
    


root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
w = Canvas(root,width=screen_width, height=screen_height)


class play:
    def __init__(self):
        self.game = None

    def menu_screen(self):
        w.delete('all')
        root.resizable(True, True)
        w.create_text(screen_width / 2, screen_height / 2, font=("Fixedsys",50,'bold'), text='Space Rocks')
        play_button = Button(root,text='play?',command=self.play,font=('Fixedsys',20,'bold'),)
        play_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        _ = w.create_window(screen_width / 2 - 100, screen_height / 2 + 80, anchor=NW, window=play_button)
        HS.Highscore_button()


    def play(self):
        w.delete('all')
        root.resizable(False, False)
        self.game = game_mechanics(root,w,self)
        self.game.level_progression()
        self.game.update()
    

    def try_again(self):
        self.play()


    def return_to_menu(self):
        self.menu_screen()
        

class highscores:
    def __init__(self):
        pass


    def Highscore_button(self):
        highscore_button = Button(root,text='Highscores',command=self.print_highscores,font=('Fixedsys',20,'bold'))
        highscore_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        _ = w.create_window(screen_width / 2 - 100, screen_height / 2 + 150, anchor=NW, window=highscore_button)


    def print_highscores(self):
        w.delete('all')
        back_button = Button(root,text='Back',command=self.Back,font=('Fixedsys',20,'bold'))
        back_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        _ = w.create_window(150,0,anchor=NE, window=back_button)
        if not os.path.isdir('./highscores'):
            os.mkdir('./highscores')
        filename = "highscores.txt"
        if os.path.isfile('./highscores/{}'.format(filename)):
            file = open('./highscores/{}'.format(filename),mode='r')
            current_highscores_file = file.read()
            file.close()
            current_highscores_file = current_highscores_file.split('\n')
            highscore_set = 0
            highscores_per_column = 18
            for i in range(70, 1951, 150):
                k = 100
                for line in enumerate(current_highscores_file[highscore_set:highscore_set+highscores_per_column]):
                    w.create_text(i,k,text=line[1:],font=('Fixedsys',15,'bold'))
                    k += 50
                highscore_set += highscores_per_column   


    def Back(self):
        Start.menu_screen()

            
w.pack()
Start = play()
HS = highscores()
Start.menu_screen()


root.mainloop()