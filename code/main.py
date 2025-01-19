from settings import *
from player import Player
from sprites import *
import math
import random 
from pytmx.util_pygame import load_pygame
from groups import Allsprites
from gun import *
from menue import *


class Game:
    def __init__(self):
        #setup
        pygame.init()
        
       
        self.score=0
        self.screen = pygame.display.set_mode((1280 ,720))
        self.clock=pygame.time.Clock()
        self.running=True

        #groups
        self.all_sprites=Allsprites()
        self.collision_sprites=pygame.sprite.Group()
        self.bullet_sprites=pygame.sprite.Group()
        self.enemy_sprites=pygame.sprite.Group()
        #bullet
        
        self.can_shoot=True
        self.shoot_time=0
        self.gun_cooldown=100# means 100 milliseconds
        self.bullet_surf=pygame.image.load(join('images','gun','bullet.png')).convert_alpha()

        self.enemy_event=pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event,300)
        self.spawn_positions=[]

        self.shoot_sound=pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_sound.set_volume(4.0)
        self.impact_sound=pygame.mixer.Sound(join('audio','impact.ogg'))
        self.impact_sound.set_volume(20.0)
        self.music=pygame.mixer.Sound(join('audio','music.wav '))
        self.music.set_volume(2.0)
      
        self.music.play(loops =-1)

    def input_bullets(self):
       if pygame.mouse.get_pressed()[0] and self.can_shoot:#to get left mouse button input
           pos=self.gun.rect.center + self.gun.angle*50
           self.shoot_sound.play()
           Bullet(self.bullet_surf,pos,self.gun.angle,(self.all_sprites,self.bullet_sprites))
           self.can_shoot=False
           self.shoot_time=pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.shoot_time>=self.gun_cooldown:
                self.can_shoot=True

            

        
    def sprites(self):
        map =load_pygame(join('data','map','world.tmx'))
        for x,y ,image in map.get_layer_by_name('Ground').tiles():
            sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            Collisionsprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))
        

        for obj in map.get_layer_by_name('Collisions'):
            Collisionsprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprites)
        
        for obj in map.get_layer_by_name('Entities'):
            if obj.name=='Player':
                self.player=Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)
                self.gun=Gun(self.player,self.all_sprites)
            else:
                self.spawn_positions.append((obj.x,obj.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision=pygame.sprite.spritecollide(bullet,self.enemy_sprites,True)# true means it will kill enemy
                if collision:
                    self.impact_sound.play()
                    self.score+=1
                    bullet.kill()
        
    def player_collision(self):
        for enemy in self.enemy_sprites:
            if self.player.hitbox_rect.colliderect(enemy.hitbox_rect):
               self.running=False

    

    def run(self,menue):


        pause=False
        while self.running:
            
            from pygame.locals import (
           
            KEYDOWN,
            QUIT,
            K_m
            )
            #dt
            dt=self.clock.tick()/1000

          
             
            #event loop
            events=pygame.event.get()
            
            for event in events :
                if event.type ==QUIT:
                   self.running=False
                if event.type==self.enemy_event and not pause:
                    self.enemy=Enemy(random.choice(self.spawn_positions),(self.all_sprites,self.enemy_sprites),self.player,self.collision_sprites)
                if event.type==KEYDOWN:
                    if event.key==K_m:
                        if  pause:
                            pause=False
                        else:
                            pause=True

            if not pause:
            #update
               self.gun_timer()
               self.input_bullets()
               self.all_sprites.update(dt)
               self.bullet_collision()
               self.player_collision()
               #draw        
               self.screen.fill('black')
               # for entity in self.all_sprites:
               #   self.display.blit(entity.image,entity.rect)
               self.all_sprites.draw(self.screen,self.player.rect.center)
            else:
               #menue=Menue()
               menue.input(events)
               
               menue.draw(self.score)
               
             
         
            pygame.display.flip()
        pygame.quit() 
if __name__=="__main__":
    
    game=Game()
    menue=Menue()
    game.sprites()
    game.run(menue)
    