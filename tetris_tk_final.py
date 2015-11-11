#!/usr/bin/env python

"""
Tetris Tk - A tetris clone written in Python using the Tkinter GUI library.

Controls:
    Left Arrow      Move left
    Right Arrow     Move right
    Down Arrow      Move down
    Up Arrow        Drop Tetronimoe to the bottom
    'a'             Rotate anti-clockwise (to the left)
    'b'             Rotate clockwise (to the right)
    'p'             Pause the game.
TODO: endgame func
TODO: timer from sys time, offset, endtime-starttime
"""

from Tkinter import *
from time import sleep
from random import randint
import time
import excel_data.output
import excel_data.make_workbook
import excel_data.survey_ans
import survey.survey
import tkSimpleDialog
import tkMessageBox
import sys

SCALE = 20
OFFSET = 3
MAXX = 10
MAXY = 22

NO_OF_LEVELS = 10

LEFT = "left"
RIGHT = "right"
DOWN = "down"

SESSION = 0 #USE THIS TO DETERMINE GAME STATE
             # take [SESSION]list

#index into these by SESSION in order to deternine which conditions are being used
STATE1 = [1, 2, 3, 4, 5, 6]
STATE2 = [1, 5, 2, 3, 4, 6]
STATE3 = [1, 4, 5, 2, 3, 6]
STATE4 = [1, 3, 4, 5, 3, 6]

LIST= STATE2 #### CHANGE THIS TO DIFFERENT STATE FOR COUNTERBALANCING
STRING_LIST= "STATE2"  ### DONT FORGET TO CHANGE THIS TOO

SUBJECT_NUM = 420.4  # CHANGE THIS FOR EVERY SUBJECT- format by birth month, birthday, decimal, state i.e.: 627.1

direction_d = { "left": (-1, 0), "right": (1, 0), "down": (0, 1) }
(BOOK, SHEET, SHEETNAME) = excel_data.make_workbook.make_workbook(SUBJECT_NUM, STRING_LIST)

def level_thresholds( first_level, no_of_levels ):
    """
    Calculates the score at which the level will change, for n levels.
    """
    thresholds =[]
    for x in xrange( no_of_levels ):
        multiplier = 2**x
        thresholds.append( first_level * multiplier )
    
    return thresholds

class status_bar( Frame ):
    """
    Status bar to display the score and level
    """
    def __init__(self, parent):
        Frame.__init__( self, parent )
        self.label = Label( self, bd=1, relief=SUNKEN, anchor=W )
        self.label.pack( fill=X )
        
    def set( self, format, *args):
        self.label.config( text = format % args)
        self.label.update_idletasks()
        
    def clear( self ):
        self.label.config(test="")
        self.label.update_idletasks()

class Board( Frame ):

    """

    The board represents the tetris playing area. A grid of x by y blocks.

    """
    
    def __init__(self, parent, scale=20, max_x=10, max_y=20, offset=3, fill = "grey"):


        """

        Init and config the tetris board, default configuration:

        Scale (block size in pixels) = 20

        max X (in blocks) = 10

        max Y (in blocks) = 20

        offset (in pixels) = 3

        """
        Frame.__init__(self, parent)


        # blocks are indexed by there corrdinates e.g. (4,5), these are

        self.landed = {}

        self.parent = parent

        self.scale = scale

        self.max_x = max_x

        self.max_y = max_y

        self.offset = offset



        self.canvas = Canvas(parent, height=900, width=1440)

        self.canvas.pack()

        self.canvas.create_rectangle(600,80,805,545, fill="grey")

    def check_for_complete_row( self, blocks ):
        """
        Look for a complete row of blocks, from the bottom up until the top row
        or until an empty row is reached.
        """
        rows_deleted = 0
        
        # Add the blocks to those in the grid that have already 'landed'
        for block in blocks:
            self.landed[ block.coord() ] = block.id
        
        empty_row = 0

        # find the first empty row
        for y in xrange(self.max_y -1, -1, -1):
            row_is_empty = True
            for x in xrange(self.max_x):
                if self.landed.get((x,y), None):
                    row_is_empty = False
                    break;
            if row_is_empty:
                empty_row = y
                break

        # Now scan up and until a complete row is found. 
        y = self.max_y - 1
        while y > empty_row:
 
            complete_row = True
            for x in xrange(self.max_x):
                if self.landed.get((x,y), None) is None:
                    complete_row = False
                    break;

                    break;

                    break;

                    break;

                    break;

                    break;

            if complete_row:
                rows_deleted += 1
                
                #delete the completed row
                for x in xrange(self.max_x):
                    block = self.landed.pop((x,y))
                    self.delete_block(block)
                    del block

                    
                # move all the rows above it down
                for ay in xrange(y-1, empty_row, -1):
                    for x in xrange(self.max_x):
                        block = self.landed.get((x,ay), None)
                        if block:
                            block = self.landed.pop((x,ay))
                            dx,dy = direction_d[DOWN]
                            
                            self.move_block(block, direction_d[DOWN])
                            self.landed[(x+dx, ay+dy)] = block

                # move the empty row down index down too
                empty_row +=1
                # y stays same as row above has moved down.
                
            else:
                y -= 1
                
        #self.output() # non-gui diagnostic
        
        # return the score, calculated by the number of rows deleted.  
        if LIST[SESSION] == 3:
            return (500 * rows_deleted) * rows_deleted # this happens only on the 3th session
        else:      
            return (100 * rows_deleted) * rows_deleted ### CHANGE THIS NUMBER TO INCREASE POINTS RATE- done and done
                
    def output( self ):
        for y in xrange(self.max_y):
            line = []
            for x in xrange(self.max_x):
                if self.landed.get((x,y), None):
                    line.append("X")
                else:
                    line.append(".")
            print "".join(line)
            
    def add_block( self, (x, y), colour):
        """
        Create a block by drawing it on the canvas, return
        it's ID to the caller.
        """
        rx = (x * self.scale) + self.offset
        ry = (y * self.scale) + self.offset
        return self.canvas.create_rectangle(

            rx + 600, ry + 100, rx+self.scale+600, ry+self.scale+100, fill=colour

        )
        
    def move_block( self, id, coord):
        """
        Move the block, identified by 'id', by x and y. Note this is a
        relative movement, e.g. move 10, 10 means move 10 pixels right and
        10 pixels down NOT move to position 10,10. 
        """
        x, y = coord
        self.canvas.move(id, x*self.scale, y*self.scale)
        
    def delete_block(self, id):
        """
        Delete the identified block
        """
        self.canvas.delete( id )
        
    def check_block( self, (x, y) ):
        """
        Check if the x, y coordinate can have a block placed there.
        That is; if there is a 'landed' block there or it is outside the
        board boundary, then return False, otherwise return true.
        """
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            return False
        elif self.landed.has_key( (x, y) ):
            return False
        else:
            return True

class Block(object):
    def __init__( self, id, (x, y)):
        self.id = id
        self.x = x
        self.y = y
        
    def coord( self ):
        return (self.x, self.y)
        
class shape(object):
    """
    Shape is the  Base class for the game pieces e.g. square, T, S, Z, L,
    reverse L and I. Shapes are constructed of blocks. 
    """
    @classmethod        
    def check_and_create(cls, board, coords, colour ):
        """
        Check if the blocks that make the shape can be placed in empty coords
        before creating and returning the shape instance. Otherwise, return
        None.
        """
        for coord in coords:
            if not board.check_block( coord ):
                return None
        
        return cls( board, coords, colour)
            
    def __init__(self, board, coords, colour ):
        """
        Initialise the shape base.
        """
        self.board = board
        self.blocks = []
        
        for coord in coords:
            block = Block(self.board.add_block( coord, colour), coord)
            
            self.blocks.append( block )
            
    def move( self, direction ):
        """
        Move the blocks in the direction indicated by adding (dx, dy) to the
        current block coordinates
        """
        d_x, d_y = direction_d[direction]
        
        for block in self.blocks:

            x = block.x + d_x
            y = block.y + d_y
            
            if not self.board.check_block( (x, y) ):
                return False
            
        for block in self.blocks:
            
            x = block.x + d_x
            y = block.y + d_y
            
            self.board.move_block( block.id, (d_x, d_y) )
            
            block.x = x
            block.y = y
        
        return True
            
    def rotate(self, clockwise = True):
        """
        Rotate the blocks around the 'middle' block, 90-degrees. The
        middle block is always the index 0 block in the list of blocks
        that make up a shape.
        """
        # TO DO: Refactor for DRY
        middle = self.blocks[0]
        rel = []
        for block in self.blocks:
            rel.append( (block.x-middle.x, block.y-middle.y ) )
            
        # to rotate 90-degrees (x,y) = (-y, x)
        # First check that the there are no collisions or out of bounds moves.
        for idx in xrange(len(self.blocks)):
            rel_x, rel_y = rel[idx]
            if clockwise:
                x = middle.x+rel_y
                y = middle.y-rel_x
            else:
                x = middle.x-rel_y
                y = middle.y+rel_x
            
            if not self.board.check_block( (x, y) ):
                return False
            
        for idx in xrange(len(self.blocks)):
            rel_x, rel_y = rel[idx]
            if clockwise:
                x = middle.x+rel_y
                y = middle.y-rel_x
            else:
                x = middle.x-rel_y
                y = middle.y+rel_x
            
            
            diff_x = x - self.blocks[idx].x 
            diff_y = y - self.blocks[idx].y 
            
            self.board.move_block( self.blocks[idx].id, (diff_x, diff_y) )
            
            self.blocks[idx].x = x
            self.blocks[idx].y = y
       
        return True
    
class shape_limited_rotate( shape ):
    """
    This is a base class for the shapes like the S, Z and I that don't fully
    rotate (which would result in the shape moving *up* one block on a 180).
    Instead they toggle between 90 degrees clockwise and then back 90 degrees
    anti-clockwise.
    """
    def __init__( self, board, coords, colour ):
        self.clockwise = True
        super(shape_limited_rotate, self).__init__(board, coords, colour)
    
    def rotate(self, clockwise=True):
        """
        Clockwise, is used to indicate if the shape should rotate clockwise
        or back again anti-clockwise. It is toggled.
        """
        super(shape_limited_rotate, self).rotate(clockwise=self.clockwise)
        if self.clockwise:
            self.clockwise=False
        else:
            self.clockwise=True
        

class square_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(4,0),(5,0),(4,1),(5,1)]
        return super(square_shape, cls).check_and_create(board, coords, "red")
        
    def rotate(self, clockwise=True):
        """
        Override the rotate method for the square shape to do exactly nothing!
        """
        pass
        
class t_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(4,0),(3,0),(5,0),(4,1)]
        return super(t_shape, cls).check_and_create(board, coords, "yellow" )
        
class l_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(4,0),(3,0),(5,0),(3,1)]
        return super(l_shape, cls).check_and_create(board, coords, "orange")
    
class reverse_l_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(5,0),(4,0),(6,0),(6,1)]
        return super(reverse_l_shape, cls).check_and_create(
            board, coords, "green")
        
class z_shape( shape_limited_rotate ):
    @classmethod
    def check_and_create( cls, board ):
        coords =[(5,0),(4,0),(5,1),(6,1)]
        return super(z_shape, cls).check_and_create(board, coords, "purple")
        
class s_shape( shape_limited_rotate ):
    @classmethod
    def check_and_create( cls, board ):
        coords =[(5,1),(4,1),(5,0),(6,0)]
        return super(s_shape, cls).check_and_create(board, coords, "magenta")
        
class i_shape( shape_limited_rotate ):
    @classmethod
    def check_and_create( cls, board ):
        coords =[(4,0),(3,0),(5,0),(6,0)]
        return super(i_shape, cls).check_and_create(board, coords, "blue")
        
class game_controller(object):
    """
    Main game loop and receives GUI callback events for keypresses etc...
    """
    def __init__(self, parent):
        """
        Intialise the game...
        """

        self.parent = parent
        self.score = 0
        self.level = 0  #dependent on self.level, increase speed (make new file for this)
        self.delay = 800    #ms   # this lil piece of shit is the delay betwn piece moves (so, speed)
        self.starttime = time.time() #use to track playtime
        self.endtime = 0
        self.totaltime = 0
        #lookup table
        self.shapes = [square_shape,
                      t_shape,
                      l_shape,
                      reverse_l_shape,
                      z_shape,
                      s_shape,
                      i_shape ]
        
        self.thresholds = level_thresholds( 500, NO_OF_LEVELS )
        
        self.status_bar = status_bar( parent )
        self.status_bar.pack(side=TOP,fill=X)
        #print "Status bar width",self.status_bar.cget("width")

        self.status_bar.set("Score: %-7d\t Level: %d " % (
            self.score, self.level+1)
        )
        
        self.board = Board(
            parent,
            scale=SCALE,
            max_x=MAXX,
            max_y=MAXY,
            offset=OFFSET
            )
        
        self.board.pack(side=BOTTOM)
        
        self.parent.bind("<Left>", self.left_callback)
        self.parent.bind("<Right>", self.right_callback)
        self.parent.bind("<space>", self.up_callback)
        self.parent.bind("<Down>", self.down_callback)
        self.parent.bind("<Up>", self.a_callback)
        self.parent.bind("s", self.s_callback)
        self.parent.bind("p", self.p_callback)
         
        self.shape = self.get_next_shape()
        #self.board.output()
        self.after_id = self.parent.after( self.delay, self.move_my_shape )

    def endGame(self):
        self.endtime = time.time()
        self.totaltime = self.endtime - self.starttime
        global SESSION
        SESSION += 1
        #print(SESSION)
        self.checkSESSION()
        Toplevel().destroy()
        self.parent.destroy()
        if LIST[SESSION] == 6:
            sys.exit()
        root = Tk()
        root.title("Tetris Tk")
        theGame = game_controller(root)
        root.mainloop()

    def checkSESSION(self):
        global SESSION
        self.checkIn()

    def writeData(self, BOOK, SHEET, SHEETNAME, SESSION): #TODO: change this to use SESSION as an arg and translate that to the row # to write to
        scoreNoSpeed = self.score
        levelNoSpeed = self.level
        timeNoSpeed = self.totaltime
        enjoyNoSpeed = self.enjoyNoSpeed
        subject_num = SUBJECT_NUM
        excel_data.output.write_data_noSpeed(BOOK, SHEET, SHEETNAME, SESSION, subject_num, scoreNoSpeed,
                                             levelNoSpeed, enjoyNoSpeed, timeNoSpeed)

    def checkIn(self):
        tkMessageBox.showwarning(title="SESSION ENDED",
                                 message ="Score: %7d\tLevel: %d\n Ready to move on?" % ( self.score, self.level),
                           parent=self.parent)
        self.enjoyNoSpeed = tkSimpleDialog.askinteger(title='Question', prompt="On a scale from 1 to 7 with 1 being not enjoyable at all, and 7 being as enjoyable as possible, how fun was this?")
        survey_ans = survey.survey.survey()
        self.writeData(BOOK, SHEET,SHEETNAME, SESSION)
        excel_data.survey_ans.write_survey_ans(BOOK, SHEET, SHEETNAME, survey_ans, SESSION)


    def handle_move(self, direction):
        #this lil bit only for time capped trial
        if LIST[SESSION] == 4:
            if time.time()-self.starttime >= 120: #let play go for two minutes
                self.endGame()
        #if you can't move then you've hit something
        if not self.shape.move( direction ):
 
            # if your heading down then the shape has 'landed'
            if direction == DOWN:
                self.score += self.board.check_for_complete_row(
                    self.shape.blocks
                    )
                del self.shape
                self.shape = self.get_next_shape()
                
                # If the shape returned is None, then this indicates that
                # that the check before creating it failed and the
                # game is over!
                if self.shape is None:
                   self.endGame()
                # do we go up a level?
                if (self.level < NO_OF_LEVELS and 
                    self.score >= self.thresholds[ self.level]):
                    self.level+=1
                    if LIST[SESSION] == 5:
                        #print("WE'RE SPEEDIN' UP")
                        self.delay-=100 #HERE HE IS RIGHT HERE LIL SHIT I FOUND U
                   
                self.status_bar.set("Score: %-7d\t Level: %d " % (
                    self.score, self.level+1)
                )
                
                # Signal that the shape has 'landed'
                return False
        return True
    
    

    def left_callback(self, event):
        if self.shape:
            self.handle_move( LEFT )
        
    def right_callback( self, event ):
        if self.shape:
            self.handle_move( RIGHT )

    def up_callback( self, event ):
        if self.shape:
            # drop the tetrominoe to the bottom
            while self.handle_move( DOWN ):
                pass

    def down_callback( self, event ):
        if self.shape:
            self.handle_move( DOWN )
            
    def a_callback( self, event):
        if self.shape:
            self.shape.rotate(clockwise=True)
            
    def s_callback( self, event):
        if self.shape:
            self.shape.rotate(clockwise=False)
        
    def p_callback(self, event):
        self.parent.after_cancel( self.after_id )
        tkMessageBox.askquestion(
            title = "Paused!",
            message = "Continue?",
            type=tkMessageBox.OK)
        self.after_id = self.parent.after(self.delay,
                                          self.move_my_shape)
    def move_my_shape(self):
        if self.shape:
            self.handle_move(DOWN)
            self.after_id = self.parent.after(self.delay, self.move_my_shape)# i think mayhaps if I change the delay? it will speed up?

    def get_next_shape(self):
        """
        Randomly select which teromino will be used next.
        """
        the_shape = self.shapes[randint(0, len(self.shapes)-1)]
        return the_shape.check_and_create(self.board)

if __name__ == "__main__":
    root = Tk()
    root.title("Tetris Tk")
    tkMessageBox.askquestion(
            title = "New Game Ready!",
            message = "Ready to start?",
            type=tkMessageBox.OK)
    theGame = game_controller(root) 
    root.mainloop()
