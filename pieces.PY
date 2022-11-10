from tkinter import CHAR
from xmlrpc.client import boolean
import numpy as np 
from enum import Enum
import copy 
class ind(Enum):
    A=0
    B=1
    C=2
    D=3
    E=4
    F=5
    G=6
    H=7
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
        self.AIteam=""
        self.gameState=0
        self.fullBoard=np.array(np.array(piece(500,'r','b'),piece(300,'k','b'),piece(300,'b','b'),piece(900,'q','b'),piece(0, 'K', 'b'),piece(300,'b','b'),\
            piece(300,'k','b'), piece(500,'r','b')), np.array(piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b'),\
            piece(100,'p','b'),piece(100,'p','b'),piece(100,'p','b')),np.array(piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),\
            piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')),\
            np.array([piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')]),\
            np.array([piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),]),\
            np.array(piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n'),piece(0,'n','n')),\
            np.array(piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w'),\
            piece(1,'p','w'),piece(1,'p','w'),piece(1,'p','w')),\
            np.array(piece(500,'r','w'),piece(300,'k','w'),piece(300,'b','w'),piece(900,'q','w'),piece(0, 'K', 'w'),piece(300,'b','w'),\
            piece(300,'k','w'), piece(500,'r','w')))
        self.turn=0 #every time turn=1 
        self.blackIndexes={"r1":np.array(0,0),"r2":np.array(0,7),"b1":np.array(0,2),"b2":np.array(0,5),"k2":np.array(0,3),"k2":np.array(0,6),"K":np.array(0,4),"q":np.array(0,3),\
            "p1":np.array(1,0),"p2":np.array(1,1),"p3":np.array(1,2),"p4":np.array(1,3),"p5":np.array(1,4),"p6":np.array(1,5),"p7":np.array(1,6),"p8":np.array(1,7)}
        self.whiteIndexes={"r1":np.array([7,0]),"r2":np.array(7,7),"b1":np.array(7,2),"b2":np.array(7,5),"k2":np.array(7,3),"k2":np.array(7,4),"K":np.array(7,5),"q":np.array(7,4),\
            "p1":np.array(6,0),"p2":np.array(6,1),"p3":np.array(6,2),"p4":np.array(6,3),"p5":np.array(6,4),"p6":np.array(6,5),"p7":np.array(1,6),"p8":np.array(1,7)}
        self.blackIToP={0:"r1",7:"r2",5:"b1",5:"b2",1:"k1",6:"k2",4:"K",3:"q",\
            10:"p1",11:"p2",12:"p3",13:"p4",14:"p5",15:"p6",16:"p7",17:"p8"}
        self.whiteIToP={70:"r1",77:"r2",72:"b1",55:"b2",71:"k2",76:"k2",74:"K",73:"q",\
            60:"p1",61:"p2",62:"p3",63:"p4",64:"p5",65:"p6",66:"p7",67:"p8"}
        self.blackPoints=38
        self.whitePoints=38
        self.advantage=0
        self.whitePieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.blackPieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.whiteaVailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[np.array(5,7),np.array(5,5)],"K":[], "q":[], "k1":[np.array(5,0),np.array(5,2)], "p1":[np.array(5,0),np.array(6,0)]\
            ,"p2":[np.array(5,1),np.array(6,1)],"p3":[np.array(5,2),np.array(6,2)],"p4":[np.array(5,3),np.array(6,3)],"p5":[np.array(5,4),np.array(6,4)],"p6":[np.array(5,5),np.array(6,6)],"p7":[np.array(5,6),np.array(6,6)],"p8":[np.array(5,7),np.array(6,7)]}
        self.blackAvailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[np.array(2,5),np.array(2,7)],"K":[], "q":[], "k1":[np.array(2,0),np.array(2,2)], "p1":[np.array(2,0),np.array(3,0)]\
            ,"p2":[np.array(1,2),np.array(1,3)],"p3":[np.array(2,2),np.array(2,3)],"p4":[np.array(2,3),np.array(3,3)],"p5":[np.array(5,4),np.array(3,4)],"p6":[np.array(2,5),np.array(3,5)],"p7":[np.array(2,6),np.array(3,6)],"p8":[np.array(2,7),np.array(7,3)]}
        self.wHasSkipped=np.array(False,False,False,False,False,False,False,False,False)
        self.bHasSkipped=np.array(False,False,False,False,False,False,False,False,False)#this info is stored for en pessant captures.
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

    def generateAvailableMoves(self, row:int, col:int, temp:bool): #generates available moves for any piece on the board, takes old indexes as arguements, edits the field 
        #of available moves map 
            availableCol=[]
            availableMoves=[availableCol]
            if self.fullBoard[row][col].type=='p':
                if self.fullBoard[row][col].team=='b':#white and black move
                    if self.fullBoard[row+1][col+1].team!=self.fullBoard[row][col].team&\
                    self.fullBoard[row+1][col-1].team!='n':
                        availableMoves.append(np.array(row+1,col+1))
                    if self.fullBoard[row+1,col-1].team!=self.fullBoard[row][col].team&\
                        self.fullBoard[row+1][col-1].team!='n':
                            availableMoves.append(np.array(row+1,col+1))
                    if self.fullBoard[row+1][col].type=='n':
                        availableMoves.append(np.array(row+1,col))
                        if self.fullBoard[row+2][col].type=='n'&row==1: 
                            availableMoves.append(np.array(row+2,col))
                if self.fullBoard[row][col].team=='w': 
                    if self.fullBoard[row-1][col+1].team!=self.fullBoard[row][col].team&\
                    self.fullBoard[row-1][col-1].team!='n':
                        availableMoves.append(np.array(row-1,col+1))
                    if self.fullBoard[row-1,col-1].team!=self.fullBoard[row][col].team&\
                        self.fullBoard[row-1][col-1].team!='n':
                        availableMoves.append(np.array(row-1,col+1))
                    if self.fullBoard[row-1][col].type=='n':
                        availableMoves.append(np.array(row-1,col))
                        if self.fullBoard[row-2][col].type=='n'&row==6: 
                            availableMoves.append(np.array(row+2,col))
                if self.fullBoard[row][col+1].type=='p'&col==3&self.fullBoard[row][col].team=='b'&self.fullBoard[row][col].team=='w': 
                    availableMoves.append(np.array(row-1,col+1))
                if self.fullBoard[row][col-1].type=='p'&col==3&self.fullBoard[row][col].team=='b'&self.fullBoard[row][col].team=='w': 
                    availableMoves.append(np.array(row-1,col-1))
                if self.fullBoard[row][col+1].type=='p'&col==3&self.fullBoard[row][col].team=='w'&self.fullBoard[row][col].team=='b': 
                    availableMoves.append(np.array(row+1,col+1))
                if self.fullBoard[row][col-1].type=='p'&col==4&self.fullBoard[row][col].team=='w'&self.fullBoard[row][col].team=='b': 
                    availableMoves.append(np.array(row+1,col-1))
                return availableMoves
            elif self.fullBoard[row][col].type=='k':
                if self.fullBoard[row+2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col+1]!=None:
                    availableMoves.append(np.array(row+2,col+1))
                if self.fullBoard[row+1][col+2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+1][col+2]!=None:
                    availableMoves.append(np.array(row+1,col+2))
                if self.fullBoard[row-2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-2][col+1]!=None:
                    availableMoves.append(np.array(row-2,col+1))
                if self.fullBoard[row+2][col-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col-1]!=None:
                    availableMoves.append(np.array(row+2,col-1))
                if self.fullBoard[row-2][col-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-2][col-1]!=None:
                    availableMoves.append(np.array(row-2,col-1))
                if self.fullBoard[row+1][col-2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+1][col-2]!=None:
                    availableMoves.append(np.array(row+1,col-2))
                if self.fullBoard[row-1][col+2].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row-1][col+2]!=None:
                    availableMoves.append(np.array(row-1,col+2))
                if self.fullBoard[row+2][col+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[row+2][col+1]!=None:
                    availableMoves.append(row+2,col+1)
                return availableMoves
            elif self.fullBoard[row][col].type=='b':
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2+1]!=None:
                        availableMoves.append(np.array(temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2+1]!=None:
                        availableMoves.append(np.array([temp1+1,temp2+1]))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2-1]!=None:
                        availableMoves.append(np.array([temp1+1,temp2+1]))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2-1]!=None:
                        availableMoves.append(np.array(temp1+1,temp2+1))
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
                    availableMoves.append(np.array(temp1+1,temp2))
                    if self.fullBoard[temp1+1][temp2].team!='n':
                        break
                    temp1+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append(np.array(temp1-1,temp2))
                    if self.fullBoard[temp1-1][temp2].team!='n':
                        break
                    temp1-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append(np.array(temp1,temp2+1))
                    if self.fullBoard[temp1+1][temp2+1].team!='n':
                        break
                    temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2-1]!=None:
                    availableMoves.append(np.array(temp1,temp2-1))
                    if self.fullBoard[temp1+1][temp2-1].team!='n':
                        break
                    temp2-=1
                return availableMoves
            elif self.fullBoard[row][col].type=='q':
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2]!=None:
                    availableMoves.append(np.array(temp1+1,temp2))
                    if self.fullBoard[temp1+1][temp2].team!='n':
                        break
                    temp1+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append(np.array(temp1-1,temp2))
                    if self.fullBoard[temp1-1][temp2].team!='n':
                        break
                    temp1-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append(np.array([temp1,temp2+1]))
                    if self.fullBoard[temp1+1][temp2+1].team!='n':
                        break
                    temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2-1]!=None:
                    availableMoves.append(np.array(temp1,temp2-1))
                    if self.fullBoard[temp1+1][temp2-1].team!='n':
                        break
                    temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2+1]!=None:
                        availableMoves.append(np.array(temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1+=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2+1]!=None:
                        availableMoves.append(np.array(temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2+=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1-1][temp2-1]!=None:
                        availableMoves.append(np.array(temp1+1,temp2+1))
                        if self.fullBoard[temp1-1][temp2+1].team!='n':
                            break
                        temp1-=1
                        temp2-=1
                temp1=row
                temp2=col
                while self.fullBoard[temp1+1][temp2-1].team!=self.fullBoard[row][col].team\
                    &self.fullBoard[temp1+1][temp2-1]!=None:
                        availableMoves.append(np.array(temp1+1,temp2+1))
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
                    availableMoves.append(np.array(temp1+1,temp2))
                if self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append(np.array(temp1-1,temp2))
                if self.fullBoard[temp1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1][temp2+1]!=None:
                    availableMoves.append(np.array(temp1,temp2+1))
                if self.fullBoard[temp1-1][temp2].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2]!=None:
                    availableMoves.append(np.array(temp1,temp2+1))
                if self.fullBoard[temp1+1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1+1][temp2+1]!=None:
                    availableMoves.append(np.array(temp1+1,temp2+1))
                if self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2+1]!=None:
                    availableMoves.append(np.array(temp1-1,temp2+1))
                if self.fullBoard[temp1-1][temp2+1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2+1]!=None:
                    availableMoves.append(np.array(temp1-1,temp2+1))
                if self.fullBoard[temp1-1][temp2-1].team!=self.fullBoard[row][col].team\
                &self.fullBoard[temp1-1][temp2-1]!=None:
                    availableMoves.append(np.array(temp1-1,temp2-1))
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
    def AIAdvantageEval(self)->int:#only call this function after all moves have been generated and checked. going to search through a tree of ints for advantage parameter. 
        whiteAdvantage=0
        blackAdvantage=0
        if len(self.whitePieces) + len(self.blackPieces)==2: #2 kings left
            self.gameState+=1#tie game
            self.advantage=0

        noMovesW=True
        noMovesB=True#store these for the checkmate and stalemate conditions
        for i in range(len(self.whitePieces)):#need to go back and make some adjustments to the generate available moves function so that it adds to the field and returns a list. 
            oldIndexes=[self.whiteIndexes[self.whitePieces[i]]]
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
            if len(self.whitePieces+self.blackPieces)<10: #late game advantage for wight 
                    if self.fullBoard[oldIndexes[0]][oldIndexes[1]].type=='p'&oldIndexes[0]<4:
                        whiteAdvantage+=(4-oldIndexes[0])*20
                   

            for j in range(len(self.whiteaVailableMoves(self.whitePieces[i]))):
                if self.whiteaVailableMoves(self.whitePieces[i])!=[]:#if its empty, either checkmate or stalemate.
                    noMovesW=True
                newIndexes=self.whiteaVailableMoves[self.whitePieces[i]]
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
                    if self.blackIndexes["K"] in temp: #more efficient than calling check function
                        whiteAdvantage+=20
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=store1
                    self.fullBoard[newIndexes[0]][newIndexes[1]]=store2
                    if self.turn%2==0&self.inCheck(): 
                        blackAdvantage+=50#lateGame 
                    if len(self.whitePieces+self.blackPieces)<10: 
                        


                
                
                

                #check to see if a move puts the player in check
    def allMovesGen(self):#only call the move function after this is called.
        if self.turn%2==0: 
            for i in self.whitePieces:
                allMoves=self.generateAvailableMoves(self.whiteIndexes[self.whitePieces[0]],self.whiteIndexes[self.whitePieces[1]])
                self.whiteaVailableMoves[self.whitePieces[i]]=allMoves
                self.playerMovesElimininator()
        else: 
            for j in self.whitePieces:
                allMoves=self.generateAvailableMoves(self.whiteIndexes[self.whitePieces[0]],self.whiteIndexes[self.whitePieces[1]])
                self.whiteaVailableMoves[self.whitePieces[i]]=allMoves
                self.playerMovesElimininator()

    def move(self, index:int, availableMoveNum:int):
        if self.turn%2==0: #if it's white's turn. 
            initialCoords=self.whiteIndexes[self.whitePieces[index]]
            newIndexes=self.whiteaVailableMoves[self.whitePieces[index]]
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
                boldPiece=self.blackIToP[newIndexes]
            self.fullBoard[newIndexes[0]][newIndexes[1]]=self.fullBoard[initialCoords[0]][initialCoords[1]]
            if self.fullBoard[newIndexes[0]][newIndexes[1]].type=='p'&newIndexes[0]==0:#pawn to queen
                self.fullBoard[newIndexes[0]][newIndexes[1]]=piece(900,'q','w')
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
    def playerMovesElimininator(self): #need to remove pieces 
        oldBoard=copy.deepcopy(self.fullBoard)
        if self.turn%2==0:
            for i in len(self.whitePieces):
                oldIndexes=self.whiteIndexes[self.whitePieces[i]]
                for j in len(self.whiteaVailableMoves[self.whitePieces[i]]):
                    self.fullBoard=oldBoard
                    self.fullBoard[self.whiteaVailableMoves[self.whitePieces[i]][j][0]][self.whiteaVailableMoves[self.whitePieces[i]][j][1]]\
                        =self.fullBoard[oldIndexes[0]][oldIndexes[1]]
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    if self.inCheck()==True: 
                        self.whiteaVailableMoves[self.whitePieces[i]].pop(self.whiteaVailableMoves[self.whitePieces[i]][j])
        else: 
            for i in len(self.blackPieces):
                oldIndexes=self.blackIndexes[self.blackPieces[i]]
                for j in len(self.blackAvailableMoves[self.blackPieces[i]]):
                    self.fullBoard=oldBoard
                    self.fullBoard[self.blackAvailableMoves[self.blackPieces[i]][j][0]][self.blackAvailableMoves[self.blackPieces[i]][j][1]]\
                        =self.fullBoard[oldIndexes[0]][oldIndexes[1]]
                    self.fullBoard[oldIndexes[0]][oldIndexes[1]]=piece(0,'n','n')
                    if self.inCheck()==True: 
                        self.blackAvailableMoves[self.blackPieces[i]].remove(self.blackAvailableMoves[self.whitePieces[i]][j])
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
    