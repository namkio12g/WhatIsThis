import sys

import pygame
from  Level import Level
from settings import  *
import colorss
from overworld import Overworld
from UI import UI

import data
class Game:
    def __init__(self):
        self.max_level=0
        self.max_health = 3
        self.current_health = 6
        self.coins = 0
        self.overworld = Overworld(0,self.max_level,SCREEN,self.create_level)
        self.status='overworld'
        self.ui=UI(SCREEN)
        self.mainOverSound=pygame.mixer.Sound('audio/Pokemon Black & White OST - 5-198 The First Day.mp3')
        self.mainlevelSound = pygame.mixer.Sound('audio/Pokemon Black & White OST - 6-198 Kanoko Town.mp3')
        self.mainlevelSound.set_volume(0.5)
        self.mainOverSound.set_volume(0.5)
        self.mainOverSound.play(loops=-1)

    def create_level(self,current_level):
        self.level= Level( SCREEN,current_level,self.create_overworld,self.change_health,self.change_coins)
        self.status='level'
        self.mainOverSound.stop()
        self.mainlevelSound.play(loops=-1)
    def create_overworld(self, current_level,max_level):
        if max_level>self.max_level:
            self.max_level=max_level
        self.overworld = Overworld(current_level,self.max_level,SCREEN,self.create_level)
        self.status='overworld'
        self.mainlevelSound.stop()
        self.mainOverSound.play(loops=-1)
    def change_coins(self,num):
        self.coins+=num
    def change_health(self,num):
        self.current_health+=num

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 3
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, SCREEN, self.create_level)
            self.status = 'overworld'
            self.mainlevelSound.stop()
            self.mainOverSound.play(loops=-1)




    def run(self):
        if self.status=='overworld':
            self.overworld.run()
        else :
            self.level.run()
            self.ui.show_coins(self.coins)
            self.ui.show_health(self.current_health)
            self.check_game_over()



SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game=Game()

CLOCK= pygame.time.Clock()
def main():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill(colorss.black)
        game.run()
        # map.run()
        pygame.display.update()
        CLOCK.tick(60)




# Press the green button in the gutter to run the script.

main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
