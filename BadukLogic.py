import numpy as np
from copy import deepcopy

class Board :
    def __init__(self):
        self.BlackStones = np.zeros( (9, 9) )
        self.WhiteStones = np.zeros( (9, 9) )
        self.Neutral = np.ones( (9, 9) )



    def get_color (self, x ,y):
        if self.Neutral[ x, y ] == 1 :
            return 0
        if self.BlackStones[x ,y] == 1 :
            return 1
        return 2
    
    def get_neighbours (self, x, y):
        ans = []
        if x > 0 :
            ans.append( (x-1 , y)  )
        if x < 8 :
            ans.append( (x+1 , y) )
        if y > 0 :
            ans.append( (x, y-1) )
        if y < 8 :
            ans.append( (x, y+1) )
        return ans

    def capture_group (self, x, y):
        visited = np.zeros( (9,9) )
        stones = []
        color = self.get_color(x , y)
        
        def dfs( x, y ):
            stones.append( (x , y) )
            visited[x ,y ] = 1

            neighbours = self.get_neighbours( x, y)

            for point in neighbours:
                x1, y1 = point
                if self.get_color( x1 , y1 ) == color and visited[ x1, y1 ] == 0 :
                    dfs ( x1 , y1 )

        
        dfs( x, y)
        for pos in stones:
            self.Neutral[ pos[0] , pos[1] ] = 1 
            if color == 1 :
                self.BlackStones[ pos[0] , pos[1]  ] = 0
            else:
                self.WhiteStones[ pos[0] , pos[1] ] = 0
    
    def count_dame(self, x, y ):
        NeutralPoints = np.zeros( (9, 9) )
        visited = np.zeros( (9,9) )
        color = self.get_color(x , y)

        def dfs( x, y):
            visited[ x, y] = 1
            neighbours = self.get_neighbours( x, y)

            for point in neighbours:
                x1, y1 = point
                if self.get_color( x1 , y1 ) == 0 :
                    NeutralPoints[x1 , y1] = 1 
                if self.get_color( x1 , y1 ) == color and visited[ x1, y1 ] == 0 :
                    dfs ( x1, y1)        
        dfs( x, y)
        return np.sum( NeutralPoints )
    
    def make_move(self, x, y, color):
        self.Neutral[x , y] = 0
        if color == 1:
            self.BlackStones[x, y] = 1
        else :
            self.WhiteStones[x , y ] = 1
        neighbours = self.get_neighbours( x, y)
        
        for point in neighbours:
            x1, y1 = point
            color1 = self.get_color(x1, y1)
            if color1 != color :
                dame = self.count_dame( x1, y1)
                if dame == 0 :
                    self.capture_group( x1, y1 )

        for point in neighbours:
            x1, y1 = point
            color1 = self.get_color(x1, y1)
            if color1 == color :
                dame = self.count_dame( x1, y1)
                if dame == 0 :
                    self.capture_group( x1, y1 )
        
        dame = self.count_dame( x, y )
        if dame == 0:
            self.capture_group(x, y)    
    
    def split_stones( self) :
        BlackMarker = deepcopy( self.BlackStones )
        WhiteMarker = deepcopy( self.WhiteStones )
        NeutralMarker = deepcopy( self.Neutral )
        visited = np.zeros( (9 , 9) )

        
        buf = []

        def dfs(x, y ):
            visited[ x, y] = 1
            buf.append( (x, y) )
            flagBlack, flagWhite = False, False
            neighbours = self.get_neighbours( x, y)
            for point in neighbours:
                x1, y1 = point
                fb, fw = False, False
                if visited[x1 , y1 ] == 0 and NeutralMarker[x1, y1] == 1:
                    fb, fw = dfs(x1, y1)
                if fb or BlackMarker[x1, y1] == 1 :
                    flagBlack = True
                if fw or WhiteMarker[x1, y1] == 1 :
                    flagWhite = True
            return flagBlack, flagWhite

        for x in range(9):
            for y in range(9):
                if NeutralMarker[x, y] == 1 and visited[x, y] == 0:
                    fb, fw = dfs( x, y)
                    if fb and not fw:
                        for point in buf:
                            BlackMarker[ point[0] , point[1] ] = 1
                            NeutralMarker[ point[0] , point[1] ] = 0
                    if fw and not fb:
                        for point in buf:
                            WhiteMarker[ point[0] , point[1] ] = 1
                            NeutralMarker[ point[0] , point[1] ] = 0
                    buf.clear()
                   
        
        return BlackMarker, WhiteMarker, NeutralMarker
    
    def GamePos2Tuple(self):
        tupleB = tuple( map(tuple, self.BlackStones ) )
        tupleW = tuple( map( tuple, self.WhiteStones ) )
        tupleN = tuple( map( tuple, self.Neutral ))
        tupleFinal = tuple( [ tupleB, tupleW, tupleN ] )
        return tupleFinal







        
