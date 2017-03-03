"""
    Author: Dominik Suwala <dxs9411@rit.edu>
    This is a Python implementation of Conway's Game of Life for Datto.
    Specific to Python 2.x (tested on 2.7.12)
"""

import os, sys

class ConwayGameOfLife():
    
    _model = None
    fc = None
    
    """
    Initializes the object 
    """
    def __init__( self, filename ):
        self.fc = self.readFromFile( filename )
    
    """
    Prints the grid with current states
    """
    
    def __str__( self ):
        dimension = len( self._model )
        out = []
        for r in range( dimension ):
            bools = [ self._model[ r ][ c ] for c in range( dimension ) ]
            bools = map( str, map( int, bools ) )
            out.append( ''.join( bools ) )
        return '\n'.join( out )
    
    """
    Return file contents read from an input file
    """
    def getFC( self ):
        return self.fc
    
    """
    Updates to a new model (i.e. one generation to the next)
    """
    def setModel( self, model ):
        self._model = model
    
    """
    Implements Conways' Game of Life rules to yield the next generation of
    living cells
    """
    def nextGeneration( self ):
        curGen = self._model
        dimension = len( curGen )
        nextGen = self.array2d( dimension, dimension )
        # Deviation pattern for neighbor search
        deviate = [ -1, 0, 1 ]
        deviations = []
        for num1 in deviate:
            for num2 in deviate:
                # ignore self from being considered a neighbor
                if( not( 0 == num1 == num2 ) ):
                    deviations.append( [ num1, num2 ] )
        
        # Indicate criteria to continue life in next epoch
        continueLifeCriteria = [ 2, 3 ]
        
        # Populate the next generation based on rules as a function of
        # neighbor count
        for row in range( dimension ):
            for col in range( dimension ):
                curNeighborBools = []
                for interaction in deviations:
                    dX = interaction[ 0 ] + row
                    dY = interaction[ 1 ] + col
                    
                    # Python allows negative indexing that starts from right
                    # edge of array.
                    if( dX >= 0 and dY >= 0 ):
                        try:
                            curNeighborBools.append(
                                curGen[ dX ][ dY ] )
                        except:
                            pass
                livingNeighbors = curNeighborBools.count( True )
                
                # Living cell logic
                if( curGen[ row ][ col ] ):
                    if livingNeighbors in continueLifeCriteria:
                        nextGen[ row ][ col ] = True
                    else:
                        nextGen[ row ][ col ] = False
                # Dead cell logic
                else:
                    if livingNeighbors == 3:
                        nextGen[ row ][ col ] = True
                    else:
                        nextGen[ row ][ col ] = False
        
        return nextGen
        
    """
    Initializes a 2D array
    """

    def array2d( self, rows, cols ):
        return [ [ False for c in range( cols ) ] for r in range( rows ) ]
    
    """
    Read a file to string
    """
    def readFromFile( self, filename ):
        try:
            fc = open( filename, 'r' ).read().replace( '\r', '' )
            return fc
        except:
            return None
    """
    Populate the model representation from a string
    """
    def populateBoard( self ):
        rows = self.getFC().strip().split( '\n' )
        expectDim = len( rows )
        
        rowi = 0
        
        curGen = self.array2d( expectDim, expectDim )
        for row in rows:
            curBoolRow = map( bool, map( int, row ) )
            if( len( curBoolRow ) != expectDim ):
                print >> sys.stderr, 'Input is not a square 2D array', len( curBoolRow )
                sys.exit( 0xBAD )
            for c in range( len( row ) ):   
                curGen[ rowi ][ c ] = curBoolRow[ c ]
            
            rowi += 1
        
        self._model = curGen
    
def main():
    filename = None
    if( len( sys.argv ) > 1 ):
        filename = sys.argv[ 1 ]    
    else:
        print >> sys.stderr, 'err: An input filename is required as an arugment'
        sys.exit( 0xBADDEF )
    game = ConwayGameOfLife( filename )
    
    if( game.getFC() == None ):
        print >> sys.stderr, 'err: Could not read file', filename
        sys.exit( 0xBADFEED )
    
    game.populateBoard()
    game.setModel( game.nextGeneration() )
    print game
    
    loop = False
    
    if loop:
        while( True ):
            game.setModel( game.nextGeneration() )
            raw_input()
            print game, '\n---'
    
if __name__ == '__main__':
    main()