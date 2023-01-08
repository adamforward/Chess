from tkinter import CHAR
from xmlrpc.client import boolean
import copy 
import sys
#I am currently looking into using matrix operations to improve efficiency, particularly within the generate available moves function and repetetive iterations within functions such as in check.  
#I currently have all the functions I need to run a game with relatively little code, still have to debug though.  
# #when I get the game up and running, I will probably make some modifications to the "AIAdvantageEval" function based on how it performs. 
class piece:
    def __init__(self, val:int, kind:CHAR, team:CHAR): 
        self.val=val
        self.kind=kind
        self.team=team
    def copy(self):
        return piece(self.val, self.kind, self.team)
class board:
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
            piece(300,'k','w'), piece(500,'r','w')])#this is used to generate available moves and keep track of everything that's written. 
        self.turn=0 #every time turn=1 
        self.blackIndexes={"r1":0,"r2":7,"b1":2,"b2":5,"k1":1,"k2":6,"K":4,"q":3,\
            "p1":10,"p2":11,"p3":12,"p4":13,"p5":14,"p6":15,"p7":16,"p8":17}
        self.whiteIndexes={"r1":70,"r2":77,"b1":72,"b2":75,"k2":71,"k2":76,"K":74,"q":73,\
            "p1":60,"p2":61,"p3":62,"p4":63,"p5":64,"p6":65,"p7":66,"p8":67}
        self.blackIToP={0:"r1",7:"r2",5:"b1",5:"b2",1:"k1",6:"k2",4:"K",3:"q",\
            10:"p1",11:"p2",12:"p3",13:"p4",14:"p5",15:"p6",16:"p7",17:"p8"}#important in cutting down on runtime in many methods used below. 
        self.whiteIToP={70:"r1",77:"r2",72:"b1",55:"b2",71:"k2",76:"k2",74:"K",73:"q",\
            60:"p1",61:"p2",62:"p3",63:"p4",64:"p5",65:"p6",66:"p7",67:"p8"}#index to pieces 
        self.blackPoints=3800
        self.whitePoints=3800
        self.advantage=0
        self.whitePieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.blackPieces=["r1","r2","b1","b2","k2","K", "q", "k1", "p1","p2","p3","p4","p5","p6","p7","p8"]
        self.whiteaVailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[55,57],"K":[], "q":[], "k1":[50,52], "p1":[50,60]\
            ,"p2":[51,61],"p3":[52,62],"p4":[53,63],"p5":[54,64],"p6":[55,66],"p7":[56,66],"p8":[57,67]}
        self.blackAvailableMoves={"r1":[],"r2":[],"b1":[],"b2":[],"k2":[25,27],"K":[], "q":[], "k1":[20,22], "p1":[20,30]\
            ,"p2":[12, 13],"p3":[(2,2),(2,3)],"p4":[(2,3),(3,3)],"p5":[(5,4),(3,4)],"p6":[(2,5),(3,5)],"p7":[(2,6),(3,6)],"p8":[(2,7),(7,3)]}
        self.wHasMovedKing=False
        self.wHasMovedR1=False
        self.wHasMovedR2=False
        self.bHasMovedKing=False
        self.bHasMovedR1=False
        self.bHasMovedR2=False
        self.AIAdvantage=0


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
        newB.whiteaVailableMoves=copy.deepcopy(self.whiteaVailableMoves)
        newB.whiteIndexes=copy.deepcopy(self.whiteIndexes)
        newB.whiteIToP=copy.deepcopy(self.whiteIToP)
        newB.whitePieces=copy.deepcopy(self.whitePieces)
        newB.whitePoints=self.whitePoints
        return newB

        
    def generateAvailableMoves(self, row: int, col: int):#changing this function up, dividing it into different sections for pieces
        if self.fullBoard[row][col].kind=='p': #returns an integer, /10=row, %10=col
            if self.fullBoard[row][col].team=='w':#only pawns vary in the indexes they can move to 
                return self.generatePawnMovesw(row, col)
            else: 
                return self.generatePawnMovesb(row, col)
        elif self.fullBoard[row][col].kind=='k': 
            return self.knightMoves(row, col)
        elif self.fullBoard[row][col].kind=='r':
            return self.rookMoves(row, col)
        elif self.fullBoard[row][col].kind=='b':
            return self.bishopMoves(row, col)
        elif self.fullBoard[row][col].kind=='K': 
            return self.kingMoves(row, col)
        elif self.fullBoard[row][col].kind=='q':
            re=self.rookMoves(row, col)
            re.append(self.bishopMoves(row,col))
            return re
        else: #gen available moves looks good 
            return None

    def generatePawnMovesw(self,row, col):#white starts at row 6
        re=[]
        if row==6 and self.fullBoard[row][col].team=='n': #skipping first 
            re.append(40+col)
        if self.fullBoard[row-1][col].team=='n': #boundary conditions never met, because in the move function if it goes to the end it becomes queen 
            re.append(10*(row-1)+col)#move forward 1 
        if col==0: #this series of is else statements is for attacking black pieces 
            if self.fullBoard[row-1][col+1].team=='b': #left edge, avoid indexing out of bounds 
                re.append(10*(row-1)+col+1)
            if row==3: #en pessant 
                #pawns are labeled by strings p1, p2, p3,... 
                #so ascii table(1)-ascii table(pawnstring[1]) gives you original column. 
                #if pawn on square that you want to en pessant corresponds to it's original column, you can en pessant 
                if self.fullBoard[3][1].team=='b' and self.fullBoard[3][1].kind=='p': 
                    if ord(self.blackIToP[31][1])-ord('1')==0: 
                        re.append(31)
        elif col==7:#right edge
            if self.fullBoard[col-1][row-1].team=='b': 
                re.append(10*(row-1)+col-1)
            if row==3: 
                if self.fullBoard[3][6].team=='b' and self.fullBoard[3][6].kind=='p': #en pessant, same idea but col index is 6
                    if ord(self.blackIToP[36][1])-ord('6')==0: #if it's p6, this expression will be ord("6")-ord("6")
                        re.append(36)
        else: #not on the edge
            if self.fullBoard[col-1][row-1].team=='b': 
                re.append(10*(row-1)+col-1)
            if self.fullBoard[col+1][row-1].team=='b': 
                re.append(10*(row-1)+col+1)
            if row==3:
                if self.fullBoard[3][col-1].team=='b' and self.fullBoard[3][col-1].kind=='p': #en pessant, same idea but col index is 6
                    if ord(self.blackIToP[30+col-1][1])-ord('1')==col-1:#if it's p8, the left hand side will =7
                        re.append(30+col-1)#check right and left if it's not on the edge 
                if self.fullBoard[3][col+1].team=='b' and self.fullBoard[3][col+1].kind=='p': 
                    if ord(self.blackIToP[30+col+1][1])-ord('1')==col+1:
                        re.append(30+col+1)


    def generatePawnMovesb(self, row, col):#black starts at row 1, index goes up. only difference is the reference point of 3 for en pessant changes to 5, row+=1 instead of -=1 
        re=[]
        if row==1 and self.fullBoard[row][col].team=='n': #skipping first 
            re.append(30+col)
        if self.fullBoard[row+1][col].team=='n': #boundary conditions never met, because in the move function if it goes to the end it becomes queen 
            re.append(10*(row+1)+col)#move forward 1 
        if col==0: #this series of is else statements is for attacking black pieces 
            if self.fullBoard[row+1][col+1].team=='w': #left edge, avoid indexing out of bounds 
                re.append(10*(row+1)+col+1)
            if row==5: #en pessant 
                #pawns are labeled by strings p1, p2, p3,... 
                #so ascii table(1)-ascii table(pawnstring[1]) gives you original column. 
                #if pawn on square that you want to en pessant corresponds to it's original column, you can en pessant 
                if self.fullBoard[5][1].team=='w' and self.fullBoard[5][1].kind=='p': 
                    if ord(self.whiteIToP[51][1])-ord(1)==0: 
                        re.append(51)
        elif col==7:#right edge
            if self.fullBoard[col-1][row+1].team=='w': 
                re.append(10*(row+1)+col-1)
            if row==5: 
                if self.fullBoard[5][6].team=='w' and self.fullBoard[5][6].kind=='p': #en pessant, same idea but col index is 6
                    if ord(self.blackIToP[56][1])-ord(6)==0: #if it's p6, this expression will be ord("6")-ord("6")
                        re.append(36)
        else: 
            if self.fullBoard[col-1][row+1].team=='w': 
                re.append(10*(row-1)+col-1)
            if self.fullBoard[col+1][row+1].team=='w': 
                re.append(10*(row-1)+col+1)
            if row==5:
                if self.fullBoard[5][col-1].team=='w' and self.fullBoard[5][col-1].kind=='p': #en pessant, same idea but col index is 6
                    if ord(self.blackIToP[50+col-1][1])-ord(1)==col-1:#if it's p8, the left hand side will =7
                        re.append(50+col-1)#check right and left if it's not on the edge 
                if self.fullBoard[5][col+1].team=='w' and self.fullBoard[5][col+1].kind=='p': 
                    if ord(self.blackIToP[50+col+1][1])-ord(1)==col+1:
                        re.append(50+col+1)



    def knightMoves(self, row:int, col:int): #debugged
        re=[]
        team=self.fullBoard[row][col].team
        for i in (1,-1): 
            moveRow=row+i
            for j in (3,-3): 
                moveCol=col+j
                if 0<=moveRow<=7 and 0<=col<=7 and self.fullBoard[moveRow][moveCol].team!=team:
                    re.append(moveRow*10+moveCol)
                if 0<=moveRow<=7 and 0<=col<=7 and self.fullBoard[moveRow][moveCol].team!=team:
                    re.append(moveRow*10+moveCol)
        for i in (1,-1): 
            moveCol=col+i
            for j in (3,-3): 
                moveRow=row+j
                if 0<=moveRow<=7 and 0<=col<=7 and self.fullBoard[moveRow][moveCol].team!=team:
                    re.append(moveRow*10+moveCol)
                if 0<=moveRow<=7 and 0<=col<=7 and self.fullBoard[moveRow][moveCol].team!=team:
                    re.append(moveRow*10+moveCol)
        return re
                

    def bishopMoves(self,row:int, col:int):#debugged
        re=[]
        team=self.fullBoard[row][col]
        for i in (1,-1): 
            moveRow=i
            for j in (1,-1): 
                moveCol=j
                while 0<= moveRow <=7 and self.fullBoard[moveRow][moveCol].team!=team:
                    re.append(moveRow*10+moveCol)
                    if self.fullBoard[moveRow][moveCol].team!=team:
                        break
        return re
        


    def rookMoves(self, row:int, col:int): #same idea as bishop, but only one changes at a time.
        re = []
        team = self.fullBoard[row][col].team #debugged
        for i in (1, -1):
            moveRow = row + i
            while 0 <= moveRow <= 7 and self.fullBoard[moveRow][col].team != team:
                re.append(moveRow * 10 + col)
                if self.fullBoard[moveRow][col].team != "n":
                    break
                moveRow += i
            moveCol = col + i
            while 0 <= moveCol <= 7 and self.fullBoard[row][moveCol].team != team:
                re.append(row * 10 + moveCol)
                if self.fullBoard[row][moveCol].team != "n":
                    break
                moveCol += i
        return re


    def kingMoves(self,row:int,col:int): #debugged 
        team=self.fullBoard[row][col].team
        re=[]
        for i in (1,-1): 
            moveRow=row+i
            if 0<=moveRow<=7 and self.fullBoard[moveRow][col].team!=team:
                re.append(moveRow*10+moveCol)
            if 0<=moveCol+i and self.fullBoard[row][moveCol+i].team!=team: 
                re.append(row*10+col)
            for j in (1,-1): 
                moveCol=col+j
                if 0<=moveRow<=7 and 0<=col<=7 and self.fullBoard[moveRow][moveCol].team!=team:
                    re.append(moveRow*10+moveCol)
                if 0<=moveRow<=7 and 0<=col<=7 and self.fullBoard[moveRow][moveCol].team!=team:
                    re.append(moveRow*10+moveCol)
        return re
                


    def AIAdvantageEval(self):#only call this function after all moves have been generated and checked. going to search through a tree of ints for advantage parameter. 
        if self.turn<=20: 
            self.earlyGameAIEval()
        elif self.turn>20 and len(self.blackPieces)>5 and len(self.whitePieces>5): 
            self.midGameAIEval()
        else: 
            self.lateGameAIEval


    def earlyGameAIEval(self):#seperating out early, mid and late game functions to make things more readable and organized, easy for debugging
        whiteAdvantage=0
        blackAdvantage=0
        noMovesW=True
        noMovesB=True

        for i in range(len(self.blackPieces)):
            currIndex=self.blackIndexes[self.blackPieces[i]]
            currRow=currIndex/10
            currCol=currIndex%10
            blackAdvantage+=len(self.blackAvailableMoves[self.blackPieces[i]])#more moves means more piece development 
            if currIndex==33 or currIndex==34 or currIndex==44 or currIndex==43:#favor moves from the middle 
                blackAdvantage+=2*len(self.blackAvailableMoves[self.blackPieces[i]])
            if len(self.blackAvailableMoves[self.blackPieces[i]])!=0: 
                noMovesB=False
            for j in range(len(self.blackAvailableMoves[self.blackPieces[i]])):
                moveIndexes=self.blackAvailableMoves[self.blackPieces[i]][j]
                if moveIndexes==33 or moveIndexes==34 or moveIndexes==44 or moveIndexes==43:
                    #moves to the middle
                    blackAdvantage+=3#once again, I will look at these weights after playing against it
                if self.turn%2==1:
                    if self.fullBoard[moveIndexes/10][moveIndexes%10].team=='w':
                        if self.fullBoard[moveIndexes/10][moveIndexes%10].val>self.fullBoard[currRow][currCol]: 
                            blackAdvantage+=self.fullBoard[moveIndexes/10][moveIndexes]%10-self.fullBoard[currRow][currCol]-50
                            #if b pawn is attacking w queen and its black's turn, advantage is 850 points 
        if noMovesB==True and self.turn%2==1: #CheckMate, cannot stalemate within first 32 turns 
                    whiteAdvantage=1000000
                    blackAdvantage=-1000000
                    self.gameState+=1

        for i in range(len(self.whitePieces)):
            currIndex=self.whiteIndexes[self.whitePieces[i]]
            currRow=currIndex/10
            currCol=currIndex%10
            whiteAdvantage+=len(self.whiteaVailableMoves[self.whitePieces[i]])#more moves means more piece development 
            if currIndex==33 or currIndex==34 or currIndex==44 or currIndex==43:#favor moves from the middle 
                whiteAdvantage+=2*len(self.whiteaVailableMoves[self.whitePieces[i]])
            if len(self.whiteaVailableMoves[self.whitePieces[i]])!=0: 
                noMovesW=False
            for j in range(len(self.whiteaVailableMoves[self.whitePieces[i]])):
                moveIndexes=self.whiteaVailableMoves[self.whitePieces[i]][j]
                if moveIndexes==33 or moveIndexes==34 or moveIndexes==44 or moveIndexes==43:
                    #moves to the middle
                    whiteAdvantage+=3#once again, I will look at these weights after playing against it
                if self.turn%2==1 and self.fullBoard[moveIndexes/10][moveIndexes%10].team=='b' and self.fullBoard[moveIndexes/10][moveIndexes%10].val>self.fullBoard[currRow][currCol]: 
                    blackAdvantage+=self.fullBoard[moveIndexes/10][moveIndexes%10]-self.fullBoard[currRow][currCol]-50
        if noMovesW==True and self.turn%2==0: #CheckMate, cannot stalemate within first 20 turns 
                blackAdvantage=1000000
                whiteAdvantage=-1000000
                self.gameState+=1
        if self.AIteam=="w": 
            self.advantage=self.whitePoints-self.blackPoints+whiteAdvantage-blackAdvantage#white team for AI 
        else:
            self.advantage=self.blackPoints-self.whitePoints+blackAdvantage-whiteAdvantage#black team for AI 


    def midGameAIEval(self):# if turn is greater than 32 and if both teams have at least 5 pieces 
        blackAdvantage=0
        whiteAdvantage=0
        noMovesBlack=False
        noMovesWhite=False
        if self.turn%2==0 and self.inCheckStored==True: #late and middle game. 
            blackAdvantage+=50
        if self.turn%2==1 and self.inCheckStored==True: 
            whiteAdvantage+=50

        for i in range(len(self.blackPieces)):
            currIndex=self.blackIndexes[self.blackPieces[i]]
            currRow=currIndex/10
            currCol=currIndex%10
            if currIndex==33 or currIndex==34 or currIndex==44 or currIndex==43:#favor moves from the middle heavier in midgame
                blackAdvantage+=3*len(self.blackAvailableMoves[self.blackPieces[i]])
            if self.fullBoard[currRow][currCol].kind=='p':
                if currRow==5: 
                    blackAdvantage+=50 
                if currRow==6: 
                    blackAdvantage+=100
            if len(self.blackAvailableMoves[self.blackPieces[i]])!=0:
                noMovesBlack=False
            for j in range(self.blackAvailableMoves[self.blackPieces[i]]):
                moveIndexes=self.blackAvailableMoves[self.blackPieces[i]][j]
                moveRow=moveIndexes/10
                moveCol=moveIndexes%10
                if moveRow==5: 
                    blackAdvantage+=1
                if moveRow==6:
                    blackAdvantage+=3
                if moveRow==7:
                    blackAdvantage+=5#favor moves to other teams side slightly 
                if moveIndexes==33 or moveIndexes==34 or moveIndexes==43 or moveIndexes==44: 
                    blackAdvantage+=5
                if self.turn%2==1 and self.fullBoard[moveRow][moveCol].team=='w' and self.fullBoard[moveRow][moveCol].val>self.fullBoard[currRow][currCol]: 
                    blackAdvantage+=self.fullBoard[moveIndexes/10][moveIndexes]%10-self.fullBoard[currRow][currCol]-50

        for i in range(len(self.whitePieces)):
            currIndex=self.whiteIndexes[self.whitePieces[i]]
            currRow=currIndex/10
            currCol=currIndex%10
            if currIndex==33 or currIndex==34 or currIndex==44 or currIndex==43:#favor moves from the middle heavier in midgame
                whiteAdvantage+=3*len(self.whiteaVailableMoves[self.whitePieces[i]])
            if self.fullBoard[currRow][currCol].kind=='p':
                if currRow==2: 
                    whiteAdvantage+=50
                if currRow==1: 
                    whiteAdvantage+=100
                if len(self.whiteaVailableMoves[self.whitePieces[i]])!=0:
                    noMovesWhite=False
            for j in range(self.whiteaVailableMoves[self.whitePieces[i]]):
                moveIndexes=self.whiteaVailableMoves[self.whitePieces[i]][j]
                moveRow=moveIndexes/10
                moveCol=moveIndexes%10
                if moveRow==5: 
                    whiteAdvantage+=1
                if moveRow==6:
                    whiteAdvantage+=3
                if moveRow==7:
                    whiteAdvantage+=5#favor moves to other teams side slightly 
                if moveIndexes==33 or moveIndexes==34 or moveIndexes==43 or moveIndexes==44: 
                    whiteAdvantage+=5
                if self.turn%2==1 and self.fullBoard[moveRow][moveCol].team=='b' and self.fullBoard[moveRow][moveCol].val>self.fullBoard[currRow][currCol]: 
                    whiteAdvantage+=self.fullBoard[moveIndexes/10][moveIndexes]%10-self.fullBoard[currRow][currCol]-50

        if noMovesWhite==True and self.turn%2==1: #CheckMate, cannot stalemate within first 32 turns 
            if self.inCheckStored==True: 
                blackAdvantage=1000000
                whiteAdvantage=-1000000
                self.gameState+=1
            else: 
                self.advantage=0
                self.gameState=1
        if noMovesBlack==True and self.turn%2==0: 
            if self.inCheckStored==True: 
                blackAdvantage=-1000000
                whiteAdvantage=1000000
                self.gameState+=1
            else: 
                blackAdvantage=0
                whiteAdvantage=0
                self.whitePoints=0
                self.blackPoints=0
                self.gameState=1
        if self.AIteam=="w":
            self.advantage=self.whitePoints-self.blackPoints+whiteAdvantage-blackAdvantage#white team for AI 
        else:
            self.advantage=self.blackPoints-self.whitePoints+blackAdvantage-whiteAdvantage#black team for AI 


    def lateGameAIEval(self):#I probably want to create some algorithm for comparing search depth to pieces left, less pieces left means deeper search
        if len(self.whitePieces) + len(self.blackPieces)==2: #2 kings left
            self.gameState+=1#tie game
            self.advantage=0
            return 
        whiteAdvantage=0
        blackAdvantage=0
        noMovesW=True
        noMovesB=True
        if self.blackPoints<self.whitePoints:
            whiteAdvantage+=3*(len(self.blackPieces)+len(self.whitePieces))#incentivise trades if you're up in the late game 
        if self.blackPoints>self.whitePoints:
            blackAdvantage+=3*(len(self.blackPieces)+len(self.whitePieces))
        if self.turn%2==0 and self.inCheckStored==True: #late and middle game. 
            blackAdvantage+=50
        if self.turn%2==1 and self.inCheckStored==True: 
            whiteAdvantage+=50
        if len(self.blackPieces)==1:#If last piece is the black king, push it to the edge for checkmate
            bKingRow=self.blackIndexes/10
            bKingCol=self.blackIndexes%10
            if bKingRow==2 or bKingRow==5:
            #has to be weighted heavily, this is to pushes the king to the edge for checkmate
                whiteAdvantage+=100 
            if bKingCol==2 or bKingCol==5: 
                whiteAdvantage+=100
            if bKingRow==1 or bKingRow==6: 
                whiteAdvantage+=150
            if bKingCol==1 or bKingCol==6:
                whiteAdvantage+=150
            if bKingRow==0 or bKingRow==7: 
                whiteAdvantage+=200
            if bKingCol==0 or bKingCol==7:
                whiteAdvantage+=200
        if len(self.whitePieces)==1:#same for white
            wKingRow=self.blackIndexes/10
            wKingCol=self.blackIndexes%10
            if wKingRow==2 or wKingRow==5:
            #has to be weighted heavily, this is to pushes the king to the edge for checkmate
                blackAdvantage+=100 
            if wKingCol==2 or wKingCol==5: 
                blackAdvantage+=100
            if wKingRow==1 or wKingRow==6: 
                blackAdvantage+=150
            if wKingCol==1 or wKingCol==6:
                blackAdvantage+=150
            if wKingRow==0 or wKingRow==7: 
                blackAdvantage+=200
            if wKingCol==0 or wKingCol==7:
                blackAdvantage+=200


        for i in range(len(self.blackPieces)): 
            currIndexes=self.blackIndexes[self.blackPieces[i]]
            currRow=currIndexes/10
            currCol=currIndexes%10
            if self.fullBoard[currRow][currCol].kind=='p': 
                if currRow>4: 
                    blackAdvantage+=currRow*30#this way, higher rows get more points for pawns
            if len(self.blackAvailableMoves[self.blackPieces[i]])!=0:
                noMovesB=False
            for j in range(self.blackAvailableMoves[self.blackPieces[i]]):#no middle control weight for late game
                moveIndexes=self.blackAvailableMoves[self.blackPieces[i]][j]
                moveRow=moveIndexes/10
                moveCol=moveIndexes%10
                if self.turn%2==1 and self.fullBoard[moveRow][moveCol].team=='b' and self.fullBoard[moveRow][moveCol].val>self.fullBoard[currRow][currCol]: 
                    whiteAdvantage+=self.fullBoard[moveIndexes/10][moveIndexes]%10-self.fullBoard[currRow][currCol]-50

        for i in range(len(self.whitePieces)): 
            currIndexes=self.whiteIndexes[self.whitePieces[i]]
            currRow=currIndexes/10
            currCol=currIndexes%10
            if self.fullBoard[currRow][currCol].kind=='p': 
                if currRow<3: 
                    whiteAdvantage+=(7-currRow)*30
            if len(self.whiteaVailableMoves[self.blackPieces[i]])!=0:
                noMovesW=False
            for j in range(self.whiteaVailableMoves[self.whitePieces[i]]):
                moveIndexes=self.whiteaVailableMoves[self.whitePieces[i]][j]
                moveRow=moveIndexes/10
                moveCol=moveIndexes%10
                if self.turn%2==1 and self.fullBoard[moveRow][moveCol].team=='w' and self.fullBoard[moveRow][moveCol].val>self.fullBoard[currRow][currCol]: 
                    whiteAdvantage+=self.fullBoard[moveIndexes/10][moveIndexes]%10-self.fullBoard[currRow][currCol]-50

        if noMovesW==True and self.turn%2==1: #CheckMate
            if self.inCheckStored==True: 
                blackAdvantage=1000000
                whiteAdvantage=-1000000
                self.gameState+=1
            else: 
                self.advantage=0
                self.gameState=1#staleMate
        if noMovesB==True and self.turn%2==0: 
            if self.inCheckStored==True: 
                blackAdvantage=-1000000
                whiteAdvantage=1000000
                self.gameState+=1
            else: 
                blackAdvantage=0
                whiteAdvantage=0
                self.whitePoints=0
                self.blackPoints=0
                self.gameState=1
        if self.AIteam=="w":
            self.advantage=self.whitePoints-self.blackPoints+whiteAdvantage-blackAdvantage#white team for AI 
        else:
            self.advantage=self.blackPoints-self.whitePoints+blackAdvantage-whiteAdvantage#black team for AI 


    def allMovesGen(self):#only call the move function after this is called.
        bKS=self.bHasMovedKing&self.bHasMovedR2==False and self.fullBoard[0][6]==piece(0,'n','n') and self.fullBoard[0][5]==piece(0,'n','n')
        bQS=self.bHasMovedKing&self.bHasMovedR1==False and self.fullBoard[0][1]==piece(0,'n','n') and self.fullBoard[0][2]==piece(0,'n','n') and self.fullBoard[0][3]==piece(0,'n','n')   
        wKS=self.wHasMovedKing==False and self.wHasMovedR2==False and self.fullBoard[7][6]==piece(0,'n','n') and self.fullBoard[7][5]==piece(0,'n','n')
        wQS=self.wHasMovedKing==False and self.wHasMovedR1==False and self.fullBoard[7][1]==piece(0,'n','n') and self.fullBoard[7][2]==piece(0,'n','n') and self.fullBoard[7][3]==piece(0,'n','n')   
        #the lines of code check to see if the squares in between K and R are empty and if you've moved those pieces.   
        #self.canKSCastle() cutting this to improve efficiency. Represented by (9,9)
        #self.canQSCastle() is checked here, represented by (10,10)
        blackChecking=[]
        whiteChecking=[]
        wpinning=[]
        bpinned={}
        bpinning=[]
        wpinned={}
        wKingMoves=self.generateAvailableMoves(self.whiteIndexes["K"]/10, self.whiteIndexes["K"]%10)
        bKingMoves=self.generateAvailableMoves(self.blackIndexes["K"]/10, self.blackIndexes["K"]%10)#will need to remove some of these 
        

        for i in range(len(self.whitePieces)):
            currRow=self.whiteIndexes[self.whitePieces[i]]/10
            currCol=self.whiteIndexes[self.whitePieces[i]]%10
            allMoves=self.generateAvailableMoves(currRow,currCol)#array of places you can move to 
            if self.turn%2==1:#pinned condition only matters if it's black's turn 
                if self.whitePieces[i][0]=="q" or self.whitePieces[i]=="r" or self.whitePieces[i]=="b": 
                    for j in range(len(allMoves)): 
                        moveIndexes=allMoves[j]
                        moveRow=moveIndexes/10
                        moveCol=moveIndexes%10
                        if self.fullBoard[moveRow][moveCol].team=='b':
                            restore=self.fullBoard[moveRow][moveCol].copy()
                            self.fullBoard[moveRow][moveCol]=piece(0,'n','n')
                            if self.blackIndexes["K"] in self.generateAvailableMoves(currRow,currCol):
                                bpinned[self.whitePieces[i]]=self.blackIToP[moveIndexes]#check conditions for if a piece is pinned
                                wpinning.append(self.whitePieces[i])
                            self.fullBoard[moveRow][moveCol]=restore#run a helper method at the end
                self.whiteaVailableMoves[self.whitePieces[i]]=allMoves
                if self.blackIndexes["K"] in allMoves:#in check condition
                    self.inCheckStored=True #only look to see if black's in check if it's blacks turn, cannot move into check 
                    whiteChecking.append(self.whitePieces[i])
            for j in bKingMoves:
                if bKingMoves[j] in allMoves:
                    bKingMoves.pop(j)
            if bKS==True:#can QS castle
                bKS=not(6 in allMoves or 5 in allMoves or 4 in allMoves or 7 in allMoves)
            if bQS==True: 
                bQS=not(4 in allMoves or 3 in allMoves or 2 in allMoves or 1 in allMoves or 0 in allMoves)
            #looking to modify this function, only need to check whether or not q, r, b are pressuring king
        if bKS==True: 
            self.blackAvailableMoves["K"].append(99)#KS castle check. 
        if bQS==True: 
            self.blackAvailableMoves["K"].append(100)#if condition is met, black can QS castle, cuts down on iterations. 


        for j in self.blackPieces:
            currRow=self.blackIndexes[self.blackPieces[i]]/10
            currCol=self.blackIndexes[self.blackPieces[i]]%10
            allMoves=self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]]/10,self.blackIndexes[self.blackPieces[i]]%10)
            if self.turn%2==0:
                if self.blackPieces[i][0]=="q" or self.blackPieces[i]=="r" or self.blackPieces[i]=="b": 
                    for j in allMoves: 
                        moveIndexes=allMoves[j]
                        moveRow=moveIndexes/10
                        moveCol=moveIndexes%10
                        if self.fullBoard[moveRow][moveCol].team=='w':
                            restore=self.fullBoard[moveRow][moveCol].copy()
                            self.fullBoard[moveRow][moveCol]=piece(0,'n','n')
                            if self.whiteIndexes["K"] in self.generateAvailableMoves(self.blackIndexes[self.blackPieces[i]]/10,self.blackIndexes[self.blackPieces[i]]%10):
                                wpinned[self.blackPieces[i]]=restore
                                bpinning.append(self.blackIToP[moveIndexes])
                            self.fullBoard[moveRow][moveCol]=restore#run a helper method at the end
                    self.blackAvailableMoves[self.blackPieces[i]]=allMoves
                if self.whiteIndexes["K"] in allMoves:#in check condition
                    self.inCheckStored=True
                    blackChecking.append(self.blackPieces[i])
            for j in wKingMoves:
                if wKingMoves[j] in allMoves:
                    bKingMoves.pop(j)
            if wKS==True:#can QS castle
                if 76 in allMoves or 75 in allMoves or 74 in allMoves or 77 in allMoves: 
                    wKS=False
            if wQS==True: 
                if 44 in allMoves or 73 in allMoves or 72 in allMoves or 71 in allMoves or 70 in allMoves: 
                    wQS=False

        self.whiteaVailableMoves["K"]=wKingMoves
        self.blackAvailableMoves["K"]=bKingMoves
        if wpinning!=[]: 
            for i in wpinning:
                direction=[]
                direction.append(self.blackIndexes["K"]/10-self.whiteIndexes[wpinning[i]]/10)#tells you which orientation the piece is checking the king in, only need to compare 1/8 as many squares for a queen 
                direction.append(self.blackIndexes["K"]%10-self.whiteIndexes[wpinning[i]]%10)#-, positive or 0 is the only neccessary information here. 
                self.Pinned(bpinned[wpinning[i]], wpinning[i],direction, "w")
        if whiteChecking!=[]: #now that moves and necessary info has been generated, need to eliminate moves that put the king into check
            for i in whiteChecking:
                if wpinning[i]=="b" or wpinning[i]=="r" or wpinning[i]=="q":
                    direction=[]
                    direction.append(self.blackIndexes["K"]/10-self.whiteIndexes[whiteChecking[i]]/10)
                    direction.append(self.blackIndexes["K"]%10-self.whiteIndexes[whiteChecking[i]]%10)
                    self.inCheck2(whiteChecking[i], "w",direction)
                else: 
                    self.inCheck1(whiteChecking[i], "b")
        if bpinning!=[]: 
            for i in bpinning:
                direction=[]
                direction.append(self.blackIndexes["K"]/10-self.blackIndexes[wpinning[i]]/10)#tells you which orientation the piece is checking the king in, only need to compare 1/8 as many squares for a queen 
                direction.append(self.blackIndexes["K"]%10-self.blackIndexes[wpinning[i]]%10)#-, positive or 0 is the only neccessary information here. 
                self.Pinned(wpinned[bpinning[i]], bpinning[i],direction, "w")
        if blackChecking!=[]: 
            for i in blackChecking:
                if bpinning[i]=="b" or wpinning[i]=="r" or wpinning[i]=="q":
                    direction=[]
                    direction.append(self.whiteIndexes["K"]/10-self.blackIndexes[whiteChecking[i]]/10)
                    direction.append(self.whiteIndexes["K"]%10-self.blackIndexes[whiteChecking[i]]%10)
                    self.inCheck2(whiteChecking[i], "w",direction)
                else: 
                    self.inCheck1(whiteChecking[i], "b")


    def Pinned(self, pinned:str,pinning:str, direction:list[int], team: str): #if a piece is pinned, this is called by the all moves function to eliminate moves that put king in check
        goodMoves=[]#later I will copy all the code and switch teams. 
        if team=="w":#white pinning black 
            #direction of row=direction[0], col is [1]
            goodMoves.append(self.whiteIndexes[pinning])#you can take the piece that's pressuring the king and you can move the pieces in the same line between the long range piece and king. 
            if direction[0]>0 and direction[1]>0: 
                for i in range(1,abs(self.blackIndexes[pinned]/10-self.whiteIndexes[pinning]/10)): #positively increasing diagonal, do not include 0 because a move does not include itself 
                    goodMoves.append((self.blackIndexes[pinned]+11))
            elif direction[0]==0 and direction[1]>0: 
                for i in range(1,abs(self.blackIndexes[pinned]%10-self.whiteIndexes[pinning]%10)): #positively increasing horizontal 
                    goodMoves.append((self.blackIndexes[pinned]+i))
            elif direction[0]>0 and direction[1]==0: 
                for i in range(1,abs(self.blackIndexes[pinned]/10-self.whiteIndexes[pinning]/10)): #positively increasing vertical 
                    goodMoves.append((self.blackIndexes[pinned]+10*i))
            elif direction[0]==0 and direction[1]<0: 
                for i in range(1,abs(self.blackIndexes[pinned]%10-self.whiteIndexes[pinning]%10)):  
                    goodMoves.append((self.blackIndexes[pinned]-i))
            elif direction[0]<0 and direction[1]<0: 
                for i in range(1,abs(self.blackIndexes[pinned]/10-self.whiteIndexes[pinning]/10)):  
                    goodMoves.append((self.blackIndexes[pinned]-11*i))
            elif direction[0]>0&direction[1]<0: 
                for i in range(1,abs(self.blackIndexes[pinned]/10-self.whiteIndexes[pinning]/10)):  
                    goodMoves.append((self.blackIndexes[pinned]+9*i))
            elif direction[0]<0 and direction[1]>0: 
                for i in range(1,abs(self.blackIndexes[pinned]/10-self.whiteIndexes[pinning]/10)):  
                    goodMoves.append((self.blackIndexes[pinned]-9))
            else: 
                for i in range(1,abs(self.blackIndexes[pinned]/10-self.whiteIndexes[pinning]/10)):  
                    goodMoves.append((self.blackIndexes[pinned]-10))
            overlap=[]
            for i in goodMoves:
                if goodMoves[i] in self.blackAvailableMoves[pinned]:
                   overlap.append(goodMoves[i])
            self.blackAvailableMoves[pinned]=overlap


        else: #if black is pinning white
            goodMoves.append(self.whiteIndexes[pinning])#you can take the piece that's pressuring the king and you can move the pieces in the same line between the long range piece and king. 
            if direction[0]>0 and direction[1]>0: 
                for i in range(1,abs(self.whiteIndexes[pinned]/10-self.blackIndexes[pinning]/10)): #positively increasing diagonal, do not include 0 because a move does not include itself 
                    goodMoves.append((self.whiteIndexes[pinned]+11))
            elif direction[0]==0 and direction[1]>0: 
                for i in range(1,abs(self.whiteIndexes[pinned]%10-self.blackIndexes[pinning]%10)): #positively increasing horizontal 
                    goodMoves.append((self.whiteIndexes[pinned]+i))
            elif direction[0]>0 and direction[1]==0: 
                for i in range(1,abs(self.whiteIndexes[pinned]/10-self.blackIndexes[pinning]/10)): #positively increasing vertical 
                    goodMoves.append((self.whiteIndexes[pinned]+10*i))
            elif direction[0]==0 and direction[1]<0: 
                for i in range(1,abs(self.whiteIndexes[pinned]%10-self.blackIndexes[pinning]%10)):  
                    goodMoves.append((self.whiteIndexes[pinned]-i))
            elif direction[0]<0 and direction[1]<0: 
                for i in range(1,abs(self.whiteIndexes[pinned]/10-self.blackIndexes[pinning]/10)):  
                    goodMoves.append((self.whiteIndexes[pinned]-11*i))
            elif direction[0]>0&direction[1]<0: 
                for i in range(1,abs(self.whiteIndexes[pinned]/10-self.blackIndexes[pinning]/10)):  
                    goodMoves.append((self.whiteIndexes[pinned]+9*i))
            elif direction[0]<0 and direction[1]>0: 
                for i in range(1,abs(self.whiteIndexes[pinned]/10-self.blackIndexes[pinning]/10)):  
                    goodMoves.append((self.whiteIndexes[pinned]-9))
            else: 
                for i in range(1,abs(self.whiteIndexes[pinned]/10-self.blackIndexes[pinning]/10)):  
                    goodMoves.append((self.whiteIndexes[pinned]-10))
            overlap=[]
            for i in goodMoves:
                if goodMoves[i] in self.whiteaVailableMoves[pinned]:
                   overlap.append(goodMoves[i])
            self.whiteaVailableMoves[pinned]=overlap


    def inCheck1(self,pressuring:str, team:str): #if king is in check from knight or pawn
        #team corresponds to team in check 
        if team=="w": #either has to capture the piece or move the king. 
            for i in self.whitePieces:#if white is in check
                if self.whitePieces[i]=="K": 
                    continue#all moves for king are checked in gen moves function 
                if self.blackIndexes[pressuring] in self.whiteaVailableMoves[self.whitePieces[i]]:#clear moves here
                    for j in self.whiteaVailableMoves[self.whitePieces[i]]:
                        if self.whiteaVailableMoves[self.whitePieces[i]][j]!=self.blackIndexes[pressuring]:
                            self.whiteaVailableMoves[self.whitePieces[i]].remove(j)
                else: 
                    self.whiteaVailableMoves[self.whitePieces[i]]=[]
        else: 
            for i in self.blackPieces:#if white is in check
                if self.blackPieces[i]=="K": 
                    continue#all moves for king are checked in gen moves function 
                if self.whiteIndexes[pressuring] in self.blackAvailableMoves[self.blackPieces[i]]:#clear moves here
                    for j in self.blackAvailableMoves[self.blackPieces[i]]:
                        if self.blackAvailableMoves[self.blackPieces[i]][j]!=self.whiteIndexes[pressuring]:
                            self.blackAvailableMoves[self.blackPieces[i]].remove(j)
                else: 
                    self.blackAvailableMoves[self.blackPieces[i]]=[]


    def inCheck2(self,pressuring:str, team:str, direction:(list[int])): #if getting checked by bishop, knight or rook
        #similar situation to pinning, but has to move in the pinning direction
        goodMoves=[]
        if team=="w":#white checking black 
            goodMoves.append(self.whiteIndexes[pressuring])#you can take the piece that's pressuring the king and you can move the pieces in the same line between the long range piece and king. 
            if direction[0]>0 and direction[1]>0: 
                for i in range(1,abs(self.blackIndexes["K"]/10-self.whiteIndexes[pressuring]/10)): #positively increasing diagonal, do not include 0 because a move does not include itself 
                    goodMoves.append((self.blackIndexes["K"]+11*i))
            elif direction[0]==0 and direction[1]>0: 
                for i in range(1,abs(self.blackIndexes["K"]%10-self.whiteIndexes[pressuring]%10)): #positively increasing horizontal 
                    goodMoves.append((self.blackIndexes["K"]+i))
            elif direction[0]>0 and direction[1]==0: 
                for i in range(1,abs(self.blackIndexes["K"]/10-self.whiteIndexes[pressuring]/10)): #positively increasing vertical 
                    goodMoves.append((self.blackIndexes["K"]+10*i))
            elif direction[0]==0 and direction[1]<0: 
                for i in range(1,abs(self.blackIndexes["K"]%10-self.whiteIndexes[pressuring]%10)):  
                    goodMoves.append((self.blackIndexes["K"]-i))
            elif direction[0]<0 and direction[1]<0: 
                for i in range(1,abs(self.blackIndexes["K"]/10-self.whiteIndexes[pressuring]/10)):  
                    goodMoves.append((self.blackIndexes["K"]-11*i))
            elif direction[0]>0&direction[1]<0: 
                for i in range(1,abs(self.blackIndexes["K"]/10-self.whiteIndexes[pressuring]/10)):  
                    goodMoves.append((self.blackIndexes["K"]+9*i))
            elif direction[0]<0 and direction[1]>0: 
                for i in range(1,abs(self.blackIndexes["K"]/10-self.whiteIndexes[pressuring]/10)):  
                    goodMoves.append((self.blackIndexes["K"]-9))
            else: 
                for i in range(1,abs(self.blackIndexes["K"]/10-self.whiteIndexes[pressuring]/10)):  
                    goodMoves.append((self.blackIndexes["K"]-10))
            for i in self.blackPieces: 
                overLap=[]
                if self.blackPieces[i]=="K": 
                    continue#condition already checked. 
                else:
                    for j in self.blackAvailableMoves[self.blackPieces[i]]:
                        if self.blackAvailableMoves[self.blackPieces[i]][j] in goodMoves: 
                            overLap.append(self.blackAvailableMoves[self.blackPieces[i]][j])#gets rid of all the moves that do not block the check.
                    self.blackAvailableMoves[self.blackPieces[i]]=overLap

                    
        else: 
            goodMoves.append(self.blackIndexes[pressuring])#you can take the piece that's pressuring the king and you can move the pieces in the same line between the long range piece and king. 
            if direction[0]>0 and direction[1]>0: 
                for i in range(1,abs(self.whiteIndexes["K"]/10-self.blackIndexes[pressuring]/10)): #positively increasing diagonal, do not include 0 because a move does not include itself 
                    goodMoves.append((self.whiteIndexes["K"]+11*i))
            elif direction[0]==0 and direction[1]>0: 
                for i in range(1,abs(self.whiteIndexes["K"]%10-self.blackIndexes[pressuring]%10)): #positively increasing horizontal 
                    goodMoves.append((self.whiteIndexes["K"]+i))
            elif direction[0]>0 and direction[1]==0: 
                for i in range(1,abs(self.whiteIndexes["K"]/10-self.blackIndexes[pressuring]/10)): #positively increasing vertical 
                    goodMoves.append((self.whiteIndexes["K"]+10*i))
            elif direction[0]==0 and direction[1]<0: 
                for i in range(1,abs(self.whiteIndexes["K"]%10-self.blackIndexes[pressuring]%10)):  
                    goodMoves.append((self.whiteIndexes["K"]-i))
            elif direction[0]<0 and direction[1]<0: 
                for i in range(1,abs(self.whiteIndexes["K"]/10-self.blackIndexes[pressuring]/10)):  
                    goodMoves.append((self.whiteIndexes["K"]-11*i))
            elif direction[0]>0&direction[1]<0: 
                for i in range(1,abs(self.whiteIndexes["K"]/10-self.blackIndexes[pressuring]/10)):  
                    goodMoves.append((self.whiteIndexes["K"]+9*i))
            elif direction[0]<0 and direction[1]>0: 
                for i in range(1,abs(self.whiteIndexes["K"]/10-self.blackIndexes[pressuring]/10)):  
                    goodMoves.append((self.whiteIndexes["K"]-9))
            else: 
                for i in range(1,abs(self.whiteIndexes["K"]/10-self.blackIndexes[pressuring]/10)):  
                    goodMoves.append((self.whiteIndexes["K"]-10))
            for i in self.whitePieces: 
                overLap=[]
                if self.Pieces[i]=="K": 
                    continue#condition already checked. 
                else:
                    for j in self.whiteaVailableMoves[self.whitePieces[i]]:
                        if self.whiteaVailableMoves[self.whitePieces[i]][j] in goodMoves: 
                            overLap.append(self.whiteaVailableMoves[self.whitePieces[i]][j])#gets rid of all the moves that do not block the check.
                    self.whiteaVailableMoves[self.whitePieces[i]]=overLap


    def move(self, index:int, availableMoveNum:int):#this will only be called after the gen all moves, so you dont have to run it twice 
        if self.turn%2==0: #if it's white's turn.
            if self.whitePieces[i]=="K":
                self.wHasMovedKing=True
            if self.whitePieces[i]=="r1":
                self.wHasMovedR1=True
            if self.whitePieces[i]=="r2":
                self.wHasMovedR2=True
            initialCoords=self.whiteIndexes[self.whitePieces[index]]
            newIndexes=self.whiteaVailableMoves[self.whitePieces[index]][availableMoveNum]
            oldRow=initialCoords/10
            oldCol=initialCoords%10
            newRow=initialCoords/10
            newCol=initialCoords%10
            if newIndexes==99: #king side castle
                self.fullBoard[7][4]=piece(0,'n','n')
                self.fullBoard[7][7]=piece(0,'n','n')
                self.fullBoard[7][6]=piece(0,'K','w')
                self.fullBoard[7][5]=piece(500, 'r', 'w')
                self.whiteIndexes["K"]=76
                self.whiteIndexes["r2"]=75
                self.whiteIToP[76]="K"
                self.whiteIToP[75]="r2"
                self.turn+=1
                return 
            if newIndexes==100: #QSCastle
                self.fullBoard[7][4]=piece(0,'n','n')
                self.fullBoard[7][3]=piece(500,'r','w')
                self.fullBoard[7][2]=piece(0,'K', 'w')
                self.fullBoard[7][0]=piece(0,'n','n')
                self.fullBoard[7][1]=piece(0,'n','n')
                self.whiteIndexes["K"]=72
                self.whiteIndexes["r1"]=73
                self.whiteIToP[72]="K"
                self.whiteIToP[73]="r2"
                self.turn+=1
                return 
            oldpoints=self.fullBoard[newRow][newCol].val#old piece refers to the one that's being captured. 
            if oldpoints>0:#if a black piece is captured 
                boldPiece=self.blackIToP[newIndexes]
                self.blackIndexes.pop([boldPiece])
                self.blackPieces.remove(boldPiece)
                self.blackIToP.pop(newIndexes)
                self.blackPoints-=oldpoints
            if self.fullBoard[newRow][newCol].kind=='p' and newIndexes/10==0:#pawn to queen
                self.fullBoard[newRow][newCol]=piece(900,'q','w')
                self.whitePoints+=800
                for i in range(2,8): 
                    queen="q"
                    newName=queen.join(str(i))
                    if newName in self.whitePieces: #if there are multiple queens 
                        continue 
                    else:
                        self.whitePieces.append(newName)
                        self.whiteIndexes[newName]=newIndexes
                        self.whiteIToP[newIndexes]=newName
                        break
                self.whitePieces.pop(index)
                self.whiteIndexes.pop(self.whitePieces[index])
                self.whiteIToP.pop(initialCoords)
                self.turn+=1
                self.fullBoard[oldRow][oldCol]=piece(0,'n','n')#need to return here, because in this special situation, index map updating is completely different. 
                return
            self.fullBoard[newRow][newCol]=piece.copy(self.fullBoard[oldRow][oldCol])
            self.whiteIndexes[self.whitePieces[index]]=newIndexes
            self.whiteIToP[newIndexes]=self.whitePieces[index]#have to reset all fields to reflect information on the new board. 
            self.fullBoard[initialCoords[0]][initialCoords[1]]=piece(0,'n','n')
            self.turn+=1

        else: #blacks turn 
            if self.blackPieces[index]=="K":
                self.bHasMovedKing=True
            if self.blackPieces[index]=="r1":
                self.bHasMovedR1=True
            if self.blackPieces[index]=="r2":
                self.bHasMovedR2=True
            initialCoords=self.blackIndexes[self.blackPieces[index]]
            newIndexes=self.blackAvailableMoves[self.blackPieces[index]][availableMoveNum]
            oldRow=initialCoords/10
            oldCol=initialCoords%10
            newRow=initialCoords/10
            newCol=initialCoords%10
            if newIndexes==99: #king side castle
                self.fullBoard[0][4]=piece(0,'n','n')
                self.fullBoard[0][7]=piece(0,'n','n')
                self.fullBoard[0][6]=piece(0,'K','b')
                self.fullBoard[0][5]=piece(500, 'r', 'b')
                self.blackIndexes["K"]=76
                self.blackIndexes["r2"]=75
                self.blackIToP[76]="K"
                self.blackIToP[75]="r2"
                self.turn+=1
                return 
            if newIndexes==100: #QSCastle
                self.fullBoard[0][4]=piece(0,'n','n')
                self.fullBoard[0][3]=piece(500,'r','b')
                self.fullBoard[0][2]=piece(0,'K', 'b')
                self.fullBoard[0][0]=piece(0,'n','n')
                self.fullBoard[0][1]=piece(0,'n','n')
                self.blackIndexes["K"]=2
                self.blackIndexes["r1"]=3
                self.blackIToP[2]="K"
                self.blackIToP[3]="r2"
                self.turn+=1
                return 
            oldpoints=self.fullBoard[newRow][newCol].val#old piece refers to the one that's being captured. 
            if oldpoints>0:#if a black piece is captured 
                woldPiece=self.whiteIToP[newIndexes]
                self.whiteIndexes.pop([woldPiece])
                self.whitePieces.remove(woldPiece)
                self.whiteIToP.pop(newIndexes)
                self.whitePoints-=oldpoints
            if self.fullBoard[newRow][newCol].kind=='p' and newRow==7:#pawn to queen
                self.fullBoard[newRow][newCol]=piece(900,'q','w')
                self.blackPoints+=800
                for i in range(2,8): 
                    queen="q"
                    newName=queen.join(str(i))
                    if newName in self.blackPieces: #if there are multiple queens 
                        continue 
                    else:
                        self.blackPieces.append(newName)
                        self.blackIndexes[newName]=newIndexes
                        self.blackIToP[newIndexes]=newName
                        break
                self.blackPieces.pop(index)
                self.blackIndexes.pop(self.whitePieces[index])
                self.blackIToP.pop(initialCoords)
                self.turn+=1
                self.fullBoard[oldRow][oldCol]=piece(0,'n','n')#need to return here, because in this special situation, index map updating is completely different. 
                return
            self.fullBoard[newRow][newCol]=piece.copy(self.fullBoard[oldRow][oldCol])
            self.blackIndexes[self.whitePieces[index]]=newIndexes
            self.blackIToP[newIndexes]=self.blackPieces[index]#have to reset all fields to reflect information on the new board. 
            self.fullBoard[oldRow][initialCoords[1]]=piece(0,'n','n')
            self.turn+=1

    def printBoard(self):
        for i in range(0,7):
            print(i,self.fullBoard[i][0].kind, self.fullBoard[i][1].kind, self.fullBoard[i][2].kind, self.fullBoard[i][3].kind,self.fullBoard[i][4].kind, self.fullBoard[i][5].kind, self.fullBoard[i][6].kind, self.fullBoard[i][7].kind)
        print(" ", "A", "B", "C", "D", "E", "F", "G", "H")

class treeNode: 
    def __init__(self, pgame:board) -> None:
        self.children=(treeNode,treeNode,treeNode,treeNode,treeNode)#list of board classes
        self.level=0
        self.parent=treeNode#previous board 
        self.game=board
def generateTopMoves(currGame:board, numMoves: int): #this function works for either team, so it can simulate human moves. 
    adv={}
    re=[]
    advantageVals=[]
    currGame.allMovesGen()#need to map advantage to top boards 
    placeHolder=currGame.deepClone()
    if currGame.turn==0:
        for i in currGame.whitePieces: 
            for j in currGame.whiteaVailableMoves[currGame.whitePieces[i]]:
                    currGame.move(j,i)
                    currGame.allMovesGen() 
                    currGame.AIAdvantageEval()
                    a=currGame.advantage
                    adv[a]=[i,j]#map advantage parameter to two highest indexes
                    advantageVals.append(a)
        advantageVals.sort(reverse=True)
        for i in range(0,numMoves): 
            currGame.move(adv[advantageVals[i]][0],advantageVals[i][1])
            re.append(currGame)
            currGame=placeHolder
        return re#returns a list of boards 
    else:
        for i in currGame.whitePieces: 
            for j in currGame.blackAvailableMoves[currGame.blackPieces[i]]:
                    currGame.move(j,i)
                    currGame.allMovesGen() 
                    currGame.AIAdvantageEval()
                    a=currGame.advantage
                    adv[a]=[i,j]#map advantage parameter to two highest indexes
                    advantageVals.append(a)
        advantageVals.sort(reverse=True)
        for i in range(0,numMoves): 
            currGame.move(adv[advantageVals[i]][0],advantageVals[i][1])
            re.append(currGame)
            currGame=placeHolder
        return re

def search(currGame:treeNode, depth:int, alphaBeta:int)->int:#Later, I want the depth to be predetermined by what stage of the game it is, earlier=less depth. 
    depth+=depth%2#need to end on an odd # of searches so that it's the players turn. 
    currGame.level+=currGame.parent.level+1
    destroy=False
    miniMax=10000000000
    if currGame.level==depth or currGame.game.gameState!=0:#if game is over, do not branch further on the tree. 
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
        if destroy!=False and currGame.children==[]:
            currGame.children=generateTopMoves(currGame,5)#5 top moves for now, may change this based on how things run
        for i in len(currGame.children): 
            search(currGame.children[i],depth, alphaBeta)#use backtracking/recursion to generate everything. returning will jump to this statement. 
    return miniMax#this parameter is what the AI will base each move on 
def AImove(game:board):
    game.allMovesGen()
    game.AIAdvantageEval()
    if game.gameState!=0:#prevent calling the search function if game is over 
        return
    bestSearch=-100000000
    moveIndexes=(0,0)
    reference=game.deepClone()
    if game.AIteam=="w": #AI team taken from player input
        for i in range(len(game.whitePieces)):
            for j in range(len(game.whiteaVailableMoves[game.whitePieces[j]])): 
                game=reference.deepClone()
                game.move(i,j)
                currSearch=treeNode(game)
                currScore=search(currSearch, 6, -200)
                if bestSearch<currScore: #eventually I want to figure out algorithms for evaluating depth and alphaBeta based on board conditions, but I need to look at runtimes first. 
                    moveIndexes=(i,j)
                    bestSearch=currScore
    else: 
        for i in range(game.blackPieces):
            for j in game.blackAvailableMoves[game.whitePieces[j]]: 
                game=reference.deepClone()
                game.move(i,j)
                currSearch=treeNode(game)
                currScore=search(currSearch, 6, -200)
                if bestSearch<currScore: #eventually I want to figure out algorithms for evaluating depth and alphaBeta based on board conditions, but I need to look at runtimes first. 
                    moveIndexes=(i,j)
                    bestSearch=currScore
    game.move(moveIndexes[0],moveIndexes[1])


def playerMove(game:board):
    game.printBoard() 
    game.allMovesGen()
    game.AIAdvantageEval()
    if game.gameState!=0:
        return
    print("indexes of piece? ex. A4, case sensitive")
    valid=False
    row=-1
    col=-1#need variables to be nonLocal
    newRow=-1
    newCol=-1
    Piece=""
    if game.AIteam=="b":
        while valid==False:
            strInd=input()
            row=ord(strInd[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            row=7-row#indexes of chess board are flipped from array indexing  
            col=ord(strInd[0])-ord('A')#A is col 0, B is col 1, etc. 
            if row*10+col in game.whiteIToP:
                Piece=game.whiteIToP[row*10+col]
                valid=True#needs to map to a value. 
            else: 
                print("Invalid Indexes, please pick a square with a white piece.")
        valid2=False
        while valid2==False: 
            print("Where do you want to move it?")
            strInt=input()
            newRow=ord(strInt[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            newCol=ord(strInt[0])-ord('A')#A is col 0, B is col 1, etc. 
            newRow=7-newRow
            if (newRow, newCol) in game.whiteaVailableMoves[Piece]:
                valid2=True
            else:
                print("Please enter a valid move for this piece.")
        i1=game.whitePieces.index(Piece)
        i2=game.whiteaVailableMoves[Piece].index(Piece)#this could be done more efficiently, because the move function was designed for the AI to do all this quickly, but efficiency in the player move is far less important. 
        game.move(i1,i2)


    else: 
        while valid==False:
            strInd=input()
            row=ord(strInd[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            row=7-row#indexes of chess board are flipped from array indexing  
            col=ord(strInd[0])-ord('A')#A is col 0, B is col 1, etc. 
            if row*10+col in game.blackIToP:
                Piece=game.whiteIToP[row*10+col]
                valid=True#needs to map to a value. 
            else: 
                print("Invalid Indexes, please pick a square with a white piece.")
        valid2=False
        while valid2==False: 
            print("Where do you want to move it?")
            strInt=input()
            newRow=ord(strInt[1])-ord('1')#1 is row zero here, take user input, convert char to int using ascii
            newCol=ord(strInt[0])-ord('A')#A is col 0, B is col 1, etc. 
            newRow=7-newRow
            if (newRow, newCol) in game.blackAvailableMoves[Piece]:
                valid2=True
            else:
                print("Please enter a valid move for this piece.")
        i1=game.whitePieces.index(Piece)
        i2=game.whiteaVailableMoves[Piece].index(Piece)#this could be done more efficiently, because the move function was designed for the AI to do all this quickly, but efficiency in the player move is far less important. 
        game.move(i1,i2)
#main 
theGame=board()
theGame.printBoard()
print("What team would you like to play as? w or b, case sensitive.")
valid=False
while valid==False: 
    playerTeam=input()
    if playerTeam=="b" or playerTeam=="w": 
        valid=True
        if playerTeam=="b":
            theGame.AIteam="w"
        else: 
            theGame.AIteam="b"
    else: 
        print("Invalid Team Input")
if playerTeam=="w":
    while theGame.gameState==0:
        theGame.printBoard()
        playerMove(theGame)
        AImove(theGame)
else: 
    while theGame.gameState==0:
        AImove(theGame)
        theGame.printBoard()
        playerMove()
if theGame.advantage==0: 
    print("It's a draw by stalemate")
elif theGame.advantage>0: 
    print("You lose")
else: 
    print("You win")