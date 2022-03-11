import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Connection:
    def __init__(self):
        self.cert={
                    #Your credntials
                    }
        
        self.cred = credentials.Certificate(self.cert)

        
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': "your db url"
        })
        self.ref = db.reference('/')
        self.userref=None
        self.game_code=""
        self.lastmsg={
            "self_pos":"",
            "new_pos":"",
            "delete":False,
            "msg":None
        }
        self.listener_obj=None
        self.keep_listen=True

    
    def startConnection(self,game_code):
        self.lastmsg["msg"]="Server Started"
        self.ref.update({
            f"{game_code}":self.lastmsg
        })
        self.game_code=game_code
        self.userref=self.ref.child(game_code)
    
    def checkConnection(self,game_code):
        self.userref=self.ref.child(game_code)
        result=self.userref.get()
        if result==None:
            return "Game does not exist"
        else:
            self.lastmsg["msg"]="Opponent Joined"
            self.userref.set(self.lastmsg)
            return "Game Found, wait for the host to start the game"
    
    def closeConnection(self):
        self.userref.delete()

    def getUpdates(self):
        new_data=self.userref.get()
        if new_data!=self.lastmsg:
            self.lastmsg=new_data
            return self.lastmsg
        else:
            return None

    def sendUpdates(self):
        self.userref.update(self.lastmsg)
       

