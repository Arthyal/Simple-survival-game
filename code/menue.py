from settings import *


class Menue():
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        self.font=pygame.font.Font(None,100)
        self.left=0
        self.top= 0
        self.general_index={'row':0,'col':0}
        self.general_options=['difficulty','enemy','score','volume']
        self.state='general'

    def input(self,events):
    
        a,b,c,d=0,0,0,0
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    a=1 
                else:
                    a=0
                if event.key==pygame.K_DOWN:
                    b=1
                else:
                    b=0
                if event.key==pygame.K_RIGHT:
                    c=1
                else:
                    c=0
                if event.key==pygame.K_LEFT:
                    d=1
                else:
                    d=0
                if event.key==pygame.K_SPACE:
                    self.state=self.general_options[self.general_index['col']+self.general_index['row']*2]
                             
        self.general_index['row']=(self.general_index['row']+b-a)%3
        self.general_index['col']=(self.general_index['col']+c-d)%3
        
    

    def general(self,score):
        score=str(score)
        rect=pygame.Rect(self.left,self.top,1280,720)
        pygame.draw.rect(self.display_surface,(255,255,255),rect,0,4)
        pygame.draw.rect(self.display_surface,(127,127,127),rect,4,4)
        
        rows=3
        cols=3
        for col in range(cols):
            for row in range(rows):
                x=rect.left+rect.width/6+(rect.width/3)*col
                y=rect.top+rect.height/6+(rect.height/3)*row
                if col==self.general_index['col'] and  row==self.general_index['row']:
                    color=(127,127,127)
                else :color=(0,0,0)
                i=col+row*3
            
                if i==0:
                      self.image=pygame.image.load(join('images','enemies','bat','0.png')).convert_alpha()
                      self.rect=self.image.get_rect(center=(x,y))
                      self.display_surface.blit(self.image,self.rect)
                elif i==1:
                      self.image=pygame.image.load(join('images','enemies','blob','0.png')).convert_alpha()
                      self.rect=self.image.get_rect(center=(x,y))
                      self.display_surface.blit(self.image,self.rect)
                elif i==2:
                      self.image=pygame.image.load(join('images','enemies','skeleton','0.png')).convert_alpha()
                      self.rect=self.image.get_rect(center=(x,y))
                      self.display_surface.blit(self.image,self.rect)
                else:
                    text_surf=self.font.render(score,True,color)
                    text_rect=text_surf.get_rect(center=(x,y))
                    self.display_surface.blit(text_surf,text_rect)

    def draw(self,score):
        if self.state=="general":
            self.general('score')
        if self.state=='score':
            self.general(score)