from settings import *

class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset=pygame.Vector2()
  
    def draw(self,surface,target_pos):
        self.offset.x=-(target_pos[0]-WINDOW_WIDTH/2)#remember that the target_pos is the tuple of coordinates in the form (x,y)
        self.offset.y=-(target_pos[1]-WINDOW_HEIGHT/2)#remember that the target_pos is the tuple of coordinates in the form (x,y)
        ground_sprites=[sprite for sprite in self if sprite.ground==True]
        object_sprites=[sprite for sprite in self if sprite.ground==False]
        for layer in [ground_sprites,object_sprites]:
            for entity in sorted(layer,key=lambda sprite:sprite.rect.centery):
                surface.blit(entity.image,entity.rect.topleft + self.offset)

       