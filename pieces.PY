from curses import COLORS
import matplotlib as plt
from tkinter import CHAR
from xmlrpc.client import boolean
import numpy 

class piece:
    def __init__(self, val:int, type:CHAR, team:CHAR): 
        self.val=val
        self.type=type
        self.team=team
        
class board:
    def __init_subclass__(self, cls):
        self=cls
    def __init__(self):
        self.AITeam=""#determined in the main
        self.fullBoard=numpy.array([[piece(500,'r','b'),piece(300,'k','b'),piece(300,'b','b'),piece(900,'q','b'),piece(0, 'K', 'b'),piece(300,'b','b'),\
            piece(300,'k','b'), piece(500,'r','b')], [piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),\
            piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b')],[piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),\
            piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')],\
            [piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w'),\
            piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w')],
            [piece(500,'r','w'),piece(300,'k','w'),piece(300,'b','w'),piece(900,'q','w'),piece(0, 'K', 'w'),piece(300,'b','w'),\
            piece(300,'k','w'), piece(500,'r','w')]])
        self.turn=0 #every time turn=1 
        self.blackIndexes={"r1":numpy.array([0,0]),"r2":[0,7],"b1":numpy.array([0,2]),"b2":numpy.array([0,5]),"k2":numpy.array([0,1]),"k2":numpy.array([0,6]),"K":numpy.array([0,4]),"q":numpy.array([0,3]),\
            "p1":numpy.array([1,0]),"p2":numpy.array([1,1]),"p3":numpy.array([1,2]),"p4":numpy.array([1,3]),"p5":numpy.array([1,4]),"p6":numpy.array([1,5]),"p7":numpy.array([1,6]),"p8":numpy.array([1,7])}
        self.whiteIndexes={"r1":numpy.array([7,0]),"r2":numpy.array([7,7]),"b1":numpy.array([7,2]),"b2":numpy.array([7,5]),"k2":numpy.array([7,3]),"k2":numpy.array([7,4]),"K":numpy.array([7,5]),"q":numpy.array([7,4]),\
            "p1":numpy.array([6,0]),"p2":numpy.array([6,1]),"p3":numpy.array([6,2]),"p4":numpy.array([6,3]),"p5":numpy.array([6,4]),"p6":numpy.array([6,5]),"p7":numpy.array([1,6]),"p8":numpy.array([1,7])}
        self.blackIToP={0:"r1",7:"r2",5:"b1",5:"b2",1:"k1",6:"k2",4:"K",3:"q",\
            10:"p1",11:"p2",12:"p3",13:"p4",14:"p5",15:"p6",16:"p7",17:"p8"}
        self.whiteIToP={70:"r1",77:"r2",72:"b1",55:"b2",71:"k2",76:"k2",71:"K",73:"q",\
            60:"p1",61:"p2",62:"p3",63:"p4",64:"p5",65:"p6",66:"p7",67:"p8"}
        self.blackPoints=380
        self.whitePoints=380
        self.advantage=0
        self.whitePieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.blackPieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.whiteaVailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[[2,7],[2,5]],"K":[], "q":[], "k1":[[2,0],[2,2]], "p1":[[0,5],[0,4]]\
            ,"p2":[[1,5],[1,4]],"p3":[[2,5],[2,4]],"p4":[[3,5],[3,4]],"p5":[[4,5],[4,4]],"p6":[[5,5],[5,4]],"p7":[[6,5],[6,4]],"p8":[[7,5],[7,4]]}
        self.blackAvailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[[2,7],[2,5]],"K":[], "q":[], "k1":[[2,0],[2,2]], "p1":[[0,3],[0,4]]\
            ,"p2":[[1,3],[1,4]],"p3":[[2,3],[2,4]],"p4":[[3,3],[3,4]],"p5":[[4,3],[4,4]],"p6":[[5,3],[5,4]],"p7":[[6,3],[6,4]],"p8":[[7,3],[7,4]]}
        self.wHasSkipped=[False,False,False,False,False,False,False,False,False]
        self.bHasSkipped=[False,False,False,False,False,False,False,False,False]
        self.wHasMovedKing=False
        self.wHasMovedR1=False
        self.wHasMovedR2=False
        self.bHasMovedKing=False
        self.bHasMovedR1=False
        self.bHasMovedR2=False
        self.calledMove=[False,False,False,False,False,False,False,False,False,False,False,False,\
            False,False,False]
        

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
        self.calledMove[index]==True
        oldBoard=self.fullBoard.copy()
        if self.turn%2==0: #if it's white's turn. 
            initialCoords=self.whiteIndexes[self.whitePieces[index]]
            newIndexes=self.whiteaVailableMoves[self.whitePieces[index]]
            if newIndexes==[9,9]: #king side castle
                self.fullBoard[7][4]=piece(0,'n','n')
                self.fullBoard[7][7]=piece(0,'n','n')
                self.fullBoard[7][6]=piece(0,'K','w')
                self.fullBoard[7][5]=piece(5, 'r', 'w')
                return 
            if newIndexes==[10,10]: 
                self.fullBoard[7][4]=piece(0,'n','n')
                self.fullBoard[7][3]=piece(5,'r','w')
                self.fullBoard[7][2]=piece(0,'K', 'w')
                self.fullBoard[7][0]=piece(0,'n','n')
                self.fullBoard[7][1]=piece(0,'n','n')
                return 
            wOldPiece=self.whiteIndexes[0]
            oldpoints=self.fullBoard[newIndexes[0]][newIndexes[1]].val
            boldPiece=""
            if oldpoints>0:
                boldPiece=self.blackIToP[newIndexes]
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
            if oldpoints>0:
                self.blackPieces.remove(boldPiece)
            self.blackIndexes[newIndexes]=None
            self.blackIToP[newIndexes]=None
            self.whiteIndexes[self.whitePieces[index]]=newIndexes
            self.whiteIToP[newIndexes]=self.whitePieces[index]
            self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(0,'n','n')
            if wOldPiece=="p1"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[0]==True
            if wOldPiece=="p2"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[1]==True
            if wOldPiece=="p3"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[2]==True
            if wOldPiece=="p4"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[3]==True
            if wOldPiece=="p5"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[4]==True
            if wOldPiece=="p6"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[5]==True
            if wOldPiece=="p7"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[6]==True
            if wOldPiece=="p8"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[7]==True
        else: 
            initialCoords=self.blackIndexes[self.blackPieces[index]]
            newIndexes=self.generateAvailableMoves(initialCoords[0],initialCoords[1])[availableMoveNum]
            oldpoints=self.fullBoard[newIndexes[0]][newIndexes[1]].val
            oldPiece=""
            if oldpoints>0:
                oldPiece=self.whiteIToP[newIndexes[0]*10+newIndexes[1]*10]
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
            if oldpoints>0:
                self.whitePieces.remove(oldPiece)
                self.whiteIToP[newIndexes[0]*10+newIndexes[1]]=None
            self.whiteIndexes[newIndexes]=None
            self.blackIndexes[self.whitePieces[index]]=newIndexes
            self.blackIToP[newIndexes[0]*10+newIndexes[1]]=self.blackPieces[index]
            self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(0,'n','n')
            if wOldPiece=="p1"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[0]==True
            if wOldPiece=="p2"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[1]==True
            if wOldPiece=="p3"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[2]==True
            if wOldPiece=="p4"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[3]==True
            if wOldPiece=="p5"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[4]==True
            if wOldPiece=="p6"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[5]==True
            if wOldPiece=="p7"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[6]==True
            if wOldPiece=="p8"&newIndexes[0]-initialCoords[0]==2: 
                self.wHasSkipped[7]==True
            
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
    def otherTeamTurnCheck(self)->bool:
        self.turn+=1
        if self.inCheck()==True: 
            self.turn-=1
            return True
        else: 
            self.turn-=1
            return False
    def printBoard(self): 
        for i in range(8): 
            print(self.fullBoard[i][0].type, self.fullBoard[i][1].type, self.fullBoard[i][2].type, self.fullBoard[i][3].type,self.fullBoard[i][4].type, self.fullBoard[i][5].type, self.fullBoard[i][6].type, self.fullBoard[i][7].type)
    def AIadvantageEval(self):#called to search through boards
            if self.AITeam=="b":
                self.advantage=self.blackPoints-self.whitePoints#basic points comparison IE queen=9 
                for i in range(len(self.whitePieces)): 
                    oldIndexes=self.whiteIndexes[self.whiteIndexes[i]]
                    if oldIndexes==[3][3]|oldIndexes==[4][3]|oldIndexes==[3][4]|oldIndexes==[4][4]:

                    for j in range(len(self.whiteaVailableMoves[self.whiteIndexes[i]])): 
                        newIndexes=self.whiteIndexes[self.whitePieces[i]][j]#if a pawn is attacking a queen, that would be an advantage of 7
                        if self.fullBoard[newIndexes[0]][newIndexes[1]].value>self.fullBoard[oldIndexes[0]][oldIndexes[1]].value: 
                            self.advantage+=self.fullBoard[newIndexes[0]][newIndexes[1]].value-self.fullBoard[oldIndexes[0]][oldIndexes[1]].value

                if self.turn<32:#early game
    def playerMoveCheck(self):#this takes out the moves that put the player in check 
        #in the main, the generate moves function will be called then this one 
        oldBoard=self.fullBoard
        if self.turn%2==0: 
            for i in range(len(self.whitePieces)):
                for j in range(len(self.generateAvailableMoves(self.whiteIndexes[self.whitePieces[i]],\
                    ))):
                    self.fullBoard[self.whiteaVailableMoves][j][0]\
                        [self.whiteaVailableMoves[self.whitePieces[i]]][j][1]=self.fullBoard[self.whiteIndexes[self.whitePieces[i]][0]]\
                            [self.whiteIndexes[self.whitePieces[i]][1]]
                    self.fullBoard[self.whiteIndexes[self.whitePieces[i]][0]][self.whiteIndexes[self.whitePieces[i]][1]]
                    if self.inCheck()==True:
                        self.whiteaVailableMoves[self.whitePieces[i]].remove()
                    self.fullBoard=oldBoard
        else: 
            for i in range(len(self.blackPieces)):
                for j in range(len(self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]],\
                    ))):
                    self.fullBoard[self.blackAvailableMoves][j][0]\
                        [self.blackAvailableMoves[self.blackPieces[i]]][j][1]=self.fullBoard[self.blackIndexes[self.blackPieces[i]][0]]\
                            [self.blackIndexes[self.blackPieces[i]][1]]
                    self.fullBoard[self.blackIndexes[self.blackPieces[i]][0]][self.blackIndexes[self.blackPieces[i]][1]]
                    if self.inCheck()==True:
                        self.blackAvailableMoves[self.blackPieces[i]].remove()
                    self.fullBoard=oldBoard
    
def boardTo1D(game:board):
    re=[]
    for i in len(game.fullBoard):
        for j in len(game.fullBoard[i]):
            re.append(game.fullBoard[i][j].type)
    return re
def graphics(fullBoard: list[list[CHAR]]): 

game=board()   
board.printBoard(game)
import sys

print("What team would you like to play as, w or b?")
team=""
while team!="w"|team!="b": 
    team=sys.stdin.readline()
    if team!="w"|team!="b": 
        print("Please input a valid team.")

def playerMove(): 
    validMove=False
    if team=="w":
        while validMove==False:
            indexes={"a":0, "b":1, "c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
            print("What is the piece you want to move? example: a4")
            thePieceCol=sys.stdin.readline()
            c=indexes[thePieceCol]
            thePieceRow=sys.stdin.readline()
            r=int(thePieceRow)-1
            if game.whiteIToP[r*10+c]!=None:
                print("What is the new poisition?")
                thePieceC=sys.stdin.readline()
                newc=indexes[thePieceC]
                thePieceR=sys.stdin.readline()
                newr=int(thePieceR)-1
                game.generateAvailableMoves(r,c)
                game.canKSCastle()
                game.canQSCastle()
                if [newr, newc] in game.whiteaVailableMoves[game.whiteIToP[r*10+c]]:
                    game.move(game.whitePieces.index(game.whiteIToP[r*10+c]), game.whiteaVailableMoves.index(game.whiteIToP[r*10+c]))
                    validMove=True

        
        

    