
import pygame as pg

class Pieces:
    def __init__(self):
        self.piece_group=pg.sprite.Group()
        self.kings=[]

    def createPieces(self):
        
        offset=pg.Vector2((50,50))
        pb1=Rook((100+offset.x,100+offset.y),0)
        pb2=Knight((200+offset.x,100+offset.y),0)
        pb3=Bishop((300+offset.x,100+offset.y),0)
        pb4=Queen((400+offset.x,100+offset.y),0)
        pb5=King((500+offset.x,100+offset.y),0)
        self.kings.append(pb5)
        pb6=Bishop((600+offset.x,100+offset.y),0)
        pb7=Knight((700+offset.x,100+offset.y),0)
        pb8=Rook((800+offset.x,100+offset.y),0)

        locals_stored = set(locals())
        for name in locals_stored:
            if name.startswith("pb"):
                val = eval(name)
                self.piece_group.add(val)

        for i in range(1,9):
            init_x=100*i
            p=Pawn((init_x+offset.x,200+offset.y),0)
            self.piece_group.add(p)

        pw1=Rook((100+offset.x,800+offset.y),1,)
        pw2=Knight((200+offset.x,800+offset.y),1)
        pw3=Bishop((300+offset.x,800+offset.y),1)
        pw4=Queen((500+offset.x,800+offset.y),1)
        pw5=King((400+offset.x,800+offset.y),1)
        self.kings.append(pw5)
        pw6=Bishop((600+offset.x,800+offset.y),1)
        pw7=Knight((700+offset.x,800+offset.y),1)
        pw8=Rook((800+offset.x,800+offset.y),1)

        locals_stored = set(locals())
        for name in locals_stored:
            if name.startswith("pw"):
                val = eval(name)
                self.piece_group.add(val)
        

        for i in range(1,9):
            init_x=100*i
            p=Pawn((init_x+offset.x,700+offset.y),1)
            self.piece_group.add(p)
            

class King(pg.sprite.Sprite):
    def __init__(self,pos,color):
        super(King,self).__init__()
        
        self.color=color  
        self.check=False
        self.isselected=False
        self.allow_list=[]
        if color==0:
            self.image=pg.transform.scale(pg.image.load("assets/b_king.png").convert_alpha(),(75,75))
        else:
            self.image=pg.transform.scale(pg.image.load("assets/w_king.png").convert_alpha(),(75,75))
        self.rect=self.image.get_rect()
        self.rect.center=pos
    def move(self,rect,group):
        self_index=""
      
        new_index=""
        delete_item=False
        for i in self.allow_list:
            if rect==i:
                self_index=[((self.rect.centery-50)//100)-1,((self.rect.centerx-50)//100)-1]
                self.rect.center=rect.center
                new_index=[(rect.y//100)-1,(rect.x//100)-1]
                group.remove(self)
                result=pg.sprite.spritecollide(self,group,False)
                group.add(self)
                if len(result)>0:
                    delete_item=True
                    group.remove(result[0])
        
        
        return [self_index,new_index,delete_item]
    def startCasting(self,piece_group):
        initial_x=self.rect.centerx
        initial_y=self.rect.centery
        self.allow_list.clear()
        move_pos=[
            [initial_x,initial_y-100],
            [initial_x,initial_y+100],
            [initial_x-100,initial_y],
            [initial_x+100,initial_y],
            [initial_x-100,initial_y-100],
            [initial_x+100,initial_y-100],
            [initial_x-100,initial_y+100],
            [initial_x+100,initial_y+100]
        ]
       
        for pos in move_pos:
            if pos[0]>100 and pos[0]<900 and pos[1]>100 and pos[1]<900:
                hit = [s for s in piece_group if s.rect.collidepoint((pos[0],pos[1]))]
                if len(hit)>0:
                    if hit[0].color!=self.color:
                        self.allow_list.append((pos[0]-50,pos[1]-50,100,100))
                else:
                    self.allow_list.append((pos[0]-50,pos[1]-50,100,100))
        return self.allow_list
      

    
class Queen(pg.sprite.Sprite):
    def __init__(self,pos,color):
        super(Queen,self).__init__()
        self.color=color
     
        self.isselected=False
        self.allow_list=[]
        if color==0:
            self.image=pg.transform.scale(pg.image.load("assets/b_queen.png").convert_alpha(),(75,75))
        else:
            self.image=pg.transform.scale(pg.image.load("assets/w_queen.png").convert_alpha(),(75,75))
        self.rect=self.image.get_rect()
        self.rect.center=pos
    def move(self,rect,group):
        self_index=""
      
        new_index=""
        delete_item=False
        for i in self.allow_list:
            if rect==i:
                self_index=[((self.rect.centery-50)//100)-1,((self.rect.centerx-50)//100)-1]
                self.rect.center=rect.center
                new_index=[(rect.y//100)-1,(rect.x//100)-1]
                group.remove(self)
                result=pg.sprite.spritecollide(self,group,False)
                group.add(self)
                if len(result)>0:
                    delete_item=True
                    group.remove(result[0])
       
        
        return [self_index,new_index,delete_item]
    def startCasting(self,piece_group):
        initial_x=self.rect.centerx
        initial_y=self.rect.centery
        tempx=initial_x
        self.allow_list.clear()
        #Check for top#####################################################
        for y in range(initial_y-100,100,-100):
            if y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((initial_x,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((initial_x-50,y-50,100,100))
                if len(hit)>0:
                    break
       
        #Check for bottom
        for y in range(initial_y+100,900,100):
            if y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((initial_x,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        print("Matched")
                        break
                self.allow_list.append((initial_x-50,y-50,100,100))
                if len(hit)>0:
                    break
        
        #Check for left
        for x in range(initial_x-100,100,-100):
            if x>100:
                hit = [s for s in piece_group if s.rect.collidepoint((x,initial_y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((x-50,initial_y-50,100,100))
                if len(hit)>0:
                    break
        
        #Check for right
        for x in range(initial_x+100,900,100):
            if x<900:
                hit = [s for s in piece_group if s.rect.collidepoint((x,initial_y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((x-50,initial_y-50,100,100))
                if len(hit)>0:
                    break
        
        #CHECK for topleft and topright#####################################################
        for y in range(initial_y-100,100,-100):
            tempx=tempx-100
            if tempx>100 and y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    break
        tempx=initial_x
        for y in range(initial_y-100,100,-100):   
            tempx=tempx+100
            if tempx<900 and y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    break
        #CHECK for bottom left and bottom right###################################################
        tempx=initial_x
        for y in range(initial_y+100,900,100):
            tempx=tempx-100
            if tempx>100 and y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    break
        tempx=initial_x
        for y in range(initial_y+100,900,100):   
            tempx=tempx+100
            if tempx<900 and y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        return self.allow_list
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    return self.allow_list
        return self.allow_list

class Rook(pg.sprite.Sprite):
    def __init__(self,pos,color):
        super(Rook,self).__init__()
        self.color=color
   
        self.isselected=False
        self.allow_list=[]
        if color==0:
            self.original_image=pg.transform.scale(pg.image.load("assets/b_rook.png").convert_alpha(),(75,75))
        else:
            self.original_image=pg.transform.scale(pg.image.load("assets/w_rook.png").convert_alpha(),(75,75))
        self.image=self.original_image
        self.rect=self.image.get_rect()
        self.rect.center=pos
    def move(self,rect,group):
        self_index=""
      
        new_index=""
        delete_item=False
        for i in self.allow_list:
            if rect==i:
                self_index=[((self.rect.centery-50)//100)-1,((self.rect.centerx-50)//100)-1]
                self.rect.center=rect.center
                new_index=[(rect.y//100)-1,(rect.x//100)-1]
                group.remove(self)
                result=pg.sprite.spritecollide(self,group,False)
                group.add(self)
                if len(result)>0:
                    delete_item=True
                    group.remove(result[0])
        
        
        return [self_index,new_index,delete_item]
    def startCasting(self,piece_group):
        initial_x=self.rect.centerx
        initial_y=self.rect.centery
        self.allow_list.clear()

        #Check for top#####################################################
        for y in range(initial_y-100,100,-100):
            if y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((initial_x,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((initial_x-50,y-50,100,100))
                if len(hit)>0:
                    break
       
        #Check for bottom
        for y in range(initial_y+100,900,100):
            if y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((initial_x,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        print("Matched")
                        break
                self.allow_list.append((initial_x-50,y-50,100,100))
                if len(hit)>0:
                    break
        
        #Check for left
        for x in range(initial_x-100,100,-100):
            if x>100:
                hit = [s for s in piece_group if s.rect.collidepoint((x,initial_y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((x-50,initial_y-50,100,100))
                if len(hit)>0:
                    break
        
        #Check for right
        for x in range(initial_x+100,900,100):
            if x<900:
                hit = [s for s in piece_group if s.rect.collidepoint((x,initial_y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        return self.allow_list
                self.allow_list.append((x-50,initial_y-50,100,100))
                if len(hit)>0:
                    return self.allow_list
        return self.allow_list

class Knight(pg.sprite.Sprite):
    def __init__(self,pos,color):
        super(Knight,self).__init__()
        self.color=color
        self.isselected=False
  
        self.allow_list=[]
        if color==0:
            self.image=pg.transform.scale(pg.image.load("assets/b_knight.png").convert_alpha(),(75,75))
        else:
            self.image=pg.transform.scale(pg.image.load("assets/w_knight.png").convert_alpha(),(75,75))
        self.rect=self.image.get_rect()
        self.rect.center=pos
    def move(self,rect,group):
        self_index=""
      
        new_index=""
        delete_item=False
        for i in self.allow_list:
            if rect==i:
                self_index=[((self.rect.centery-50)//100)-1,((self.rect.centerx-50)//100)-1]
                self.rect.center=rect.center
                new_index=[(rect.y//100)-1,(rect.x//100)-1]
                group.remove(self)
                result=pg.sprite.spritecollide(self,group,False)
                group.add(self)
                if len(result)>0:
                    delete_item=True
                    group.remove(result[0])
      
        
        return [self_index,new_index,delete_item]
    def startCasting(self,piece_group):
        initial_x=self.rect.centerx
        initial_y=self.rect.centery
        self.allow_list.clear()
        #check for forward then left
        tempy=initial_y-200
        tempx=initial_x-100
        if tempx>100 and tempy>100:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))
        
        #check for forward then right
        tempx=initial_x+100
        if tempx<900 and tempy>100:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))
        
        #check for backward and left
        tempy=initial_y+200
        tempx=initial_x-100
        if tempx>100 and tempy<900:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))
        
        #check for backward and right
        tempx=initial_x+100
        if tempx<900 and tempy<900:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))
        
        #check for left and up
        tempx=initial_x-200
        tempy=initial_y-100
        if tempx>100 and tempy>100:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))
        
        #check for left and down
        tempy=initial_y+100
        if tempx>100 and tempy<900:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))

        #check for right and up
        tempx=initial_x+200
        tempy=initial_y-100
        if tempx<900 and tempy>100:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))

        #check for right and down
        tempy=initial_y+100
        if tempx<900 and tempy<900:
            hit = [s for s in piece_group if s.rect.collidepoint((tempx,tempy))]
            if len(hit)>0:
                if hit[0].color!=self.color:
                    self.allow_list.append((tempx-50,tempy-50,100,100))
            else:
                self.allow_list.append((tempx-50,tempy-50,100,100))

        return self.allow_list

class Bishop(pg.sprite.Sprite):
    def __init__(self,pos,color):
        super(Bishop,self).__init__()
        self.color=color
        self.isselected=False
   
        self.allow_list=[]
        if color==0:
            self.original_image=pg.transform.scale(pg.image.load("assets/b_bishop.png").convert_alpha(),(75,75))
        else:
            self.original_image=pg.transform.scale(pg.image.load("assets/w_bishop.png").convert_alpha(),(75,75))
        self.image=self.original_image
        self.rect=self.image.get_rect()
        self.rect.center=pos


    def move(self,rect,group):
        self_index=""
      
        new_index=""
        delete_item=False
        for i in self.allow_list:
            if rect==i:
                self_index=[((self.rect.centery-50)//100)-1,((self.rect.centerx-50)//100)-1]
                self.rect.center=rect.center
                new_index=[(rect.y//100)-1,(rect.x//100)-1]
                group.remove(self)
                result=pg.sprite.spritecollide(self,group,False)
                group.add(self)
                if len(result)>0:
                    delete_item=True
                    group.remove(result[0])
       
        return [self_index,new_index,delete_item]
    def startCasting(self,piece_group):
        initial_x=self.rect.centerx
        initial_y=self.rect.centery
        tempx=initial_x
        self.allow_list.clear()

        #CHECK for topleft and topright#####################################################
        for y in range(initial_y-100,100,-100):
            tempx=tempx-100
            if tempx>100 and y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    break
        tempx=initial_x
        for y in range(initial_y-100,100,-100):   
            tempx=tempx+100
            if tempx<900 and y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    break
        #CHECK for bottom left and bottom right###################################################
        tempx=initial_x
        for y in range(initial_y+100,900,100):
            tempx=tempx-100
            if tempx>100 and y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        break
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    break
        tempx=initial_x
        for y in range(initial_y+100,900,100):   
            tempx=tempx+100
            if tempx<900 and y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((tempx,y))]
                if len(hit)>0:
                    if hit[0].color==self.color:
                        return self.allow_list
                self.allow_list.append((tempx-50,y-50,100,100))
                if len(hit)>0:
                    return self.allow_list
        return self.allow_list

class Pawn(pg.sprite.Sprite):
    def __init__(self,pos,color):
        super(Pawn,self).__init__()
        self.color=color
        self.isselected=False
      
        self.ismovingfirst=True
        self.movedirection=pg.Vector2((0,1))
        self.allow_list=[]
        

        if color==0:
            self.ortiginal_image=pg.transform.scale(pg.image.load("assets/b_pawn.png").convert_alpha(),(75,75))
            self.maxmovement=200
        else:
            self.ortiginal_image=pg.transform.scale(pg.image.load("assets/w_pawn.png").convert_alpha(),(75,75))
            self.maxmovement=-200
        self.image=self.ortiginal_image
        self.rect=self.image.get_rect()
        self.rect.center=pos
    
    def move(self,rect,group):
        self_index=""
      
        new_index=""
        delete_item=False
        for i in self.allow_list:
            if rect==i:
                self_index=[((self.rect.centery-50)//100)-1,((self.rect.centerx-50)//100)-1]
                self.rect.center=rect.center
                new_index=[(rect.y//100)-1,(rect.x//100)-1]
                group.remove(self)
                result=pg.sprite.spritecollide(self,group,False)
                group.add(self)
                if len(result)>0:
                    delete_item=True
                    group.remove(result[0])
                if self.ismovingfirst==True:
                    self.ismovingfirst=False
        
        return [self_index,new_index,delete_item]      
        
            
    def startCasting(self,piece_group):
        initial_x=self.rect.centerx
        initial_y=self.rect.centery
        self.allow_list.clear()
        if self.color==1:
            hit_x=initial_x-100
            hit_y=initial_y-100
           
            if hit_x>100 and hit_y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((hit_x,hit_y))]
                if len(hit)>0:
                    if hit[0].color!=self.color:
                        self.allow_list.append((hit_x-50,hit_y-50,100,100))
            hit_x=initial_x+100
            if hit_x<900 and hit_y>100:
                hit = [s for s in piece_group if s.rect.collidepoint((hit_x,hit_y))]
                if len(hit)>0:
                    if hit[0].color!=self.color:
                        self.allow_list.append((hit_x-50,hit_y-50,100,100))
            
            if self.ismovingfirst==True:
                for y in range(initial_y-100,initial_y-201,-100):
                    hit = [s for s in piece_group if s.rect.collidepoint((initial_x,y))]
                    if len(hit)>0:
                        continue
                    else:
                        self.allow_list.append((initial_x-50,y-50,100,100))
            else:
                tempy=initial_y-100
                if tempy>100:
                    hit = [s for s in piece_group if s.rect.collidepoint((initial_x,tempy))]
                    if len(hit)==0:
                        self.allow_list.append((initial_x-50,tempy-50,100,100))    
                  
                        
            
            return self.allow_list
        else:
            hit_x=initial_x-100
            hit_y=initial_y+100
           
            if hit_x>100 and hit_y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((hit_x,hit_y))]
                if len(hit)>0:
                    if hit[0].color!=self.color:
                        self.allow_list.append((hit_x-50,hit_y-50,100,100))
            hit_x=initial_x+100
            if hit_x<900 and hit_y<900:
                hit = [s for s in piece_group if s.rect.collidepoint((hit_x,hit_y))]
                if len(hit)>0:
                    if hit[0].color!=self.color:
                        self.allow_list.append((hit_x-50,hit_y-50,100,100))
            
            if self.ismovingfirst==True:
                for y in range(initial_y+100,initial_y+201,100):
                    hit = [s for s in piece_group if s.rect.collidepoint((initial_x,y))]
                    if len(hit)>0:
                        continue
                    else:
                        self.allow_list.append((initial_x-50,y-50,100,100))
            else:
                tempy=initial_y+100
                if tempy<900:
                    hit = [s for s in piece_group if s.rect.collidepoint((initial_x,tempy))]
                    if len(hit)==0:
                        self.allow_list.append((initial_x-50,tempy-50,100,100))
           
            return self.allow_list

    
   

        
    
        
    