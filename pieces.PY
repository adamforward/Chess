from tkinter import CHAR
from xmlrpc.client import boolean
import copy 
import sys
#I am currently looking into using matrix operations to improve efficiency, particularly within the generate available moves function and repetetive iterations within functions such as in check.  
#I currently have all the functions I need to run a game with relatively little code, still have to debug though.  
# #when I get the game up and running, I will probably make some modifications to the "AIAdvantageEval" function
class piece:
    def __init__(self, val:int, type:CHAR, team:CHAR): 
        self.val=val
        self.type=type
        self.team=team
        def copy(self):
            newPiece=piece(self.val, self.type, self.team)
            return newPiece
class board:
    def __init_subclass__(self, cls):
        self=cls
    def __init__(self):
        self.inCheckStored=False
        self.AIteam=""
        self.gameState=0
        self.fullBoard=([piece(500,'r','b'),piece(300,'k','b'),piece(300,'b','b'),piece(900,'q','b'),piece(0, 'K', 'b'),piece(300,'b','b'),\
            piece(300,'k','b'), piece(500,'r','b')], [piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),\
            piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b')],[piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),\
            piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),],\
            [piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')],\
            [piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w'),\
            piece(100,'p','w'),piece(100,'p','w'),piece(100,'p','w')],\
            [piece(500,'r','w'),piece(300,'k','w'),piece(300,'b','w'),piece(900,'q','w'),piece(0, 'K', 'w'),piece(300,'b','w'),\
            piece(300,'k','w'), piece(500,'r','w')])
        self.turn=0 #every time turn=1 
        self.blackIndexes={"r1":(0,0),"r2":(0,7),"b1":(0,2),"b2":(0,5),"k2":(0,3),"k2":(0,6),"K":(0,4),"q":(0,3),\
            "p1":(1,0),"p2":(1,1),"p3":(1,2),"p4":(1,3),"p5":(1,4),"p6":(1,5),"p7":(1,6),"p8":(1,7)}
        self.whiteIndexes={"r1":(7,0),"r2":(7,7),"b1":(7,2),"b2":(7,5),"k2":(7,3),"k2":(7,4),"K":(7,5),"q":(7,4),\
            "p1":(6,0),"p2":(6,1),"p3":(6,2),"p4":y(6,3),"p5":(6,4),"p6":(6,5),"p7":(1,6),"p8":(1,7)}
        self.blackIToP={0:"r1",7:"r2",5:"b1",5:"b2",1:"k1",6:"k2",4:"K",3:"q",\
            10:"p1",11:"p2",12:"p3",13:"p4",14:"p5",15:"p6",16:"p7",17:"p8"}
        self.whiteIToP={70:"r1",77:"r2",72:"b1",55:"b2",71:"k2",76:"k2",74:"K",73:"q",\
            60:"p1",61:"p2",62:"p3",63:"p4",64:"p5",65:"p6",66:"p7",67:"p8"}
        self.blackPoints=3800
        self.whitePoints=3800
        self.advantage=0
        self.whitePieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.blackPieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.whiteaVailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[(5,7),(5,5)],"K":[], "q":[], "k1":[(5,0),(5,2)], "p1":[(5,0),(6,0)]\
            ,"p2":[(5,1),(6,1)],"p3":[(5,2),(6,2)],"p4":[(5,3),(6,3)],"p5":[(5,4),(6,4)],"p6":[(5,5),(6,6)],"p7":[(5,6),(6,6)],"p8":[(5,7),(6,7)]}
        self.blackAvailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[(2,5),(2,7)],"K":[], "q":[], "k1":[(2,0),(2,2)], "p1":[(2,0),(3,0)]\
            ,"p2":[(1,2), (1,3)],"p3":[(2,2),(2,3)],"p4":[(2,3),(3,3)],"p5":[(5,4),(3,4)],"p6":[(2,5),(3,5)],"p7":[(2,6),(3,6)],"p8":[(2,7),(7,3)]}
        self.wHasSkipped=(False,False,False,False,False,False,False,False,False)
        self.bHasSkipped=(False,False,False,False,False,False,False,False,False)#this info is stored for en pessant captures.
        self.wHasMovedKing=False
        self.wHasMovedR1=False
        self.wHasMovedR2=False
        self.bHasMovedKing=False
        self.bHasMovedR1=False
        self.bHasMovedR2=False
    def deepClone(self):#will need to do this once for AI to work.
        newB=board()
        newB.AIteam=self.AIteam
        newB.AIteam=self.AIteam
        newB.advantage=self.advantage
        newB.turn=self.turn
        newB.bHasMovedKing=self.bHasMovedKing
        newB.AIteam=self.AIteam
        newB.blackIndexes=copy.deepcopy(self.blackIndexes)
        newB.blackIToP=copy.deepcopy(self.blackIToP)
        newB.blackPoints=self.blackPoints
        newB.gameState=self.gameState
        newB.bHasMovedR1=self.bHasMovedR1
        newB.bHasMovedR2=self.bHasMovedR2
        newB.bHasMovedKing=self.bHasMovedKing
        newB.blackAvailableMoves=copy.deepcopy(self.blackAvailableMoves)
        newB.wHasMovedKing=self.wHasMovedKing
        newB.wHasMovedR1=self.wHasMovedR1
        newB.wHasMovedR2=self.wHasMovedR2
        newB.wHasSkipped=copy.deepcopy(self.wHasSkipped)
        newB.whiteaVailableMoves=copy.deepcopy(self.whiteaVailableMoves)
        newB.whiteIndexes=copy.deepcopy(self.whiteIndexes)
        newB.whiteIToP=copy.deepcopy(self.whiteIToP)
        newB.whitePieces=copy.deepcopy(self.whitePieces)
        newB.whitePoints=self.whitePoints
        return newB
    def getPlayerMove(self): 
        while self.AIteam!="w"|self.AIteam!="b":
            print("w or b?")
            self.AIteam=input()#Eventually, I will get the graphics going so that it will be 
        
    def generateAvailableMoves(self, row:int, col:int): #generates available moves for any piece on the board, takes old indexes as arguements, edits the field 
        #of available moves map 
            availableCol=[]
            availableMoves=[availableCol]
            if self.fullBoard[row][col].type=='p':
                if self.fullBoard[row][col].team=='b':#white and black move
                    if self.fullBoard[row+1][col+1].team!=self.fullBoard[row][col].team&\
                    self.fullBoard[row+1][col-1].team!='n':
                        availableMoves.append((row+1,col+1))#this function I could make changes to using numpy arrays and matrix operations.
                    if self.fullBoard[row+1,col-1].team!=self.fullBoard[row][col].team&\
                        self.fullBoard[row+1][col-1].team!='n':
                            availableMoves.append((row+1,col+1))
                    if self.fullBoard[row+1][col].type=='n':
                        availableMoves.append((row+1,col))
                        if self.fullBoard[row+2][col].type=='n'&row==1: 
                            availableMoves.append((row+2,col))
                if self.fullBoard[row][col].team=='w': 
                    if self.fullBoard[row-1][col+1].team!=self.fullBoard[row][col].team&\
                    self.fullBoard[row-1][col-1].team!='n':
                        availableMoves.append((row-1,col+1))
                    if self.fullBoard[row-1,col-1].team!=self.fullBoard[row][col].team&\
                        self.fullBoard[row-1][col-1].team!='n':
                        availableMoves.append((row-1,col+1))
                    if self.fullBoard[row-1][col].type=='n':
                        availableMoves.append((row-1,col))
                        if self.fullBoard[row-2][col].type=='n'&row==6: 
                            availableMoves.append((row+2,col))
                if self.fullBoard[row][col+1].type=='p'&col==3&self.fullBoard[row][col].team=='b'&self.fullBoard[row][col].team=='w': 
                    availableMoves.append((row-1,col+1))
                if self.fullBoard[row][col-1].type=='p'&col==3&self.fullBoard[row][col].team=='b'&self.fullBoard[row][col].team=='w': 
                    availableMoves.append((row-1,col-1))
                if self.fullBoard[row][col+1].type=='p'&col==3&self.fullBoard[row][col].team=='w'&self.fullBoard[row][col].team=='b': 
                    availableMoves.append((row+1,col+1))
                if self.fullBoard[row][col-1].type=='p'&col==4&self.fullBoard[row][col].team=='w'&self.fullBoard[row][col].team=='b': 
                    availableMoves.append((row+1,col-1))
                return availableMoves
            elif self.fullBoard[row][col].type=='k':
                if self.fullBoard[row+2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col+1]!=None:
                    availableMoves.append((row+2,col+1))
                if self.fullBoard[row+1][col+2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+1][col+2]!=None:
                    availableMoves.append((row+1,col+2))
                if self.fullBoard[row-2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-2][col+1]!=None:
                    availableMoves.append((row-2,col+1))
                if self.fullBoard[row+2][col-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col-1]!=None:
                    availableMoves.append((row+2,col-1))
                if self.fullBoard[row-2][col-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-2][col-1]!=None:
                    availableMoves.append(np.array(row-2,col-1))
                if self.fullBoard[row+1][col-2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+1][col-2]!=None:
                    availableMoves.append((row+1,col-2))
                if self.fullBoard[row-1][col+2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-1][col+2]!=None:
                    availableMoves.append((row-1,col+2))
                if self.fullBoard[row+2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col+1]!=None:
                    availableMoves.append((row+2,col+1))
                return availableMoves
            elif self.fullBoard[row][col].type=='b':
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2+1]!=None:
                        availableMoves.append((temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2+1]!=None:
                        availableMoves.append(([temp1+1,temp2+1]))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2-1]!=None:
                        availableMoves.append(([temp1+1,temp2+1]))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2-1]!=None:
                        availableMoves.append((temp1+1,temp2+1))
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
                    availableMoves.append((temp1+1,temp2))
                    if self.fullBoard[temp1+1][temp2].team!='n':
                        break
                    temp1+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append((temp1-1,temp2))
                    if self.fullBoard[temp1-1][temp2].team!='n':
                        break
                    temp1-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append((temp1,temp2+1))
                    if self.fullBoard[temp1+1][temp2+1].team!='n':
                        break
                    temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2-1]!=None:
                    availableMoves.append((temp1,temp2-1))
                    if self.fullBoard[temp1+1][temp2-1].team!='n':
                        break
                    temp2-=1
                return availableMoves
            elif self.fullBoard[row][col].type=='q':
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2]!=None:
                    availableMoves.append((temp1+1,temp2))
                    if self.fullBoard[temp1+1][temp2].team!='n':
                        break
                    temp1+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append((temp1-1,temp2))
                    if self.fullBoard[temp1-1][temp2].team!='n':
                        break
                    temp1-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append((temp1,temp2+1))
                    if self.fullBoard[temp1+1][temp2+1].team!='n':
                        break
                    temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2-1]!=None:
                    availableMoves.append((temp1,temp2-1))
                    if self.fullBoard[temp1+1][temp2-1].team!='n':
                        break
                    temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2+1]!=None:
                        availableMoves.append((temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2+1]!=None:
                        availableMoves.append((temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2-1]!=None:
                        availableMoves.append((temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2-1]!=None:
                        availableMoves.append((temp1+1,temp2+1))
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
                    availableMoves.append((temp1+1,temp2))
                if self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append((temp1-1,temp2))
                if self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append((temp1,temp2+1))
                if self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append((temp1,temp2+1))
                if self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2+1]!=None:
                    availableMoves.append((temp1+1,temp2+1))
                if self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2+1]!=None:
                    availableMoves.append((temp1-1,temp2+1))
                if self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2+1]!=None:
                    availableMoves.append((temp1-1,temp2+1))
                if self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2-1]!=None:
                    availableMoves.append((temp1-1,temp2-1))
            else:
                return 
    def inCheck(self)->bool:
        if self.turn%2==0: #if it's white's turn 
            for i in range(self.blackPieces): 
                temp=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]][0][1])
                for j in range(temp): 
                    if self.fullBoard[temp[j][0]][temp[j][1]].type=='K':
                        self.inCheckStored=True
                        return True
            self.inCheckStored=False#I added this field so that this function would only be called once in the AI advantage method. 
            return False 
        else: 
            for i in range(self.whitePieces): #if it's black's turn. 
                temp=self.generateAvailableMoves(self.whiteIndexes[self.blackPieces[i]][0][1])
                for j in range(temp): 
                    if self.fullBoard[temp[j][0]][temp[j][1]].type=='K':
                        self.inCheckStored=True
                        return True
            self.inCheckStored=False
            return False 
    def AIAdvantageEval(self):#only call this function after all moves have been generated and checked. going to search through a tree of ints for advantage parameter. 
        whiteAdvantage=0
        blackAdvantage=0
        if self.turn>32:
            if self.turn%2==0&self.inCheckStored==True: #late and middle game. 
                blackAdvantage+=50
            if self.turn%2==1&self.inCheckStored==True: 
                whiteAdvantage+=50
        if len(self.whitePieces) + len(self.blackPieces)==2: #2 kings left
            self.gameState+=1#tie game
            self.advantage=0
            return 
        if len(self.blackPieces)==1:#last piece is the black king
            if self.blackIndexes["K"][0]==2|self.blackIndexes["K"][0]==5|self.blackIndexes["K"][1]==2|self.blackIndexes["K"][1]==5:
            #has to be weighted heavily, this is to pushes the king to the edge for checkmate
                whiteAdvantage+=100 
            if self.blackIndexes["K"][0]==1|self.blackIndexes["K"][0]==6|self.blackIndexes["K"][1]==1|self.blackIndexes["K"][1]==6:
                whiteAdvantage+=150
            if self.blackIndexes["K"][0]==0|self.blackIndexes["K"][0]==7|self.blackIndexes["K"][1]==0|self.blackIndexes["K"][1]==7:
                whiteAdvantage+=200
        if self.whitePoints>self.blackPoints+100& len(self.blackPieces)+len(self.whitePieces)<10:
            whiteAdvantage-=(len(self.blackPieces)+len(self.whitePieces))*2#Incentivise trades if AI is up in the lategame 
        noMovesW=True
        noMovesB=True#store these for the checkmate and stalemate conditions
        for i in range(len(self.whitePieces)):#need to go back and make some adjustments to the generate available moves function so that it adds to the field and returns a list. 
            oldIndexes=(self.whiteIndexes[self.whitePieces[i]])
            if self.turn<=32:#define early game as <= 32 moves, enough to move each piece once
                whiteAdvantage+=2*len(self.whiteaVailableMoves[self.whitePieces[i]])#weigh this heavily early game for piece development. 
                if oldIndexes==[3,3]|oldIndexes==[3,4]|oldIndexes==[4,3]|oldIndexes==[4,4]:#favor control of middle of the board in early game.
                    whiteAdvantage+=self.whiteaVailableMoves[self.whitePieces[i]]*5#Moves from middle. 
            if self.turn>=32 & len(self.whitePieces)+len(self.blackPieces)>10:# this is the midgame interval, different weights are applied here. 
                whiteAdvantage+=len(self.whiteaVailableMoves[self.whitePieces[i]])
                if oldIndexes==[3,3]|oldIndexes==[3,4]|oldIndexes==[4,3]|oldIndexes==[4,4]:
                    whiteAdvantage+=len(self.whiteaVailableMoves[self.whitePieces[i]])*8#weigh control of the middle heavier, especially with moves 
                if self.fullBoard[oldIndexes[0]][oldIndexes[1]].type=='p'&oldIndexes[0]<4:#black end is at 0, incentivise pawns to be far up. 
                    whiteAdvantage+=(4-oldIndexes[0])*15
            if len(self.whitePieces+self.blackPieces)<10: #late game advantage for white, different weights on everything. Can search deeper into boards late in the game. 
                whiteAdvantage+=len(self.whiteaVailableMoves[self.whitePieces[i]])
                if self.fullBoard[oldIndexes[0]][oldIndexes[1]].type=='p'&oldIndexes[0]<4:
                    whiteAdvantage+=(4-oldIndexes[0])*30#weigh far up pawns heavier in late game 
                if oldIndexes==[3,3]|oldIndexes==[3,4]|oldIndexes==[4,3]|oldIndexes==[4,4]:
                    whiteAdvantage+=len(self.whiteaVailableMoves[self.whitePieces[i]])#weigh control of the middle light in late game. 
            for j in range(len(self.whiteaVailableMoves(self.whitePieces[i]))):
                if self.whiteaVailableMoves(self.whitePieces[i])!=[]:#if its empty, either checkmate or stalemate.
                    noMovesW=False
                newIndexes=self.whiteaVailableMoves[self.whitePieces[i]][j]
                if self.fullBoard[newIndexes[0]][newIndexes[1]].value>self.fullBoard[oldIndexes[0]][oldIndexes[1]].value:
                    whiteAdvantage+=self.fullBoard[newIndexes[0]][newIndexes[1]].value-self.fullBoard[oldIndexes[0]][oldIndexes[1]].value-100# if pawn attacking queen, 600 point advantage
                if self.turn<=32:#earlygame 
                    if newIndexes==[3,3]|newIndexes==[3,4]|newIndexes==[4,3]|newIndexes==[4,4]:# favor # of moves to the middle of board
                        whiteAdvantage+=5
                    if newIndexes[0]<4: 
                        whiteAdvantage+=4
                if self.turn<=32 & len(self.whitePieces)+len(self.blackPieces)>10:# this is the midgame interval, different weights are applied here. 
                    if newIndexes[0]==4:
                        whiteAdvantage+=2
                    if newIndexes[0]==3:
                        whiteAdvantage+=6
                    if newIndexes[0]==2:#if you're pressuring squares on black's side.
                        whiteAdvantage+=10
                    if newIndexes[0]==1:
                        whiteAdvantage+=14
                    if newIndexes[0]==0: 
                        whiteAdvantage+=18
                    if newIndexes==[3,3]|newIndexes==[3,4]|newIndexes==[4,3]|newIndexes==[4,4]:# favor # of moves to the middle of board
                        whiteAdvantage+=5
                    store1=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    store2=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[oldIndexes[0]][oldIndexes[1]]
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    temp=self.generateAvailableMoves(newIndexes[0],newIndexes[1])
                    if self.blackIndexes["K"] in temp: #more efficient than calling check function, this is number of moves that put king in check.
                        whiteAdvantage+=20
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=store1
                    self.fullBoard[newIndexes[0]][newIndexes[1]]=store2
                if len(self.whitePieces+self.blackPieces)<10: #lateGame advantage
                    store1=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    store2=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[oldIndexes[0]][oldIndexes[1]]
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    temp=self.generateAvailableMoves(newIndexes[0],newIndexes[1])
                    if self.blackIndexes["K"] in temp: 
                        whiteAdvantage+=30# weigh this parameter heavier in late game. 
                        #all these different control of board parameters are far less important in the late game, because the 
                    if newIndexes==[3,3]|newIndexes==[3,4]|newIndexes==[4,3]|newIndexes==[4,4]:# favor # of moves to the middle of board
                        whiteAdvantage+=2
            #exit for loop 
            if noMovesW==True&self.turn%2==0: #either stalemate or checkMate
                if self.inCheckStored==True:
                    blackAdvantage+=1000000
                    whiteAdvantage-=1000000
                    self.gameState+=1
                else: 
                    self.advantage=0
                    self.gameState+=1
                    return
        if len(self.whitePieces)==1:#go through and do same iterations for black 
            if self.whiteIndexes["K"][0]==2|self.whiteIndexes["K"][0]==5|self.whiteIndexes["K"][1]==2|self.whiteIndexes["K"][1]==5:
            #has to be weighted heavily, this is to pushes the king to the edge for checkmate
                blackAdvantage+=100 
            if self.whiteIndexes["K"][0]==1|self.whiteIndexes["K"][0]==6|self.whiteIndexes["K"][1]==1|self.whiteIndexes["K"][1]==6:
                blackAdvantage+=150
            if self.whiteIndexes["K"][0]==0|self.whiteIndexes["K"][0]==7|self.whiteIndexes["K"][1]==0|self.whiteIndexes["K"][1]==7:
                blackAdvantage+=200
            if self.blackPoints>self.whitePoints+100& len(self.whitePieces)+len(self.blackPieces)<10:
                blackAdvantage-=(len(self.blackPieces)+len(self.whitePieces))*2#Incentivise trades if AI is up in the lategame 
            noMovesW=True
            noMovesB=True#store these for the checkmate and stalemate conditions
        for i in range(len(self.blackPieces)):#need to go back and make some adjustments to the generate available moves function so that it adds to the field and returns a list. 
            oldIndexes=(self.blackIndexes[self.blackPieces[i]])
            if self.turn<=32:#define early game as <= 32 moves, enough to move each piece once
                blackAdvantage+=2*len(self.blackAvailableMoves[self.blackPieces[i]])#weigh this heavily early game for piece development. 
                if oldIndexes==[3,3]|oldIndexes==[3,4]|oldIndexes==[4,3]|oldIndexes==[4,4]:#favor control of middle of the board in early game.
                    blackAdvantage+=self.blackAvailableMoves[self.blackPieces[i]]*5#Moves from middle. 
            if self.turn>=32 & len(self.blackPieces)+len(self.whitePieces)>10:# this is the midgame interval, different weights are applied here. 
                blackAdvantage+=len(self.blackAvailableMoves[self.blackPieces[i]])
                if oldIndexes==[3,3]|oldIndexes==[3,4]|oldIndexes==[4,3]|oldIndexes==[4,4]:
                    blackAdvantage+=len(self.blackAvailableMoves[self.blackPieces[i]])*8#weigh control of the middle heavier, especially with moves 
                if self.fullBoard[oldIndexes[0]][oldIndexes[1]].type=='p'&oldIndexes[0]<4:#black end is at 0, incentivise pawns to be far up. 
                    blackAdvantage+=(4-oldIndexes[0])*15
            if len(self.blackPieces+self.whitePieces)<10: #late game advantage for white, different weights on everything. Can search deeper into boards late in the game. 
                blackAdvantage+=len(self.blackAvailableMoves[self.blackPieces[i]])
                if self.fullBoard[oldIndexes[0]][oldIndexes[1]].type=='p'&oldIndexes[0]<4:
                    blackAdvantage+=(4-oldIndexes[0])*30#weigh far up pawns heavier in late game 
                if oldIndexes==[3,3]|oldIndexes==[3,4]|oldIndexes==[4,3]|oldIndexes==[4,4]:
                    blackAdvantage+=len(self.blackAvailableMoves[self.blackPieces[i]])#weigh control of the middle light in late game. 
            for j in range(len(self.blackAvailableMoves(self.blackPieces[i]))):
                if self.blackAvailableMoves(self.blackPieces[i])!=[]:#if its empty, either checkmate or stalemate.
                    noMovesB=False
                newIndexes=self.blackAvailableMoves[self.blackPieces[i]][j]
                if self.fullBoard[newIndexes[0]][newIndexes[1]].value>self.fullBoard[oldIndexes[0]][oldIndexes[1]].value:
                    blackAdvantage+=self.fullBoard[newIndexes[0]][newIndexes[1]].value-self.fullBoard[oldIndexes[0]][oldIndexes[1]].value-100# if pawn attacking queen, 600 point advantage
                if self.turn<=32:#earlygame 
                    if newIndexes==[3,3]|newIndexes==[3,4]|newIndexes==[4,3]|newIndexes==[4,4]:# favor # of moves to the middle of board
                        blackAdvantage+=5
                    if newIndexes[0]<4: 
                        blackAdvantage+=4
                if self.turn<=32 & len(self.blackPieces)+len(self.blackPieces)>10:# this is the midgame interval, different weights are applied here. 
                    if newIndexes[0]==4:
                        blackAdvantage+=2
                    if newIndexes[0]==3:
                        blackAdvantage+=6
                    if newIndexes[0]==2:#if you're pressuring squares on black's side.
                        blackAdvantage+=10
                    if newIndexes[0]==1:
                        blackAdvantage+=14
                    if newIndexes[0]==0: 
                        blackAdvantage+=18
                    if newIndexes==[3,3]|newIndexes==[3,4]|newIndexes==[4,3]|newIndexes==[4,4]:# favor # of moves to the middle of board
                        blackAdvantage+=5
                    store1=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    store2=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[oldIndexes[0]][oldIndexes[1]]
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    temp=self.generateAvailableMoves(newIndexes[0],newIndexes[1])
                    if self.whiteIndexes["K"] in temp: #more efficient than calling check function, this is number of moves that put king in check.
                        blackAdvantage+=20
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=store1
                    self.fullBoard[newIndexes[0]][newIndexes[1]]=store2
                if len(self.whitePieces+self.blackPieces)<10: #lateGame advantage
                    store1=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    store2=piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[oldIndexes[0]][oldIndexes[1]]
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    temp=self.generateAvailableMoves(newIndexes[0],newIndexes[1])
                    if self.whiteIndexes["K"] in temp: 
                        blackAdvantage+=30# weigh this parameter heavier in late game. 
                        #all these different control of board parameters are far less important in the late game, because the 
                    if newIndexes==[3,3]|newIndexes==[3,4]|newIndexes==[4,3]|newIndexes==[4,4]:# favor # of moves to the middle of board
                        blackAdvantage+=2
            #exit for loop 
            if noMovesB==True&self.turn%2==1: #either stalemate or checkMate
                if self.inCheckStored==True:
                    whiteAdvantage+=1000000
                    blackAdvantage-=1000000
                    self.gameState+=1
                else: 
                    self.advantage=0
                    self.gameState+=1
                    return 
            if self.AIteam=="w": 
                self.advantage=whiteAdvantage-blackAdvantage
            else: 
                self.advantage=blackAdvantage-whiteAdvantage
                        #the AI will create a tree of different boards and search for this advantage parameter to decide what move its doing. 

    def printInfo(self): #this is a function that I'll only use for debugging 
        self.printBoard()
        self.allMovesGen()
        print("White:")
        for i in range(self.whitePieces): 
            print(self.whitePieces[i])
            print("is located at:")
            print(self.whiteIndexes[i])
            print("index to piece test:")
            indexes=self.whiteIndexes[0]*10+self.whiteIndexes[1]
            print(self.whiteIToP[indexes])
            for j in range(self.whiteaVailableMoves[i]):
                print("can move to:")
                print(self.whiteaVailableMoves[self.whitePieces[i]][j])
                #check to see if a move puts the player in check
    def allMovesGen(self):#only call the move function after this is called.
        wKS=False
        bKS=False
        wQS=False
        bQS=False
        if self.bHasMovedKing==False:
            if self.bHasMovedR2==False&self.fullBoard[0][6]==piece(0,'n','n')&self.fullBoard[0][5]==piece(0,'n','n'):
                bKS=True
            if self.bHasMovedR1==False&self.fullBoard[0][1]==piece(0,'n','n')&self.fullBoard[0][2]==piece(0,'n','n')&self.fullBoard[0][3]==piece(0,'n','n'):
                bQS=True
        if self.wHasMovedKing==False:
                if self.wHasMovedR2==False&self.fullBoard[7][6]==piece(0,'n','n')&self.fullBoard[7][5]==piece(0,'n','n'):
                    wKS=True
                if self.wHasMovedR1==False&self.fullBoard[7][1]==piece(0,'n','n')&self.fullBoard[7][2]==piece(0,'n','n')&self.fullBoard[7][3]==piece(0,'n','n'):
                    wQS=True
        #self.canKSCastle() cutting this to improve efficiency. 
        #self.canQSCastle()
        for i in self.whitePieces:
            allMoves=self.generateAvailableMoves(self.whiteIndexes[self.whitePieces[i]][0],self.whiteIndexes[self.whitePieces[i]][1])
            self.whiteaVailableMoves[self.whitePieces[i]]=allMoves
            if (0,6) in allMoves|(0,5) in allMoves|(0,4) in allMoves|(0,7) in allMoves: 
                bKS=False
            if (0,4) in allMoves|(0,3) in allMoves|(0,2) in allMoves|(0,1) in allMoves|(0,0) in allMoves:
                bQS=False
            self.playerMovesElimininator()#looking to modify this function, only need to check whether or not q, r, b are pressuring king
        for j in self.blackPieces:
            allMoves=self.generateAvailableMoves(self.blackIndexes[self.whitePieces[i]][0],self.whiteIndexes[self.whitePieces[i]][1])
            self.whiteaVailableMoves[self.whitePieces[i]]=allMoves
            if (7,6) in allMoves|(7,5) in allMoves|(7,4) in allMoves|(7,7) in allMoves: 
                wKS=False
            if (7,4) in allMoves|(7,3) in allMoves|(7,2) in allMoves|(7,1) in allMoves|(7,0) in allMoves:
                wQS=False
            if self.whiteIndexes["K"] in allMoves:
                self.inCheckStored=True
            self.playerMovesElimininator()
    def move(self, index:int, availableMoveNum:int):#this will only be called after the gen all moves, so you dont have to run it twice 
        if self.turn%2==0: #if it's white's turn. 
            initialCoords=self.whiteIndexes[self.whitePieces[index]]
            newIndexes=self.whiteaVailableMoves[self.whitePieces[index]]#need to modify this function to make it more efficient
            if newIndexes==[9,9]: #king side castle
                self.fullBoard[7][4]=piece(0,'n','n')
                self.fullBoard[7][7]=piece(0,'n','n')
                self.fullBoard[7][6]=piece(0,'K','w')
                self.fullBoard[7][5]=piece(500, 'r', 'w')
                return 
            if newIndexes==[10,10]: #QSCastle
                self.fullBoard[7][4]=piece(0,'n','n')
                self.fullBoard[7][3]=piece(500,'r','w')
                self.fullBoard[7][2]=piece(0,'K', 'w')
                self.fullBoard[7][0]=piece(0,'n','n')
                self.fullBoard[7][1]=piece(0,'n','n')
                return 
            wOldPiece=self.whiteIndexes[0]
            oldpoints=self.fullBoard[newIndexes[0]][newIndexes[1]].val
            boldPiece=""
            if oldpoints>0:
                boldPiece=self.blackIToP[newIndexes[0]*10+newIndexes[1]]
            self.fullBoard[newIndexes[0]][newIndexes[1]]=piece.copy(self.fullBoard[initialCoords[0]][initialCoords[1]])
            if self.fullBoard[newIndexes[0]][newIndexes[1]].type=='p'&newIndexes[0]==0:#pawn to queen
                self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(900,'q','w')
                self.whitePoints+=8
            self.blackPoints-=oldpoints
            self.turn+=1
            if oldpoints>0:
                self.blackPieces.remove(boldPiece)
            self.blackIndexes.pop([newIndexes])
            self.blackIToP.pop([newIndexes])
            self.whiteIndexes[self.whitePieces[index]]=newIndexes
            self.whiteIToP[newIndexes[0]*10+newIndexes[1]]=self.whitePieces[index]#have to reset all fields to reflect information on the new board. 
            self.fullBoard[initialCoords[0]][initialCoords[1]]=piece(0,'n','n')
            if wOldPiece=="p1"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[0]=True
            if wOldPiece=="p2"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[1]=True
            if wOldPiece=="p3"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[2]=True
            if wOldPiece=="p4"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[3]=True
            if wOldPiece=="p5"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[4]=True
            if wOldPiece=="p6"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[5]=True
            if wOldPiece=="p7"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[6]=True
            if wOldPiece=="p8"&newIndexes[0]-initialCoords[0]==-2: 
                self.wHasSkipped[7]=True
        else: 
            initialCoords=self.blackIndexes[self.blackPieces[index]]
            newIndexes=self.blackAvailableMoves(self.blackPieces[index])[availableMoveNum]
            oldpoints=self.fullBoard[newIndexes[0]][newIndexes[1]].val
            oldPiece=""
            if oldpoints>0:
                oldPiece=self.whiteIToP[newIndexes[0]*10+newIndexes[1]]
            self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[initialCoords[0]][initialCoords[1]]
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
                self.whiteIToP.pop(newIndexes[0]*10+newIndexes[1])
            self.whiteIndexes.pop(oldPiece)
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
            for i in self.whitePieces:
                self.whiteaVailableMoves[self.whitePieces[i]].clear()#reset the board
        self.inCheckStored=False
    def playerMovesElimininator(self): #this function test whether or not each move results in a checkmate. 
        oldBoard=copy.deepcopy(self.fullBoard)
        if self.turn%2==0:
            for i in len(self.whitePieces):
                oldIndexes=self.whiteIndexes[self.whitePieces[i]]
                for j in len(self.whiteaVailableMoves[self.whitePieces[i]]):
                    self.fullBoard=oldBoard
                    self.fullBoard[self.whiteaVailableMoves[self.whitePieces[i]][j][0]][self.whiteaVailableMoves[self.whitePieces[i]][j][1]]\
                        =piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    if self.inCheck()==True: 
                        self.whiteaVailableMoves[self.whitePieces[i]].pop(self.whiteaVailableMoves[self.whitePieces[i]][j])
        else: 
            for i in len(self.blackPieces):
                oldIndexes=self.blackIndexes[self.blackPieces[i]]
                for j in len(self.blackAvailableMoves[self.blackPieces[i]]):
                    self.fullBoard=oldBoard
                    self.fullBoard[self.blackAvailableMoves[self.blackPieces[i]][j][0]][self.blackAvailableMoves[self.blackPieces[i]][j][1]]\
                        =piece.copy(self.fullBoard[oldIndexes[0]][oldIndexes[1]])
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    if self.inCheck()==True: 
                        self.blackAvailableMoves[self.blackPieces[i]].remove(self.blackAvailableMoves[self.whitePieces[i]][j])
    def canKSCastle(self):
        if self.turn%2==0&self.wHasMovedKing==False&self.wHasMovedR2==False&self.fullBoard[7][6]==piece(0,'n','n')\
            &self.fullBoard[7][5]==piece(0,'n','n'): 
            for i in range(len(self.blackPieces)):
                temp=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]])
                for j in range(temp): 
                    if temp[i]==(7,7)|temp[i]==(7,4)|temp[i]==(7,6)|temp[i]==(7,5):
                        return
            self.canKSCastle==True
            self.whiteaVailableMoves["K"].append([9,9])
        if self.turn%2==1&self.bHasMovedKing==False&self.bHasMovedR2==False&self.fullBoard[0][6]==piece(0,'n','n')\
            &self.fullBoard[0][5]==piece(0,'n','n'): 
                for i in range(len(self.whitePieces)):
                    temp=self.generateAvailableMoves(self.whiteIndexes[self.blackPieces[i]])
                    for j in range(temp): 
                        if temp[i]==(0,7)|temp[i]==(0,4)|temp[i]==(7,6)|temp[i]==(7,8):
                            return
                self.canKSCastle==True
                self.blackAvailableMoves["K"].append((9,9))
    def canQSCastle(self): 
            if self.turn%2==0&self.wHasMovedKing==False&self.wHasMovedR1==False&self.fullBoard[7][6]==piece(0,'n','n')\
            &self.fullBoard[7][5]==piece(0,'n','n'): 
                for i in range(len(self.blackPieces)):
                    temp=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]])
                    for j in range(temp): 
                        if temp[i]==[7,3]|temp[i]==[7,4]|temp[i]==[7,2]|temp[i]==[7,1]|temp[i]==[7,0]:
                            return 
                self.canQSCastle==True
                self.whiteaVailableMoves["K"].append((10,10))
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
    def printBoard(self):
        for i in range(8):
            print(self.fullBoard[i][0].type, self.fullBoard[i][1].type, self.fullBoard[i][2].type, self.fullBoard[i][3].type,self.fullBoard[i][4].type, self.fullBoard[i][5].type, self.fullBoard[i][6].type, self.fullBoard[i][7].type)

class treeNode: 
    def __init__(self, pgame:board) -> None:
        self.children=(treeNode,treeNode,treeNode,treeNode,treeNode)#list of board classes
        self.level=0
        self.parent=treeNode#previous board 
        self.game=board
def generateTopMoves(currGame:board, numMoves: int): #this function works for either team, so it can simulate human moves. 
    re=[]
    currGame.allMovesGen()
    currGame.playerMovesElimininator()#depth first search. Start with a given board that represents a possible move. 
    placeHolder=currGame.deepClone()
    if currGame.turn==0:
        for i in currGame.whitePieces: 
            for j in currGame.whiteaVailableMoves[currGame.whitePieces[i]]:
                if len(re)<numMoves: 
                    currGame.move(j,i)
                    currGame.allMovesGen() 
                    currGame.AIAdvantageEval()
                    re.append(currGame)
                else: 
                    currGame.move(j,i)
                    currGame.allMovesGen() 
                    currGame.AIAdvantageEval()
                    re.sort(key=lambda x:x.advantage)#sorts by the advantage parameter. 
                    if currGame.AIteam=="b":
                        if re[0].advantage < currGame.advantage:
                            re[0]=currGame
                        currGame=placeHolder
                    else: 
                        if re[0].advantage > currGame.advantage:
                            re[0]=currGame
                        currGame=placeHolder
    else:
        for i in currGame.blackPieces: 
            for j in currGame.blackAvailableMoves[currGame.blackPieces[i]]:
                if len(re)<numMoves: 
                    re.append(currGame.blackAvailableMoves[currGame.blackPieces[i]][j])
                else: #if its black vs if its white. 
                    currGame.move(j,i)
                    currGame.allMovesGen()
                    currGame.playerMovesElimininator()#depth first search. Start with a given board that represents a possible move. 
                    currGame.AIAdvantageEval()
                    re.sort(currGame.advantage)
                    if currGame.AIteam=="w":
                        if re[0]< currGame.advantage:
                            re.pop(0)
                            re.append(i,j)#this function generates the n moves that put the player in the best position.
                        currGame=placeHolder
                    else: 
                        if re[0]>currGame.advantage:
                            re.pop(0)
                            re.append(i,j)#this function generates the n moves that put the player in the best position.
                        currGame=placeHolder
    for i in re: 
        re[i]=treeNode(re[i])
    return re

def search(currGame:treeNode, depth:int, alphaBeta:int)->int:#Later, I want the depth to be predetermined by what stage of the game it is, earlier=less depth. 
    depth+=depth%2#need to end on an odd # of searches so that it's the players turn. 
    currGame.level+=currGame.parent.level+1
    destroy=False
    miniMax=10000000000
    if currGame.level==depth|currGame.game.gameState!=0:#if game is over, do not branch further on the tree. 
        if currGame.game.advantage<miniMax: 
            miniMax=currGame.game.advantage
            return
    elif currGame.game.advantage<alphaBeta: #if too bad of an advantage is reached, exit the search function
        miniMax=miniMax=currGame.game.advantage
        destroy=True
        while currGame.level!=1: 
            currGame=currGame.parent#go to the top of the tree, set children to none to stop searching
        currGame.children=()
        return
    else:
        if destroy!=False&currGame.children==():
            currGame.children=generateTopMoves(currGame,5)#5 top moves for now, may change this based on how things run
        for i in len(currGame.children): 
            search(currGame.children[i],depth, alphaBeta)#use backtracking/recursion to generate everything. returning will jump to this statement. 
    return miniMax#this parameter is what the AI will base each move on 
def AImove(game:board):
    bestSearch=-100000000
    moveIndexes=(0,0)
    reference=game.deepClone()
    if game.AIteam=="w": 
        for i in range(game.whitePieces):
            for j in game.whiteaVailableMoves[game.whitePieces[j]]: 
                game=reference
                game.move
                currSearch=treeNode(game)
                currScore=search(currSearch, 6, -200)
                if bestSearch<currScore: #eventually I want to figure out algorithms for evaluating depth and alphaBeta based on board conditions, but I need to look at runtimes first. 
                    moveIndexes=(i,j)
                    bestSearch=currScore
    else: 
        for i in range(game.blackPieces):
            for j in game.blackAvailableMoves[game.whitePieces[j]]: 
                currSearch=treeNode(game)
                currScore=search(currSearch, 6, -200)
                if bestSearch<currScore: #eventually I want to figure out algorithms for evaluating depth and alphaBeta based on board conditions, but I need to look at runtimes first. 
                    moveIndexes=(i,j)
                    bestSearch=currScore
    game.move(moveIndexes[0],moveIndexes[1])
def playerMove(game:board):
    game.printBoard() 
    game.allMovesGen()
    print("indexes of piece? ex. A4, case sensitive")
    valid=False
    row=-1
    col=-1#need variables to be nonLocal
    newRow=-1
    newCol=-1
    Piece=""
    if game.turn%2==0:
        while valid==False:
            strInd=input()
            row=ord(strInd[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            col=ord(strInd[0])-ord('A')#A is col 0, B is col 1, etc. 
            
            if row*10+col in game.whiteIToP:
                Piece=game.whiteIToP[row*10+col]
                valid=True#needs to map to a value. 
            print("Where do you want to move it?")
            strInt=input()
            valid2=False
            newRow=ord(strInt[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            newCol=ord(strInt[0])-ord('A')#A is col 0, B is col 1, etc. 
            if (newRow, newCol) in game.whiteaVailableMoves[Piece]:
                valid2=True
            if valid2==False: 
                valid=False
        i1=game.whitePieces.index(Piece)
        i2=game.whiteaVailableMoves[Piece].index(Piece)#this could be done more efficiently, because the move function was designed for the AI to do all this quickly, but efficiency in the player move is far less important. 
        game.move(i1,i2)
    else: 
        while valid==False:
            strInd=input()
            row=ord(strInd[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            col=ord(strInd[0])-ord('A')#A is col 0, B is col 1, etc. 
            if row*10+col in game.blackIToP:
                Piece=game.blackIToP[row*10+col]
                valid=True#needs to map to a value. 
            print("Where do you want to move it?")
            strInt=input()
            valid2=False
            newRow=ord(strInt[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            newCol=ord(strInt[0])-ord('A')#A is col 0, B is col 1, etc. 
            if (newRow, newCol) in game.blackAvailableMoves[Piece]:
                valid2=True
            if valid2==False: 
                valid=False
        i1=game.blackPieces.index(Piece)
        i2=game.blackAvailableMoves[Piece].index(Piece)#this could be done more efficiently, because the move function was designed for the AI to do all this quickly, but efficiency in the player move is far less important. 
        game.move(i1,i2)

   