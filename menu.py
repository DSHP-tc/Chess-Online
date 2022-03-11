import pygame as pg
# a67c52
class MainMenu:
    def __init__(self):
        self.main_menu_group=pg.sprite.Group()
        self.host_button=Button((250,500),"host_button.png")
        self.join_button=Button((750,500),"join_button.png")
        self.start_button=Button((500,850),"start.png")
        self.submit_button=Button((500,850),"submit_button.png")
        self.main_menu_group.add(self.host_button)
        self.main_menu_group.add(self.join_button)

        self.font=pg.font.Font("font/COOPBL.TTF",72)
        self.heading_text=self.font.render("Chess Online",True,(166,124,82))
        self.heading_text_rect=self.heading_text.get_rect()
        self.heading_text_rect.center=(500,200)
        self.font=pg.font.Font("font/COOPBL.TTF",36)
        self.game_code_text=self.font.render("Game Code: ",True,(166,124,82))
        self.game_code_text_rect=self.game_code_text.get_rect()
        self.game_code_text_rect.center=(500,700)

        self.game_code_input=self.font.render("Enter Code",True,(166,124,82))
        self.game_code_input_rect=self.game_code_input.get_rect()
        self.game_code_input_rect.center=(500,700)

        self.input_box=pg.Rect(200, 200, 300, 100)
        self.input_box.center=(500,700)
        self.menu_choice=""

        self.font=pg.font.Font("font/COOPBL.TTF",24)
        self.msg=self.font.render("",True,(166,124,82))
        self.msg_rect=self.msg.get_rect()
        self.msg_rect.center=(500,950)

    def setMsg(self,msg):
        self.msg=self.font.render(msg,True,(166,124,82))
        self.msg_rect=self.msg.get_rect()
        self.msg_rect.center=(500,950)

class Button(pg.sprite.Sprite):
    def __init__(self,pos,img_name):
        super(Button,self).__init__()
        self.image=pg.image.load(f"assets/{img_name}").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center=pos
