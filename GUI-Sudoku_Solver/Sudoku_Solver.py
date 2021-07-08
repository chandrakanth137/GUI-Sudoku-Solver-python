from tkinter import *  
from tkinter import messagebox
import copy

# to find the empty cells in the sudoku
def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if(arr[row][col]== 0):
                l[0]= row
                l[1]= col
                return True
    return False

# to check if the input value already exists or not in that row 
def used_in_row(arr, row, num):
    for i in range(9):
        if(arr[row][i] == num):
            return True
    return False

# to check if the input value already exists or not in that column  
def used_in_col(arr, col, num):
    for i in range(9):
        if(arr[i][col] == num):
            return True
    return False
 
# to check if that value is used already exists in the 3x3 grid or not
def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if(arr[i + row][j + col] == num):
                return True
    return False

# to check if value is fit enough to be in that cell 
def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3, col - col % 3, num)

# sudoku solver driver function
def solver(arr):
    l =[0, 0]
     
    if(not find_empty_location(arr, l)):
        return True

    row = l[0]
    col = l[1]
     
    for num in range(1, 10):
         
        if(check_location_is_safe(arr,
                          row, col, num)):
             
            arr[row][col]= num
 
            if(solver(arr)):
                return True
 
            arr[row][col] = 0
                  
    return False

# Global variables        
win = Tk()
win.title("Sudoku")
win.geometry("700x760")
win.configure(bg="#1f1f1f")
win.resizable(False,False)
SIDE = 60
WIDTH = 540
HEIGHT = 540
border_thickness = 4

# class for creating question sudoku board and input sudoku board function
class dokuSolver(object):
    def __init__(self):
        self.question = []

    def game_start(self):
        self.input_board = []
        self.answer = [] 
            
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
        self.choice = StringVar()
        self.create_board()
        
# to choose the board from respective text files
    def submit_board(self):
        bo = ['1','2','3','4']
        li1= []
        if self.choice.get() in bo:
            with open("%s.txt" % self.choice.get(),'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line[-1] == '\n':
                        li1.append(list(map(int,line[:-1])))
                    else:
                        li1.append(list(map(int,line[:])))
            
            self.doku.answer = copy.deepcopy(li1)
            self.doku.question = copy.deepcopy(li1)
            self.doku.input_board = copy.deepcopy(li1)
            self.menu.destroy()
            self.lb.destroy()
            self.bt.destroy()
            self.e.destroy()
            solver(self.doku.answer)
            self.create_num_board()
        else:
            self.menu.destroy()
            self.lb.destroy()
            self.bt.destroy()
            self.e.destroy()
            messagebox.showinfo('Invalid Choice','Entered value out of range')
            self.board_selection()

    # to create a window to choose the question
    def board_selection(self):
        self.menu = Canvas(win,width=300,height=130,bg="black",highlightbackground="red")
        self.menu.place(x = 200 ,y =150)
        self.lb = Label(win,text = "Choose Board.\nEnter number between 1 - 4",fg='white',bg='black')
        self.bt = Button(win,text="Submit",width=20,height=1,command=self.submit_board,highlightbackground='black')
        self.e = Entry(win,textvariable = self.choice,width=30,bg='black',fg='white')
        self.lb.place(x = 253,y = 155)
        self.bt.place(x = 240,y=240)
        self.e.place(x=212,y=205)
    
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
        self.board_selection()

    # to draw the layout when the sudoku puzzle is solved successfully
    def draw_won(self):
        x0 = y0 = border_thickness + SIDE * 2
        x1 = y1 = border_thickness + SIDE * 7
        
        self.sudoku_board.create_oval(x0, y0, x1, y1,tags="won", fill="dark orange", outline="orange")
        x = y = border_thickness + 4 * SIDE + SIDE / 2
        self.sudoku_board.create_text(x, y,text="          Sudoku Solved!\nPress clear to restart sudoku", tags="won",fill="white", font=("Arial", 20))
    
    # to check if the board was solved
    def is_complete(self):
        if self.doku.input_board == self.doku.answer:
            self.draw_won()
        else:
            lb = Label(win,text="Wrong Answer!",fg = "red",bg="black",font= ('Arial Bold',30,))
            lb.place(x=247,y=650)
            self.after(2000,lb.destroy) 

    def solve_it(self):
        solver(self.doku.input_board)
        for i in range(9):
            for j in range(9):
                value = self.doku.input_board[i][j]
                if value != 0 and (i,j) in self.zero_pos: 
                    x = border_thickness + j * SIDE + SIDE/2
                    y = border_thickness + i * SIDE + SIDE/2
                    self.sudoku_board.create_text(x,y,text = value,tags="temp",fill="Cyan",font=('Arial','30','bold'))


    # to create the initial question board
    def create_num_board(self):
        clear_bt = Button(win, text="Clear", width=8, height=2,command=self.clear_board)
        clear_bt.place(x=75,y=600)

        solve_bt = Button(win, text="Check", width=8, height=2,command=self.is_complete)
        solve_bt.place(x=525,y=600)

        solution_bt = Button(win, text ="Solve", width=8, height=2,command=self.solve_it)
        solution_bt.place(x=300,y=600)

        self.sudoku_board.bind("<Button-1>",self._click)
        self.sudoku_board.bind("<Key>",self._keypress)
        self.zero_pos = []
        for i in range(9):
            for j in range(9):
                if self.doku.question[i][j] == 0:
                    self.zero_pos.append((i,j)) 
        self.sudoku_board.delete("num")
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
        for (i,j) in self.zero_pos:
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
    game = dokuSolver()
    game.game_start()
    dokuUI(win,game)
    win.mainloop()


