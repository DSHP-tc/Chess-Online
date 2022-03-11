import pygame as pg

class Board:
    def __init__(self):
        self.x=100
        self.y=100
        self.block_group=pg.sprite.Group()
        self.font=pg.font.Font("font/COOPBL.TTF",24)
        self.msg0=self.font.render("Your Turn",True,(166,124,82))
        self.msg0_rect=self.msg0.get_rect()
        self.msg0_rect.center=(500,950)

        self.msg1=self.font.render("Opponent's Turn",True,(166,124,82))
        self.msg1_rect=self.msg1.get_rect()
        self.msg1_rect.center=(500,950)

        self.color_msg_b=self.font.render("Your Color: Black",True,(166,124,82))
        self.color_msg_b_rect=self.color_msg_b.get_rect()
        self.color_msg_b_rect.center=(500,50)

        self.color_msg_w=self.font.render("Your Color: White",True,(166,124,82))
        self.color_msg_w_rect=self.color_msg_w.get_rect()
        self.color_msg_w_rect.center=(500,50)
    def createBoard(self):
        color=1
        for row in range(1,9):
            for col in range(1,9):
                id=f"{row}{col}"
                obj=Square(id,color,pg.Vector2((self.x*col,self.y*row)))
                self.block_group.add(obj)
                if color==0:
                    color=1
                else:
                    color=0
            if color==0:
                    color=1
            else:
                color=0
    def getBoardMatrics(self):
        temp=[
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','K','Q','B','N','R'],    
        ]
        return temp

                
                
class Square(pg.sprite.Sprite):
    def __init__(self,id,color,pos):
        super(Square,self).__init__()
        self.id=id
        self.color=color
        self.isselected=False
        self.cell_size=(100,100)
        self.block_img=[pg.transform.scale(pg.image.load("assets/b_square.png").convert(),self.cell_size),
        pg.transform.scale(pg.image.load("assets/w_square.png").convert(),self.cell_size),]
        if self.color==0:
            self.image=self.block_img[0]
        else:
            self.image=self.block_img[1]
        self.rect=self.image.get_rect()
        self.rect.x=pos.x
        self.rect.y=pos.y

        

