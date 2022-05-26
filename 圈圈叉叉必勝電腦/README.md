#  A Never Lose Computer Player.

### 100 Test Result:  
RandomPlayer wins　:　0 times  
GeniusPlayer wins　:　74 times  
Tie　:　26 times  

### How to do ? : Minimax Algorithm  

Idea : Iterate all posibile moves, and calculate its win rate, chooce the biggest one to go.  

#### define utility = X's win rate

Implement : Recusive all next moves, in each case, it has two situation:  
If this is X(Computer)'s turn :  
choose the biggest utility of next move  
If this is O(Player)'s turn :  
choose the smallest utility of next move 

(from the computer's point of view)  
Because we want to win the game, so we will choose the step with the greatest chance of winning in my turn, But opponent is not fool, he will choose the lease chance of my winning in his turn. Follow this rules and we can get the best solution.  

### Optimization : Alpha-Beta Pruning  
Idea : If current utility is biggest/smallest than father's utility, we can return immediately, because there is no more answer greater than curerent answer.  

In X's round, we will go to the biggest utility step, so we want to maximize the utility  
In O's round, we will go to the smallest utility step, so we want to minimize the utility  

In X's round, if the current utility is bigger than father's utility, we can return now.  
Because the utility will be greater or equal than now, it will not change the father's choice, father wants to minimize the utility.  
In O's round, if the current utility is smaller than father's utility, we can return now.  
Because the utility will be less or equal than now, it will not change the father's choice, father wants to maximize the utility.  

### Play It
https://replit.com/@erichung1113/Tic-Tac-Toe#main.py
