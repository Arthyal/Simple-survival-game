from settings import *

class Gun(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.player=player
        self.distance=140
        self.angle=pygame.Vector2(1,0)
        
        self.ground=False 
        self.gun_surf=pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.image=self.gun_surf
        print(type(self.image))
        self.rect=self.image.get_rect(center = self.player.rect.center + self.angle*self.distance)

    def get_direction(self):
        mouse_pos=pygame.Vector2(pygame.mouse.get_pos())
        player_pos=pygame.Vector2(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        self.angle=(mouse_pos-player_pos).normalize()

    def rotate(self):
        angle=math.degrees(math.atan2(self.angle.x,self.angle.y))-90
        if self.angle.x>0:
            self.image=pygame.transform.rotozoom(self.gun_surf,angle,1)
        else:
            self.image=pygame.transform.rotozoom(self.gun_surf,abs(angle),1)
            self.image=pygame.transform.flip(self.image,False,True)


    def update(self,_):
        self.get_direction()
        self.rotate()
        self.rect.center=self.player.rect.center + self.angle*self.distance
        