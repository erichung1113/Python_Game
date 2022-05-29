board=[
    [3,9,-1, -1,5,-1, -1,-1,-1],
    [-1,-1,-1, 2,-1,-1, -1,-1,5],
    [-1,-1,-1, 7,1,9, -1,8,-1],
    
    [-1,5,-1, -1,6,8, -1,-1,-1],
    [2,-1,6, -1,-1,3, -1,-1,-1],
    [-1,-1,-1, -1,-1,-1, -1,-1,4],

    [5,-1,-1, -1,-1,-1, -1,-1,-1],
    [6,7,-1, 1,-1,5, -1,4,-1],
    [1,-1,9, -1,-1,-1, 2,-1,-1]
]


def is_valid(val,r,c):
    row_vals=board[r]
    col_vals=[board[i][c] for i in range(9)]

    if val in row_vals or val in col_vals:
        return False
    
    start_row=(r//3)*3
    start_col=(c//3)*3
    for i in range(start_row,start_row+3):
        for j in range(start_col,start_col+3):
            if board[i][j]==val:
                return False
    
    return True

def all_filled():
    for i in range(9):
        for j in range(9):
            if board[i][j]==-1:
                return False
    return True

def find_empty():
    for i in range(9):
        for j in range(9):
            if board[i][j]==-1:
                return i,j
    
    return None,None

def solve():
    result=find_empty()

    i=result[0]
    j=result[1]

    if i==None:
        return True
        
    for k in range(1,10):
        if is_valid(k,i,j):
            board[i][j]=k

            if solve():
                return True
            
            board[i][j]=-1
    
    return False


if(solve()):
    print(board)
