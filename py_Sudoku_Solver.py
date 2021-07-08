board = [
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


def print_board(sudo):
    for i in range(len(sudo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - - - -")
        for j in range(len(sudo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ",end= " ")

            if j == 8:
                print(sudo[i][j])
            else:
                print(str(sudo[i][j]) + " ", end =" ")
                

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
        

print("QUESTION :", end ="\n\n") 
print_board(board)
solver(board)   
print("\n ANSWER :", end ="\n\n")
print_board(board)
