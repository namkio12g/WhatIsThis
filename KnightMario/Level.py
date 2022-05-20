
from support import *
import pygame
from settings import *
from  Tile import Tile
from  Tile import StaticTile,one_imageNoAnimated,Coin
from background import Background
from enemy import Enemy
from Player import Player
import data
from  effects import EffectExplosion

class Level():
    def __init__(self,surface,current_level,create_overworld,change_health,change_coins):
        self.surface=surface
        self.create_overworld=create_overworld
        self.change_coins=change_coins
        self.word_shift=0
        self.current_level=current_level
        self.level_data=data.levels[self.current_level]
        self.new_max_level=self.level_data['unlock']
        self.image1=pygame.image.load('Graph/decoration/oak_woods_tileset.png')
        #effects
        self.explosion_sprites=pygame.sprite.GroupSingle()
        #terrian set up
        terrian_layout= import_csv_layout(self.level_data['terrian'])
        self.terrian_image = import_tile_image('Graph/decoration/oak_woods_tileset.png')
        self.terrian_sprites=self.create_tiles(terrian_layout,'terrian')
        #grass
        grass_layout=import_csv_layout(self.level_data['grass'])
        self.grass_sprites=self.create_tiles(grass_layout,'grass')
        #lamp
        lamp_layout = import_csv_layout(self.level_data['lamp'])
        self.lamp_sprites = self.create_tiles(lamp_layout, 'lamp')
        #rock
        rock_layout = import_csv_layout(self.level_data['rock'])
        self.rock_sprites = self.create_tiles(rock_layout, 'rock')
        #fence
        fence_layout = import_csv_layout(self.level_data['fence'])
        self.fence_sprites = self.create_tiles(fence_layout, 'fence')
        #coin
        coin_layout = import_csv_layout(self.level_data['coin'])
        self.coin_sprites = self.create_tiles(coin_layout, 'coin')
        #background
        level_width= len(terrian_layout[1])*64
        self.background=Background(level_width)
        #enemy
        enemy_layout = import_csv_layout(self.level_data['enemy'])
        self.enemy_sprites = self.create_tiles(enemy_layout, 'enemy')
        #constraint
        constraint_layout = import_csv_layout(self.level_data['constraint'])
        self.constraint_sprites = self.create_tiles(constraint_layout, 'constraint')
        #player
        player_layout = import_csv_layout(self.level_data['player'])
        self.player=pygame.sprite.GroupSingle()
        self.Goal = pygame.sprite.GroupSingle()
        self.set_up_player(player_layout,change_health)
        #audio
        self.stomp_music=pygame.mixer.Sound('audio/action/stomp.wav')
        self.stomp_music.set_volume(0.5)
        self.coin_sound=pygame.mixer.Sound('audio/action/coin.wav')
    def scroll_x(self):
        player=self.player.sprite
        player_x=player.rect.centerx
        direction_x=player.direction.x
        if player_x<SCREEN_WIDTH/3 and direction_x<0:
            self.word_shift=8
            player.speed=0
        elif player_x > SCREEN_WIDTH-SCREEN_WIDTH/3 and direction_x > 0:
            self.word_shift = -8
            player.speed = 0
        else:
            self.word_shift = 0
            player.speed = 5
    def create_tiles(self,layout,type):
        sprite_group=pygame.sprite.Group()
        for row_index,row in enumerate(layout):
            for col,val in enumerate(row):
                if val!='-1':
                    x=col*tile_size
                    y=row_index*tile_size
                    if(type=='terrian'):

                        tile_image=self.terrian_image[int(val)]
                        sprite=StaticTile(tile_size,x,y,tile_image)

                    if type=='grass':
                        if val == '0':sprite = one_imageNoAnimated(tile_size,x,y,'Graph/decoration/grass/grass_1.png')
                        if val == '4': sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/grass/grass_2 (1).png')
                        if val == '5': sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/grass/grass_3 (1).png')
                    if type=='lamp':
                        sprite = one_imageNoAnimated(tile_size,x,y,'Graph/decoration/lamp/lamp.png')
                    if type == 'rock':
                        if val == '0': sprite = one_imageNoAnimated(tile_size, x, y,
                                                                    'Graph/decoration/rock/rock_3.png')
                        if val == '1': sprite = one_imageNoAnimated(tile_size, x, y,
                                                                    'Graph/decoration/rock/rock_2.png')
                        if val == '2': sprite = one_imageNoAnimated(tile_size, x, y,
                                                                    'Graph/decoration/rock/rock_1.png')
                    if type == 'fence':
                        sprite = one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/fence/fence_1.png')
                    if type=='coin':
                        sprite =Coin(tile_size,x,y)
                    if type == 'enemy':
                        sprite = Enemy(tile_size, x, y)
                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    def set_up_player(self,layout,change_health):
        for row_index,row in enumerate(layout):
            for col,val in enumerate(row):
                if val!='-1':
                    x=col*tile_size
                    y=row_index*tile_size
                    if val=='1':
                        sprite=Player((x,y),change_health)
                        self.player.add(sprite)
                    if val=='0':
                        sprite=one_imageNoAnimated(tile_size, x, y, 'Graph/decoration/player/END.png')
                        self.Goal.add(sprite)


    def enemy_collide_with_constraint(self):
        for enemy in self.enemy_sprites:
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reversed()


    def y_movement_collide(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.terrian_sprites.sprites():
            if (sprite.rect.colliderect(player.rect) ):
                if player.direction.y > 0 and player.onCeiling==False:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True
        if player.onGround and player.direction.y > 0 or player.direction.y < 0:
            player.onGround = False
        if player.onCeiling and player.direction.y > 0:
            player.onCeiling = False
    def x_movement_collide(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrian_sprites.sprites():
            if (sprite.rect.colliderect(player.rect)):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right
        if player.onLeft and (player.rect.x < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight and (player.rect.x > self.currentX or player.direction.x <= 0):
            player.onRight = False
    #interact
    def check_death(self):
        if self.player.sprite.rect.y>SCREEN_HEIGHT:
            self.create_overworld(self.current_level,0)
    def check_win(self):
        player=self.player.sprite
        goal=self.Goal.sprite
        if  player.rect.colliderect(goal.rect):
            self.create_overworld(self.current_level,self.new_max_level)

    def collide_with_enemy(self):
        sprites_collide=pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        for enemy in sprites_collide:
            enemy_center = enemy.rect.centery
            enemy_top = enemy.rect.top
            player_bottom = self.player.sprite.rect.bottom
            if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                self.player.sprite.direction.y=-15
                explosion_sprite = EffectExplosion(enemy.rect.center)
                self.explosion_sprites.add(explosion_sprite)
                self.stomp_music.play()
                enemy.kill()
            else:
                self.player.sprite.get_damed()
    def collide_with_coins(self):
        sprites_collide = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites, True)
        for coin in sprites_collide:
            self.change_coins(+1)
            self.coin_sound.play()



    def run(self):
        #draw
        self.background.draw(self.surface,self.word_shift)
        self.terrian_sprites.draw(self.surface)
        self.fence_sprites.draw(self.surface)
        self.lamp_sprites.draw(self.surface)
        self.rock_sprites.draw(self.surface)
        self.grass_sprites.draw(self.surface)
        self.enemy_sprites.draw(self.surface)
        self.coin_sprites.draw(self.surface)
        self.player.draw(self.surface)
        self.Goal.draw(self.surface)

        self.explosion_sprites.draw(self.surface)

        self.scroll_x()


        #move
        self.terrian_sprites.update(self.word_shift)
        self.grass_sprites.update(self.word_shift)
        self.lamp_sprites.update(self.word_shift)
        self.explosion_sprites.update(self.word_shift)
        self.player.update()

        self.fence_sprites.update(self.word_shift)
        self.rock_sprites.update(self.word_shift)
        self.coin_sprites.update(self.word_shift)
        self.Goal.update(self.word_shift)
        #collide with enemy
        self.collide_with_enemy()
        self.collide_with_coins()
        self.check_death()
        self.check_win()

        #enemy
        self.enemy_collide_with_constraint()
        self.enemy_sprites.update(self.word_shift)
        self.constraint_sprites.update(self.word_shift)
        self.x_movement_collide()
        self.y_movement_collide()


        pass
