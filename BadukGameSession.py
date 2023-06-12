import numpy as np
from copy import deepcopy
from BadukLogic import *

class BadukGame:
    def __init__(self, komi = 6.5 ):
        self.currBoard = Board()
        self.komi = komi
        self.currPlayer = 1
        self.BlackPass = False
        self.WhitePass = False
        
        self.listPositionTuple = []
        self.listPositionTuple.append( self.currBoard.GamePos2Tuple() )


    def changePlayer(self):
        self.currPlayer = 3 - self.currPlayer

    def GameEnd (self):
        return self.BlackPass and self.WhitePass

    def calculateResult(self):
        BlackMarker, WhiteMarker, _ = self.currBoard.split_stones()
        BlackScore = np.sum(BlackMarker)
        WhiteScore = np.sum(WhiteMarker)
        result = BlackScore - ( WhiteScore + self.komi )
        return BlackMarker, WhiteMarker, result
    
    def checkPossibilityMove( self, x, y ):
        BoardCopy = deepcopy(self.currBoard)
        if BoardCopy.Neutral[x , y] == 0:
            return False, BoardCopy
        BoardCopy.make_move( x, y, self.currPlayer )
        if BoardCopy.GamePos2Tuple() in self.listPositionTuple:
            return False, BoardCopy
        return True, BoardCopy
    
    def makeMove(self, x, y, flagPass = False):
        if flagPass:
            if self.currPlayer == 1:
                self.BlackPass = True
            else:
                self.WhitePass = True
            self.changePlayer()
            return True
        flag, resBoard = self.checkPossibilityMove( x, y)
        if flag :
            self.changePlayer()
            self.currBoard = resBoard
            self.listPositionTuple.append(resBoard.GamePos2Tuple())
        return flag

    
