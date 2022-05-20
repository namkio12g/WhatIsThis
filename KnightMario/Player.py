import  pygame
from colorss import *
import support
from settings import *
from math import sin
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,change_health):
        super().__init__()
        self.change_health=change_health
        self.setup_animations()
        self.frame_index=0
        self.animation_speed=0.15
        self.status='idle'
        self.facing_right=True
        self.onGround=True
        self.onCeiling=False
        self.onLeft=False
        self.onRight=False
        self.image=self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.invincible=False
        self.invincible_duration=800
        self.hurt_time=0
        self.hit_sound=pygame.mixer.Sound('audio/action/hit.wav')
        self.jump_sound=pygame.mixer.Sound('audio/action/jump.wav')
        self.jump_sound.set_volume(0.2)
        #chuyen dong nhan vat

        self.direction = pygame.math.Vector2(0, 0)
        self.jump_speed=-18
        self.gravity=1
        self.speed=5
    def setup_animations(self):
        character_path = 'Graph/decoration/character/'
        self.animations={'idle':[],'fall':[],'jump':[]}
        for animation in self.animations.keys() :
            full_path=character_path+animation
            self.animations[animation]=support.import_folder(full_path)

    def setup_status(self):
        if self.direction.y<0:
            self.status='jump'
        elif self.direction.y>1:
            self.status='fall'
        else:

                self.status = 'idle'

    def get_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] :
            self.jump()
        if keys[pygame.K_LEFT]:
            self.direction.x=-1
            self.facing_right=False
        elif keys[pygame.K_RIGHT]:
            self.direction.x=1
            self.facing_right = True
        else :
            self.direction.x=0
    def animate(self):
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(animation):
            self.frame_index=0
        image=animation[int(self.frame_index)]
        if self.facing_right==True:
            self.image=image
        else:
            self.image=pygame.transform.flip(image,True,False)
        if self.invincible:
            value=self.Glitch()
            self.image.set_alpha(value)
        else:
            self.image.set_alpha(255)
        #SET UP RECT
        if self.onGround and self.onLeft:
            self.rect=self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.onGround and self.onRight:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.onGround :
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.onCeiling and self.onLeft:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.onCeiling and self.onRight:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def apply_gravity(self):
        self.direction.y+=self.gravity
        self.rect.y+=self.direction.y
    def jump(self):
        if self.onGround==True and self.onCeiling!=True:
            self.direction.y=self.jump_speed
            self.jump_sound.play()
    def get_damed(self):
        if not self.invincible:
            self.change_health(-1)
            self.invincible=True
            self.hit_sound.play()
            self.hurt_time=pygame.time.get_ticks()

    def invincibility(self):
        if self.invincible:
            currenTime=pygame.time.get_ticks()
            if currenTime-self.hurt_time>=self.invincible_duration:
                self.invincible=False

    def Glitch(self):
        a = sin(pygame.time.get_ticks())
        if a>=0 :return 255
        else:return 0
    def update(self):
        self.get_input()
        self.setup_status()
        self.animate()
        self.invincibility()









