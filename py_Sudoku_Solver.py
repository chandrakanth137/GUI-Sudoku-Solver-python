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
                

def empty_box(sudo):
    for i in range(len(sudo)):
        for j in range(len(sudo[0])):
            if sudo[i][j] == 0:
                return (i,j)


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
        

print("QUESTION :", end ="\n\n") 
print_board(board)
solver(board)   
print("\n ANSWER :", end ="\n\n")
print_board(board)
