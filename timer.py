class Timer:
    def __init__(self,game):
        self.game = game
        self.timer_text = 0
        self.text = None
        self.timing = True

    
    def update_timer(self):
        if self.timing == False or self.game.end_game == True:
            return
        else:
            self.timer_text += 1
            self.game.root.after(1000,self.update_timer)