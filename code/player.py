from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super(Player,self).__init__(groups)  
        self.load_images()
        self.state,self.frame_index='down',0
        self.image=pygame.image.load(join('images','player','down','0.png')).convert_alpha()
        self.rect=self.image.get_rect(center=pos)
        self.hitbox_rect=self.rect.inflate(-60,-90)

        self.direction=pygame.Vector2()
        self.speed=500
        self.collision_sprites=collision_sprites
        self.ground=False

    def load_images(self):
        self.frames={'left':[],'right':[],'down':[],'top':[]}

       # print(list(walk(join('images','player'))))  this give the list comprising of the info
        for state in self.frames.keys():
            for folder_path,subfolder_path,file_names in walk(join('images','player')):
                if file_names:
                    for file_name in file_names:
                        full_path=join(folder_path,file_name)
                        surf=pygame.image.load(full_path).convert_alpha   
                        self.frames[state].append(surf)
        

    def input(self):
        keys=pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction.x=-1
        elif keys[pygame.K_d]:
            self.direction.x=1
        else:
            self.direction.x=0

        if keys[pygame.K_w]:  
            self.direction.y=-1
        elif keys[pygame.K_s]:
            self.direction.y=1
        else:
            self.direction.y=0

    def move(self,dt):
        if self.direction.magnitude()>0:
            self.direction=self.direction.normalize()

        self.hitbox_rect.x+=self.direction.x*self.speed*dt
        self.collision('horizontal')
        self.hitbox_rect.y+=self.direction.y*self.speed*dt
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


        
    def update(self,dt):
        self.input()
        self.move(dt)
