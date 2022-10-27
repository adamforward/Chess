from ctypes.wintypes import CHAR
from xmlrpc.client import boolean


class piece:
    def __init__(self, val:int, type:CHAR, team:CHAR, pinned: bool,underAttack): 
        self.val=val
        self.type=type
        self.team=team
        
class board:
    def __init_subclass__(self, cls):
        self=cls
    def __init__(self):
        self.fullBoard=[[piece(5,'r','b'),piece(3,'k','b'),piece(3,'b','b'),piece(0,'K','b'),piece(9, 'q', 'b'),piece(3,'b','b'),\
            piece(3,'k','b'), piece(5,'r','b')],[piece(1,'p','b'),piece(1,'p','b'),piece(1,'p','b'),piece(1,'p','b'),piece(1,'p','b'),\
            piece(1,'p','b'),piece(1,'p','b'),piece(1,'p','b')][piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),\
            piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),]\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')],\
            [piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w'),\
            piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w')],
            [piece(5,'r','w'),piece(3,'k','w'),piece(3,'b','w'),piece(0,'K','w'),piece(9, 'q', 'w'),piece(3,'b','w'),\
            piece(3,'k','w'), piece(5,'r','w')]]
        self.turn=0 #every time turn=1 
        self.blackIndexes={"r1":[0,0],"r2":[0,7],"b1":[0,2],"b2":[0,5],"k2":[0,3],"k2":[0,4],"K":[0,5],"q":[0,4],\
            "p1":[1,0],"p2":[1,1],"p3":[1,2],"p4":[1,3],"p5":[1,4],"p6":[1,5],"p7":[1,6],"p8":[1,7]}
        self.whiteIndexes={"r1":[7,0],"r2":[7,7],"b1":[7,2],"b2":[7,5],"k2":[7,3],"k2":[7,4],"K":[7,5],"q":[7,4],\
            "p1":[6,0],"p2":[6,1],"p3":[6,2],"p4":[6,3],"p5":[6,4],"p6":[6,5],"p7":[1,6],"p8":[1,7]}
        self.blackIToP={[0,0]:"r1",[0,7]:"r2",[0,2]:"b1",[0,5]:"b2",[0,3]:"k2",[0,4]:"k2",[0,5]:"K",[0,4]:"q",\
            [1,0]:"p1",[1,1]:"p2",[1,2]:"p3",[1,3]:"p4",[1,4]:"p5",[1,5]:"p6",[1,6]:"p7",[1,7]:"p8"}
        self.whiteIToP={[0,0]:"r1",[0,7]:"r2",[0,2]:"b1",[0,5]:"b2",[0,3]:"k2",[0,4]:"k2",[0,5]:"K",[0,4]:"q",\
            [1,0]:"p1",[1,1]:"p2",[1,2]:"p3",[1,3]:"p4",[1,4]:"p5",[1,5]:"p6",[1,6]:"p7",[1,7]:"p8"}
        self.blackPoints=38
        self.whitePoints=38
        self.advantage=0
        self.whitePieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.blackPieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.whiteaVailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[],"K":[], "q":[], "k1":[], "p1":[]\
            ,"p2":[],"p3":[],"p4":[],"p5":[],"p6":[],"p7":[],"p8":[]}
        self.blackAvailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[],"K":[], "q":[], "k1":[], "p1":[]\
            ,"p2":[],"p3":[],"p4":[],"p5":[],"p6":[],"p7":[],"p8":[]}
        self.wHasSkipped=[False,False,False,False,False,False,False,False,False]
        self.bHasSkipped=[False,False,False,False,False,False,False,False,False]
        self.wHasMovedKing=False
        self.wHasMovedR1=False
        self.wHasMovedR2=False
        self.bHasMovedKing=False
        self.bHasMovedR1=False
        self.bHasMovedR2=False
    def generateAvailableMoves(self, row:int, col:int): 
            availableCol=[]
            availableMoves=[availableCol]
            if self.fullBoard[row][col].type=='p':
                if self.fullBoard[row][col].team=='w':
                    if self.fullBoard[row+1][col+1].team!=self.fullBoard[row][col].team&\
                    self.fullBoard[row+1][col-1].team!='n':
                        availableMoves.append([row+1,col+1])
                    if self.fullBoard[row+1,col-1].team!=self.fullBoard[row][col].team&\
                        self.fullBoard[row+1][col-1].team!='n':
                        availableMoves.append([row+1,col+1])
                    if self.fullBoard[row+1][col].type=='n':
                        availableMoves.append([row+1,col])
                        if self.fullBoard[row+2][col].type=='n'&row==1: 
                            availableMoves.append([row+2,col])
                if self.fullBoard[row][col].team=='b': 
                    if self.fullBoard[row-1][col+1].team!=self.fullBoard[row][col].team&\
                    self.fullBoard[row-1][col-1].team!='n':
                        availableMoves.append([row-1,col+1])
                    if self.fullBoard[row-1,col-1].team!=self.fullBoard[row][col].team&\
                        self.fullBoard[row-1][col-1].team!='n':
                        availableMoves.append([row-1,col+1])
                    if self.fullBoard[row-1][col].type=='n':
                        availableMoves.append([row-1,col])
                        if self.fullBoard[row-2][col].type=='n'&row==6: 
                            availableMoves.append([row+2,col])
                if self.fullBoard[row][col+1].type=='p'&col==3&self.fullBoard[row][col].team=='b'&self.fullBoard[row][col].team=='w': 
                    availableMoves.append([row-1,col+1])
                if self.fullBoard[row][col-1].type=='p'&col==3&self.fullBoard[row][col].team=='b'&self.fullBoard[row][col].team=='w': 
                    availableMoves.append([row-1,col-1])
                if self.fullBoard[row][col+1].type=='p'&col==3&self.fullBoard[row][col].team=='w'&self.fullBoard[row][col].team=='b': 
                    availableMoves.append([row+1,col+1])
                if self.fullBoard[row][col-1].type=='p'&col==4&self.fullBoard[row][col].team=='w'&self.fullBoard[row][col].team=='b': 
                    availableMoves.append([row+1,col-1])
                return availableMoves
            elif self.fullBoard[row][col].type=='k':
                if self.fullBoard[row+2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col+1]!=None:
                    availableMoves.append([row+2,col+1])
                if self.fullBoard[row+1][col+2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+1][col+2]!=None:
                    availableMoves.append([row+1,col+2])
                if self.fullBoard[row-2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-2][col+1]!=None:
                    availableMoves.append([row-2,col+1])
                if self.fullBoard[row+2][col-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col-1]!=None:
                    availableMoves.append([row+2,col-1])
                if self.fullBoard[row-2][col-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-2][col-1]!=None:
                    availableMoves.append([row-2,col-1])
                if self.fullBoard[row+1][col-2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+1][col-2]!=None:
                    availableMoves.append([row+1,col-2])
                if self.fullBoard[row-1][col+2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-1][col+2]!=None:
                    availableMoves.append([row-1,col+2])
                if self.fullBoard[row+2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col+1]!=None:
                    availableMoves.append([row+2,col+1])
                return availableMoves
            elif self.fullBoard[row][col].type=='b':
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2+1]!=None:
                        availableMoves.append([temp1+1,temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2+1]!=None:
                        availableMoves.append([temp1+1,temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2-1]!=None:
                        availableMoves.append([temp1+1,temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2-1]!=None:
                        availableMoves.append([temp1+1,temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2-=1
                return availableMoves
            elif self.fullBoard[row][col].type=='r':
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2]!=None:
                    availableMoves.append([temp1+1,temp2])
                    if self.fullBoard[temp1+1][temp2].team!='n':
                        break
                    temp1+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append([temp1-1,temp2])
                    if self.fullBoard[temp1-1][temp2].team!='n':
                        break
                    temp1-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append([temp1,temp2+1])
                    if self.fullBoard[temp1+1][temp2+1].team!='n':
                        break
                    temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2-1]!=None:
                    availableMoves.append([temp1,temp2-1])
                    if self.fullBoard[temp1+1][temp2-1].team!='n':
                        break
                    temp2-=1
                return availableMoves
            elif self.fullBoard[row][col].type=='q':
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2]!=None:
                    availableMoves.append([temp1+1,temp2])
                    if self.fullBoard[temp1+1][temp2].team!='n':
                        break
                    temp1+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append([temp1-1][temp2])
                    if self.fullBoard[temp1-1][temp2].team!='n':
                        break
                    temp1-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append([temp1,temp2+1])
                    if self.fullBoard[temp1+1][temp2+1].team!='n':
                        break
                    temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2-1]!=None:
                    availableMoves.append([temp1,temp2-1])
                    if self.fullBoard[temp1+1][temp2-1].team!='n':
                        break
                    temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2+1]!=None:
                        availableMoves.append([temp1+1][temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2+1]!=None:
                        availableMoves.append([temp1+1][temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2-1]!=None:
                        availableMoves.append([temp1+1][temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2-1]!=None:
                        availableMoves.append([temp1+1][temp2+1])
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2-=1
                return availableMoves
            elif self.fullBoard[row][col]=='K':
                temp1=row
                temp2=col
                if self.fullBoard[temp1+1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2]!=None:
                    availableMoves.append([temp1+1,temp2])
                if self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append([temp1-1,temp2])
                if self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append([temp1,temp2+1])
                if self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append([temp1,temp2+1])
                if self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2+1]!=None:
                    availableMoves.append([temp1+1,temp2+1])
                if self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2+1]!=None:
                    availableMoves.append([temp1-1,temp2+1])
                if self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2+1]!=None:
                    availableMoves.append([temp1-1,temp2+1])
                if self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2-1]!=None:
                    availableMoves.append([temp1-1,temp2-1])
            else:
                return 
    def inCheck(self)->bool:
        if self.turn%2==0: #if it's white's turn 
            for i in range(self.blackPieces): 
                temp=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]][0][1])
                for j in range(temp): 
                    if self.fullBoard[temp[j][0]][temp[j][1]].type=='K':
                        return True
            return False 
        else: 
            for i in range(self.whitePieces): #if it's black's turn. 
                temp=self.generateAvailableMoves(self.whiteIndexes[self.blackPieces[i]][0][1])
                for j in range(temp): 
                    if self.fullBoard[temp[j][0]][temp[j][1]].type=='K':
                        return True
            return False 
    def move(self, index:int, availableMoveNum:int): 
        oldBoard=self.fullBoard.copy()
        if self.turn%2==0: #if it's white's turn. 
            initialCoords=self.whiteIndexes[self.whitePieces[index]]
            newIndexes=self.generateAvailableMoves(initialCoords[0],initialCoords[1])[availableMoveNum]
            oldpoints=self.fullBoard[newIndexes[0]][newIndexes[1]].val
            oldPiece=""
            if oldpoints>0:
                oldPiece.append(self.blackIToP[newIndexes])
            self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[initialCoords[0]][initialCoords[1]]
            if self.inCheck()==True:
                self.fullBoard=oldBoard
                self.whiteaVailableMoves[self.whitePieces[index]].remove([newIndexes])
                return 
            if self.fullBoard[newIndexes[0]][newIndexes[1]].type=='p'&newIndexes[0]==0:#pawn to queen
                self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(9,'q','w')
                self.whitePoints+=8
            self.blackPoints-=oldpoints
            self.turn+=1
            self.blackPieces.remove(oldPiece)
            self.blackIndexes[newIndexes]=None
            self.blackIToP[newIndexes]=None
            self.whiteIndexes[self.whitePieces[index]]=newIndexes
            self.whiteIToP[newIndexes]=self.whitePieces[index]
            self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(0,'n','n')
            if oldPiece=="p1"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[0]==True
            if oldPiece=="p2"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[1]==True
            if oldPiece=="p3"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[2]==True
            if oldPiece=="p4"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[3]==True
            if oldPiece=="p5"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[4]==True
            if oldPiece=="p6"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[5]==True
            if oldPiece=="p7"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[6]==True
            if oldPiece=="p8"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[7]==True
        else: 
            initialCoords=self.blackIndexes[self.blackPieces[index]]
            newIndexes=self.generateAvailableMoves(initialCoords[0],initialCoords[1])[availableMoveNum]
            oldpoints=self.fullBoard[newIndexes[0]][newIndexes[1]].val
            oldPiece=""
            if oldpoints>0:
                oldPiece.append(self.whiteIToP[newIndexes])
            self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[initialCoords[0]][initialCoords[1]]
            if self.inCheck()==True:
                self.fullBoard=oldBoard
                self.blackAvailableMoves[self.whitePieces[index]].remove([newIndexes])
                return 
            if self.fullBoard[newIndexes[0]][newIndexes[1]].type=='p'&newIndexes[0]==0:#pawn to queen
                self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(9,'q','w')
                self.blackPoints+=8
            if initialCoords==[7][4]:
                self.wHasMovedKing==True
            if initialCoords==[7][0]:
                self.wHasMovedR1==True
            if initialCoords==[7][7]:
                self.wHasMovedR1==True
            if initialCoords==[0][4]:
                self.bHasMovedKing==True
            if initialCoords==[0][0]:
                self.bHasMovedR1==True
            if initialCoords==[0][7]:
                self.bHasMovedR1==True
            self.whitePoints-=oldpoints
            self.turn+=1
            self.whitePieces.remove(oldPiece)
            self.whiteIndexes[newIndexes]=None
            self.whiteIToP[newIndexes]=None
            self.blackIndexes[self.whitePieces[index]]=newIndexes
            self.blackIToP[newIndexes]=self.whitePieces[index]
            self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(0,'n','n')
            if availableMoveNum[index]==[9,9]:
                self.fullBoard[7,]

    def canKSCastle(self):
        if self.turn%2==0&self.wHasMovedKing==False&self.wHasMovedR2==False&self.fullBoard[7][6]==piece(0,'n','n')\
            &self.fullBoard[7][5]==piece(0,'n','n'): 
            for i in range(len(self.blackPieces)):
                temp=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]])
                for j in range(temp): 
                    if temp[i]==[7,7]|temp[i]==[7,4]|temp[i]==[7,6]|temp[i]==[7,8]:
                        return
            self.canKSCastle==True
            self.whiteaVailableMoves["K"].append([9,9])
        if self.turn%2==1&self.bHasMovedKing==False&self.bHasMovedR2==False&self.fullBoard[0][6]==piece(0,'n','n')\
            &self.fullBoard[0][5]==piece(0,'n','n'): 
                for i in range(len(self.whitePieces)):
                    temp=self.generateAvailableMoves(self.whiteIndexes[self.blackPieces[i]])
                    for j in range(temp): 
                        if temp[i]==[0,7]|temp[i]==[0,4]|temp[i]==[7,6]|temp[i]==[7,8]:
                            return
                self.canKSCastle==True
                self.blackAvailableMoves["K"].append([9,9])
    def canQSCastle(self): 
            if self.turn%2==0&self.wHasMovedKing==False&self.wHasMovedR1==False&self.fullBoard[7][6]==piece(0,'n','n')\
            &self.fullBoard[7][5]==piece(0,'n','n'): 
                for i in range(len(self.blackPieces)):
                    temp=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]])
                    for j in range(temp): 
                        if temp[i]==[7,3]|temp[i]==[7,4]|temp[i]==[7,2]|temp[i]==[7,1]|temp[i]==[7,0]:
                            return 
                self.canQSCastle==True
                self.whiteaVailableMoves["K"].append([10,10])
                return 
            if self.turn%2==1&self.bHasMovedKing==False&self.bHasMovedR1==False&self.fullBoard[0][6]==piece(0,'n','n')\
            &self.fullBoard[0][5]==piece(0,'n','n'): 
                for i in range(len(self.blackPieces)):
                    temp=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]])
                    for j in range(temp): 
                        if temp[i]==[0,3]|temp[i]==[0,4]|temp[i]==[0,2]|temp[i]==[0,1]|temp[i]==[0,0]:
                            return False
                self.canQSCastle==True
                self.blackAvailableMoves["K"].append([10,10])
                return True
            return False
    