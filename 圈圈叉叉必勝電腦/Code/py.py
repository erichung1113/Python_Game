import copy,random
inf=1e9

board=[[' ']*3 for i in range(3)]
used=[False]*10

def init():
    for i in range(3):
        for j in range(3):
            num=i*3+j+1
            used[num]=False
            board[i][j]=str(num)
        print('|'.join(board[i]))

def show(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j] if board[i][j].isalpha() else " ",end='')
            print("|" if j<2 else "\n",end='')
    print('')

def Write(Pos,Who):
    used[int(Pos)]=True

    for i in range(3):
        for j in range(3):
            if board[i][j]==Pos:
                board[i][j]=Who
                return

def isfilled(status):
    for i in range(3):
        for j in range(3):
            if status[i][j].isdigit():
                return False
    return True

def isend(board):
    for i in range(3):
        if(board[i][0]==board[i][1]==board[i][2]):
            return True,board[i][0]
        if(board[0][i]==board[1][i]==board[2][i]):
            return True,board[0][i]
    if(board[0][0]==board[1][1]==board[2][2]):
        return True,board[0][0]
    if(board[2][0]==board[1][1]==board[0][2]):
        return True,board[2][0]
    
    return False,-1

def dfs(status,depth,player,faOpt):
    endcheck=isend(status)
    if endcheck[0]:
        return (1 if endcheck[1]=='X' else -1)*depth,0
    
    if isfilled(status):
        return 0,0

    Opt=-inf if player=='X' else inf
    next_player='O' if player=='X' else 'X'
    Pos=0

    for i in range(3):
        for j in range(3):
            if status[i][j].isdigit():
                nextstatus=copy.deepcopy(status)
                nextstatus[i][j]=player
                returnValue=dfs(nextstatus,depth-1,next_player,Opt)

                if (player=='X' and returnValue[0]>Opt) or (player=='O' and returnValue[0]<Opt):
                    Opt=returnValue[0]
                    Pos=i*3+j+1

                if player=='O' and Opt<=faOpt: return -inf,0
                if player=='X' and Opt>=faOpt: return inf,0 

    return Opt,Pos
    
                
def GeniusMove():
    Write(str(dfs(board,10,'X',inf)[1]),'X')

def RandMove():
    Pos=random.randint(1,9)
    while used[Pos]:
        Pos=random.randint(1,9)
    Write(str(Pos),'O')

def playerMove():
    Pos=input('Plase take a Move: ')
    while(used[int(Pos)]):
        Pos=input('That position has used,plase take a Move again: ')
    Write(Pos,'O')
init()

winner='Non'
for i in range(9):
    if i&1:
        print("Computer Move...")
        GeniusMove()
        show(board)
    else:
        playerMove()
        show(board)
    
    endresult=isend(board)
    if endresult[0]:
        winner=endresult[1]
        print(f"{winner} is win!!\n")
        break

if winner=='Non': print("Tie!!\n")
