from settings import *

class sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(topleft=pos)
        self.ground=True

class Collisionsprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image=surf
        
        self.rect=self.image.get_rect(topleft=pos)
        self.ground=False

class Bullet(pygame.sprite.Sprite):
    def __init__(self,surf,pos,direction,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(center=pos)
        self.ground=False
        self.spawn_time=pygame.time.get_ticks()
        self.life=1000
        self.direction=direction
        self.speed=1200
    
    def update(self,dt):
        self.rect.center+=self.direction*self.speed*dt
        if pygame.time.get_ticks()-self.spawn_time>=self.life:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player,collision_sprites):
        super().__init__(groups)
        self.player=player
        self.image=pygame.image.load(join('images','enemies','bat','0.png')).convert_alpha()
        self.rect=self.image.get_rect(center =pos )
        self.hitbox_rect=self.rect.inflate(-20,-40)
        self.direction=pygame.Vector2()
        self.collision_sprites=collision_sprites
        self.speed=150
        self.ground=False
    
    def update(self,dt):
        #direction
        player_pos=pygame.Vector2(self.player.rect.center)   
        enemy_pos=pygame.Vector2(self.rect.center)
        self.direction=(player_pos-enemy_pos).normalize()

        self.hitbox_rect.x+=self.speed*self.direction.x*dt
        self.collision('horizontal')
        self.hitbox_rect.y+=self.speed*self.direction.y*dt
        self.collision('vertical')
        self.rect.center=self.hitbox_rect.center

    def collision(self,direction):
        for entity in self.collision_sprites:
            if direction=='horizontal':
                if self.hitbox_rect.colliderect(entity.rect):
                    if self.direction.x>0:
                        self.hitbox_rect.right=entity.rect.left
                    if self.direction.x<0:
                        self.hitbox_rect.left=entity.rect.right
            if direction=='vertical':
                if self.hitbox_rect.colliderect(entity.rect):
                    if self.direction.y>0:
                        self.hitbox_rect.bottom=entity.rect.top
                    if self.direction.y<0:
                        self.hitbox_rect.top=entity.rect.bottom


