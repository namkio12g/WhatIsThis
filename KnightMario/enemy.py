from Tile import AnimatedImage
from  random import randint
import  pygame
class Enemy(AnimatedImage):
    def __init__(self, size, x, y, ):
        super().__init__(size, x, y, 'Graph/decoration/enemy' )
        self.rect.y+=size-self.image.get_size()[1]
        self.speed=randint(2,4)
    def move(self):

        self.rect.x+=self.speed
    def move_reverse(self):
        if self.speed<0:
            self.image=pygame.transform.flip(self.image,True,False)
    def reversed(self):
        self.speed*=-1
    def update(self,shift):


        self.rect.x += shift
        self.frames_moving()
        self.move()
        self.move_reverse()