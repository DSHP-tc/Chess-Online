import sys
import string,random,threading

import pygame as pg
from board import Board
from pieces import Pieces
from menu import MainMenu
from connection import Connection
pg.init()

class Game:
    def __init__(self):
        self.win=pg.display.set_mode((1000,1000))
        self.connection=Connection()
        self.mainmenu=MainMenu()
        self.board=Board()
        self.board.createBoard()
        self.board_matrix=self.board.getBoardMatrics()
        self.pieces=Pieces()
        self.pieces.createPieces()
        self.last_selected_piece=None
        self.last_selected_block=None
        self.selected_rect=None
        self.allowed_rects=[]
        self.action=[None,None,None]
        self.mycolor=1
        self.myturn=True
        self.switchtogame=False
        self.game_code_input=""
        self.game_code=""
        self.input_text=False
        self.input_limit=8
        self.data=None
        self.notifyevent=pg.USEREVENT+1
        self.startlisten=False
        self.game_over=False
        pg.time.set_timer(self.notifyevent, 5000)
      
        self.notify_thread = threading.Thread(target=self.notificationListner)
        self.main()

    def processSelection(self,pos):
        clicked_pieces = [s for s in self.pieces.piece_group if s.rect.collidepoint(pos)]
        if len(clicked_pieces)>0:
            if clicked_pieces[0].color==self.mycolor:
                clicked_pieces[0].isselected=True
                if self.last_selected_piece!=None:
                    self.last_selected_piece.isselected=False
                self.last_selected_piece=clicked_pieces[0]
                self.selected_rect=clicked_pieces[0].rect
                self.last_selected_block=None
                self.allowed_rects=self.last_selected_piece.startCasting(self.pieces.piece_group)
                print(self.allowed_rects)
            
        else:
            clicked_block = [s for s in self.board.block_group if s.rect.collidepoint(pos)]
            clicked_block[0].isselected=True
            if self.last_selected_block!=None:
                self.last_selected_block.isselected=False
            self.last_selected_block=clicked_block[0]
            self.selected_rect=clicked_block[0].rect
            self.last_selected_piece=None
            self.allowed_rects=[]
    def drawAllowedRects(self):
        if len(self.allowed_rects)>0:
            for rect in self.allowed_rects:
                pg.draw.rect(self.win,(0,255,0),rect,1)
    def drawSelectedRect(self,rect):
        if self.selected_rect!=None:
            pg.draw.rect(self.win,(255,0,0),rect,1)
    def updateGameState(self,personal):
        if personal==True:
            if self.action[0]!="" and self.action[1]!="":  
              
                target_i=self.action[1][0]
                target_j=self.action[1][1]
                initial_i=self.action[0][0]
                initial_j=self.action[0][1]
                self.board_matrix[target_i][target_j]=self.board_matrix[initial_i][initial_j]
                self.board_matrix[initial_i][initial_j]='-'
        else:
       
            target_i=self.action[1][0]
            target_j=self.action[1][1]
            initial_i=self.action[0][0]
            initial_j=self.action[0][1]
            self.board_matrix[target_i][target_j]=self.board_matrix[initial_i][initial_j]
            self.board_matrix[initial_i][initial_j]='-'

            target_x=((target_j+1)*100)+50
            target_y=((target_i+1)*100)+50
            initial_x=((initial_j+1)*100)+50
            initial_y=((initial_i+1)*100)+50
            if self.action[2]==True:
                clicked_piece = [s for s in self.pieces.piece_group if s.rect.collidepoint((target_x,target_y))]
                # if len(clicked_piece)>0:
                self.pieces.piece_group.remove(clicked_piece[0])
            clicked_piece = [s for s in self.pieces.piece_group if s.rect.collidepoint((initial_x,initial_y))]
            
            clicked_piece[0].rect.center=(target_x,target_y)
            


    def notificationListner(self):
        self.data=self.connection.getUpdates()
        ("Notofication received",self.data)
        if self.data!=None:
            if ("start" in self.data["msg"]) and self.data["self_pos"]!="":
                self.action[0]=self.data["self_pos"]
                self.action[1]=self.data["new_pos"]
                self.action[2]=self.data["delete"]
                self.updateGameState(False)
                self.myturn=True
    def showMenu(self):

        for event in pg.event.get():
            if event.type==pg.QUIT:
                if self.connection.userref!=None:
                    self.connection.closeConnection()
                pg.quit()
                sys.exit()
            if event.type==pg.MOUSEBUTTONDOWN:
                pos=pg.mouse.get_pos()
                if event.button==1:
                    #STARTING THE SERVER#################################################
                    if self.mainmenu.host_button.rect.collidepoint(pos): 
                        self.startlisten=True
                        if self.mainmenu.submit_button in self.mainmenu.main_menu_group:
                            self.mainmenu.main_menu_group.remove(self.mainmenu.submit_button)
                        self.mainmenu.setMsg("") 
                        self.game_code = ''.join(random.choices(string.ascii_lowercase, k = 8))
                        self.mainmenu.game_code_text=self.mainmenu.font.render(f"Game Code: {self.game_code}",True,(166,124,82))
                        self.mainmenu.game_code_text_rect=self.mainmenu.game_code_text.get_rect()
                        self.mainmenu.game_code_text_rect.center=(500,700)
                        self.mainmenu.menu_choice="host"
                        self.connection.startConnection(self.game_code)
                        self.mainmenu.setMsg("Share the game code and wait for opponent to join")
                    if self.mainmenu.start_button.rect.collidepoint(pos):
                        if self.mainmenu.menu_choice=="host":
                            self.switchtogame=True
                            self.mycolor=random.randint(0,1)
                            if self.mycolor==1:
                                self.myturn=True
                                self.data=self.connection.lastmsg
                                self.data["msg"]="start:0"
                                
                            else:
                                self.data=self.connection.lastmsg
                                self.data["msg"]="start:1"
                                self.myturn=False
                            self.connection.lastmsg=self.data
                            self.connection.sendUpdates()
                            return
                    
                    #JOINING THE SERVER###########################################################
                    if self.mainmenu.join_button.rect.collidepoint(pos):
                        self.startlisten=False  
                        if self.game_code!="":
                            self.connection.closeConnection()
                        self.mainmenu.setMsg("") 
                        self.mainmenu.menu_choice="join"
                        self.game_code_input="Enter Code"
                    if self.mainmenu.input_box.collidepoint(pos):
                        if self.input_text==False:
                            self.game_code_input=""
                        self.input_text=True
                    else: 
                        self.input_text=False
                    if self.mainmenu.submit_button.rect.collidepoint(pos):
                        if self.mainmenu.menu_choice=="join":
                            msg=self.connection.checkConnection(self.game_code_input)
                            if "Game Found" in msg:
                                self.startlisten=True
                            self.mainmenu.setMsg(msg)
            if event.type==pg.TEXTINPUT and self.input_text==True and len(self.game_code_input)<8:
                self.game_code_input += event.text
                if len(self.game_code_input)==8:
                    self.mainmenu.main_menu_group.add(self.mainmenu.submit_button)
                    self.mainmenu.setMsg("Submit the code and wait for host to start the game")
                

            if event.type==pg.KEYDOWN and self.input_text==True:
                if event.key == pg.K_BACKSPACE:
                    self.game_code_input = self.game_code_input[:-1]
                    if self.mainmenu.submit_button in self.mainmenu.main_menu_group:
                        self.mainmenu.main_menu_group.remove(self.mainmenu.submit_button)
            
            if event.type==self.notifyevent and self.startlisten:
                self.notify_thread.start()
                self.notify_thread=threading.Thread(target=self.notificationListner)
               
            
        if self.data!=None and self.mainmenu.menu_choice=="host":   
            if self.data["msg"]=="Opponent Joined":
                self.mainmenu.main_menu_group.add(self.mainmenu.start_button) 
                self.mainmenu.setMsg("Opponent joined the game")
        if self.data!=None and self.mainmenu.menu_choice=="join":
            if "start" in self.data["msg"]:
                temp=self.data["msg"].split(":")
                self.mycolor=int(temp[1])
                if self.mycolor==1:
                    self.myturn=True
                else:
                    self.myturn=False
                self.switchtogame=True
                return
                
        self.win.fill(0)
        self.mainmenu.main_menu_group.draw(self.win)
        self.win.blit(self.mainmenu.heading_text,self.mainmenu.heading_text_rect)
        
        self.win.blit(self.mainmenu.msg,self.mainmenu.msg_rect)
        if self.mainmenu.menu_choice=="host":
            self.win.blit(self.mainmenu.game_code_text,self.mainmenu.game_code_text_rect)
        elif self.mainmenu.menu_choice=="join":
            self.mainmenu.game_code_input=self.mainmenu.font.render(self.game_code_input,True,(166,124,82))
            self.mainmenu.game_code_input_rect=self.mainmenu.game_code_input.get_rect()
            self.mainmenu.game_code_input_rect.center=(500,700)
            pg.draw.rect(self.win,(166,124,82),self.mainmenu.input_box,5) 
            self.win.blit(self.mainmenu.game_code_input,self.mainmenu.game_code_input_rect)
        
    def main(self):
        final_msg=""
        font=pg.font.Font("font/COOPBL.TTF",72)
        
        run=True
        clock=pg.time.Clock()
        while run:
            if self.switchtogame==False:
                self.showMenu()
            else:
                if self.game_over==False:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            self.connection.closeConnection()
                            pg.quit()
                            sys.exit()
                        if event.type==pg.MOUSEBUTTONDOWN:
                            if event.button==3 and self.myturn==True:
                                pos = pg.mouse.get_pos()
                                self.processSelection(pos)
                            elif event.button==1 and self.myturn==True:
                                pos = pg.mouse.get_pos()
                                if self.last_selected_piece!=None:      
                                    clicked_block = [s for s in self.board.block_group if s.rect.collidepoint(pos)]
                                    self.action=self.last_selected_piece.move(clicked_block[0].rect,self.pieces.piece_group)
                                    print("Recived",self.action)
                                    if self.action[0]!=self.action[1]:
                                        self.myturn=False
                                        self.updateGameState(True)
                                    
                                    self.connection.lastmsg["self_pos"]=self.action[0]
                                    self.connection.lastmsg["new_pos"]=self.action[1]
                                    self.connection.lastmsg["delete"]=self.action[2]
                                    self.connection.sendUpdates()
                                    self.allowed_rects=[]
                                    self.last_selected_piece=None
                                    self.selected_rect=None
                        if event.type==self.notifyevent and self.startlisten:
                            self.notify_thread.start()
                            self.notify_thread=threading.Thread(target=self.notificationListner)
                    
                    if self.pieces.kings[0] not in self.pieces.piece_group:
                        self.game_over=True
                        if self.mycolor==0:
                            final_msg="You Lost"
                        else:
                            final_msg="Opponent Lost"
                    if self.pieces.kings[1] not in self.pieces.piece_group:
                        self.game_over=True
                        if self.mycolor==1:
                            final_msg="You Lost"
                        else:
                            final_msg="Opponent Lost"
                    self.win.fill(0)
                    if self.myturn==True:
                        self.win.blit(self.board.msg0,self.board.msg1_rect)
                    elif self.myturn==False:
                        self.win.blit(self.board.msg1,self.board.msg0_rect)
            
                    if self.mycolor==0:
                        self.win.blit(self.board.color_msg_b,self.board.color_msg_b_rect)
                    elif self.mycolor==1:
                        self.win.blit(self.board.color_msg_w,self.board.color_msg_w_rect)
                    self.board.block_group.draw(self.win)
                    self.pieces.piece_group.draw(self.win)
                    self.drawSelectedRect(self.selected_rect)
                    self.drawAllowedRects()
                else:
                    for event in pg.event.get():
                        if event.type==pg.QUIT:
                            self.connection.closeConnection()
                            pg.quit()
                            sys.exit()
                    msg0=font.render(final_msg,True,(166,124,82))
                    msg0_rect=msg0.get_rect()
                    msg0_rect.center=(500,500)
                    self.win.blit(msg0,msg0_rect)
            pg.display.update()
            clock.tick(60)

game_obj=Game()