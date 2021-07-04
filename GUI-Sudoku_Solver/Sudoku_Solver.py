from tkinter import * 

choice = StringVar()
answer = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
] 
board1 =  [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
        ]
board2 = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]

]


win = Tk()
win.title("Sudoku")
win.geometry("700x800")
win.configure(bg="#1f1f1f")
win.resizable(False,False)
SIDE = 60
WIDTH = 540
HEIGHT = 540
border_thickness = 4


#to check if cell is empty/0 in the sudoku
def empty_box(sudo):
    for i in range(len(sudo)):
        for j in range(len(sudo[0])):
            if sudo[i][j] == 0:
                return (i,j)

#to validate whether the board is right or wrong
def validate_board(sudo,pos,num):
    for i in range(len(sudo[0])):
        if sudo[pos[0]][i] == num and pos[1] != i:
            return False
        
    for i in range(len(sudo)):    
        if sudo[i][pos[1]] == num and pos[0] != i:
             return False

    coord_x = pos[1] // 3
    coord_y = pos[0] // 3

    for i in range(coord_y * 3 , coord_y * 3 + 3):
        for j in range(coord_x * 3 , coord_x * 3 + 3):
            if sudo[i][j] == num and (i, j) == pos:
                return False
    
    return True

#sudoku solver driver function
def solver(sudo):
    empty = empty_box(sudo)
    if not empty:
        return True
    else:
        row , col = empty
        for i in range(10):
            if validate_board(sudo, (row,col), i):

                sudo[row][col] = i

                if solver(sudo):
                    return True

                sudo[row][col] = 0
    
    return False
        

# to find the positions where 0 exists in the sudoku
zero_pos = []
for i in range(9):
    for j in range(9):
        if board1[i][j] == 0:
            zero_pos.append((i,j)) 



# class for creating question sudoku board and input sudoku board function
class dokuSolver(object):
    def __init__(self):
        self.question = []
        self.question = board1

    def game_start(self):
        self.input_board = []
        self.input_board = board2
        

    
# class to create the GUI for the sudoko board 
class dokuUI(Frame):
    def __init__(self,main_screen,doku):
        self.doku = doku
        self.main_screen = main_screen
        Frame.__init__(self,main_screen)
        self.row = -1
        self.col = -1
        self.cur_x = -1
        self.cur_y = -1
        self.item = {}
        self.create_board()

    # basic layout the gui    
    def create_board(self):
        self.sudoku_board = Canvas(win, width= 540, height = 540, bg="white", highlightbackground="black")
        for i in range(9):
            if i%3 == 0 and i != 0 and i != 8:
                self.sudoku_board.create_line(0, i*SIDE, WIDTH+border_thickness, i*SIDE, fill="black", width=2)
            else:
                self.sudoku_board.create_line(0, i*SIDE, WIDTH+border_thickness, i*SIDE, fill="black")  

        for i in range(9):
            if i%3 == 0 and i != 0 and i != 8:
                self.sudoku_board.create_line(i*SIDE, 0, i*SIDE, HEIGHT+border_thickness, fill="black", width=2)
            else:
             self.sudoku_board.create_line(i*SIDE, 0 , i*SIDE, HEIGHT+border_thickness ,fill="black") 

        self.sudoku_board.pack(padx=20,pady=20)

        clear_bt = Button(win, text="Clear", width=8, height=2,command=self.clear_board)
        clear_bt.place(x=75,y=600)

        solve_bt = Button(win, text="Check", width=8, height=2,command=self.is_complete)
        solve_bt.place(x=525,y=600)

        self.sudoku_board.bind("<Button-1>",self._click)
        self.sudoku_board.bind("<Key>",self._keypress)  

        self.create_num_board()
    
    # to draw the layout when the sudoku puzzle is solved successfully
    def draw_won(self):
        x0 = y0 = border_thickness + SIDE * 2
        x1 = y1 = border_thickness + SIDE * 7
        
        self.sudoku_board.create_oval(x0, y0, x1, y1,tags="won", fill="dark orange", outline="orange")
        x = y = border_thickness + 4 * SIDE + SIDE / 2
        self.sudoku_board.create_text(x, y,text="          Sudoku Solved!\nPress clear to restart sudoku", tags="won",fill="white", font=("Arial", 20))
    
    # to check if the board was solved
    def is_complete(self):
        if self.doku.input_board == answer:
            self.draw_won()
        else:
            lb = Label(win,text="Wrong Answer!",fg = "red")
            lb.place(x=300,y=600)
            self.after(2000,lb.destroy)

    # to create the initial question board
    def create_num_board(self):
        self.sudoku_board.delete("que")
        for i in range(9):
            for j in range(9):
                value = self.doku.question[i][j]
                if value != 0: 
                    x = border_thickness + j * SIDE + SIDE/2
                    y = border_thickness + i * SIDE + SIDE/2
                    self.sudoku_board.create_text(x,y,text = value,tags="num",fill="black",font=('Arial','30','bold'))

    
    # to input values in the empty cells
    def fill_empty(self):
        value = self.doku.input_board[self.row][self.col]
        if value != 0 : 
            x = border_thickness + self.col * SIDE + SIDE/2
            y = border_thickness + self.row * SIDE + SIDE/2
            if (self.cur_x,self.cur_y) != (self.row,self.col) and (x,y) not in self.item :
                self.item[(x,y)] = self.sudoku_board.create_text(x,y,text = value,tags="temp",fill= "SteelBlue1" ,font=('Arial','30','bold'))
                self.cur_x,self.cur_y = self.row,self.col
            else:
                self.sudoku_board.delete(self.item[(x,y)])
                self.item[(x,y)] = self.sudoku_board.create_text(x,y,text = value,tags="temp",fill= "SteelBlue1" ,font=('Arial','30','bold'))


    # to draw the outline when a cell is clicked
    def design_pointer(self):
        self.sudoku_board.delete("pointer")
        if(self.row >= 0 and self.col >= 0):
            x1 =  self.col * SIDE 
            x2 =  (self.col + 1) * SIDE
            y1 =  self.row * SIDE 
            y2 =  (self.row + 1) * SIDE 
            self.sudoku_board.create_rectangle(x1,y1,x2,y2,outline="red",tags="pointer",width=3)

    #to clear the entered numbers in the board
    def clear_board(self):
        self.sudoku_board.delete("won")
        self.sudoku_board.delete("temp") 
        self.design_pointer()
        for (i,j) in zero_pos:
            self.doku.input_board[i][j] = 0

    # to update the value of the input board whenever a number is added in the cell
    def _keypress(self,event):
        if self.row >= 0 and self.col >= 0 and event.char in "123456789":
            self.doku.input_board[self.row][self.col] = int(event.char)
            self.fill_empty()

    # to identify where the mouse click happended to identify the cell locations
    def _click(self,event):
        a, b = event.x , event.y
        if(border_thickness < a < WIDTH - border_thickness and border_thickness< b < HEIGHT - border_thickness):
            self.sudoku_board.focus_set()

            x , y = int((b - border_thickness)/SIDE) , int((a - border_thickness)/SIDE)
            if (self.row, self.col) == (x,y):
                self.row, self.col = -1, -1
            elif self.doku.question[x][y] == 0:
                self.row, self.col = x, y
        else:
            self.row , self.col = -1 , -1

        self.design_pointer()
        
# program's main driver function
if __name__ == '__main__':
    solver(answer)
    game = dokuSolver()
    game.game_start()
    dokuUI(win,game)
    win.mainloop()



