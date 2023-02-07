from termcolor2 import c
import random
import time


# Input: board (3x3 Matrix)
# Output: Pretty print of the spaces
# Description: Prints the board nicely.
def show(board):
    spaces = []
    for i in range(3):
        for j in range(3):
            if type(board[i][j]) == str or board[i][j] == 0:
                spaces.append(board[i][j])
            else:
                if board[i][j] > 0:
                    spaces.append(c(board[i][j]).green)
                else:
                    spaces.append(c(board[i][j]).red)

    for i in range(3):
        print(" ", str(spaces[(i * 3) + 0]), " ", str(spaces[(i * 3) + 1]), " ", str(spaces[(i * 3) + 2]))
    print()


# Input: Game.board (3x3 matrix)
# Output: Winner of the game ('X', 'O', or '-')
# Description: Returns the winner of the game. Checks each non-blank row, column, and diagonals for matches.
def win(board):
    # Checks horizontal spaces
    if board[0][0] != '-' and board[0][0] == board[0][1] and board[0][0] == board[0][2]:
        return board[0][0]
    if board[1][0] != '-' and board[1][0] == board[1][1] and board[1][0] == board[1][2]:
        return board[1][0]
    if board[2][0] != '-' and board[2][0] == board[2][1] and board[2][0] == board[2][2]:
        return board[2][0]

    # Checks vertical spaces
    if board[0][0] != '-' and board[0][0] == board[1][0] and board[0][0] == board[2][0]:
        return board[0][0]
    if board[0][1] != '-' and board[0][1] == board[1][1] and board[0][1] == board[2][1]:
        return board[0][1]
    if board[0][2] != '-' and board[0][2] == board[1][2] and board[0][2] == board[2][2]:
        return board[0][2]

    # Checks diagonal spaces
    if board[0][0] != '-' and board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    if board[0][2] != '-' and board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        return board[0][2]

    # Checks if the board is full and no winner, in which case it is a draw
    draw = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                draw = False
    if draw:
        return "draw"
    else:
        return '-'


# Input: A player ('X' or 'O')
# Output: The other player ('X' or 'O')
# Description: Simple method that returns the other player for the sake of simplicity and readability.
def next(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'


# Input: fitness board (3x3 matrix)
# Output: list of coordinates
# Description: Returns the list of coordinates with the highest fitness values
def best(board):
    best = []
    maximum = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] != '-':
                if len(best) == 0:
                    maximum = board[i][j]
                    best.append([i, j])
                else:
                    if board[i][j] > maximum:
                        best.clear()
                        maximum = board[i][j]
                        best.append([i, j])
                    elif board[i][j] == maximum:
                        best.append([i, j])

    return best


# Input: fitness board (3x3 matrix)
# Output: list of coordinates
# Description: Returns the list of coordinates with the lowest fitness values
def worst(board):
    worst = []
    minimum = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] != '-':
                if len(worst) == 0:
                    minimum = board[i][j]
                    worst.append([i, j])
                else:
                    if board[i][j] < minimum:
                        minimum = board[i][j]
                        worst.append([i, j])
                    elif board[i][j] == minimum:
                        worst.append([i, j])

    return worst


# Input: board (3x3 matrix)
# Output: player ('X' or 'O')
# Description: Reads the board and determines who's turn it should be.
def turn(board):
    x = 0
    o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                x += 1
            elif board[i][j] == 'O':
                o += 1

    if x == 0:
        player = 'X'
    elif x > o:
        player = 'O'
    else:
        player = 'X'

    return player


# Input: board (3x3 matrix)
# Output: board (3x3 matrix)
# Description: Returns a matrix filled with fitness values in each position for possible moves
def fit(board):


    fitboard = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    player = turn(board)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':

                # Make a simulated move to check position [i][j]
                board[i][j] = player

                # This if just inverts the score if it is not player 'X' turn
                if player == 'X':
                    fitboard[i][j] = simulate(board, next(player))
                elif player == 'O':
                    fitboard[i][j] = 0 - simulate(board, next(player))

                # Undo simulated move
                board[i][j] = '-'

    return fitboard


# Input: A game state (s), a position to check the fitness of (p), and the current player (t)
# Output: The fitness score of the given position
# Description: Simulates all possible outcomes after a move and returns the "fitness" of that move.
#               Fitness score is calculated by the number of possible ways to win or lose after the move.
#               Higher fitness scores favor player 'X'. Lower fitness scores favor player 'O'.
def simulate(game, player):
    winner = win(game)

    if winner == 'X':
        return 1
    if winner == 'O':
        return -1
    if winner == 'draw':
        return 0

    possibleScores = []
    for i in range(3):
        for j in range(3):
            if game[i][j] == '-':
                # Make a simulated move at position[i][j] and get the score
                game[i][j] = player
                score = simulate(game, next(player))

                # Undo simulated move
                game[i][j] = "-"

                # Alpha-Beta Pruning: immediately returns score the first time
                # that the player finds a move that can win
                if player == 'X' and score == 1:
                    return 1
                elif player == 'O' and score == -1:
                    return -1

                # Adds scores from all possible subsequent moves to a list
                possibleScores.append(score)

    if player == 'X':
        return max(possibleScores)
    elif player == 'O':
        return min(possibleScores)


player = ''
opponent = ''
print("Would you like to be X or O?")
while player != 'X' and player != 'O':
    player = input().upper()
    opponent = next(player)

myGame = [['-', '-', '-'],
          ['-', '-', '-'],
          ['-', '-', '-']]

show(myGame)

currentPlayer = 'X'


while win(myGame) == '-':

    if turn(myGame) == player:
        print("Enter coordinates to make a move (e.g. \"OO\" or \"21\")")
        coord = input()
        print()

        if coord.isnumeric() and 10 > int(coord) > 0:

            # COORD INPUT
            # row = int(coord[0])
            # col = int(coord[1])

            # NUMPAD INPUT
            coord = int(coord)
            row = (2 - int((coord - 1) / 3))
            col = (coord - 1) % 3

            if myGame[row][col] == '-':
                myGame[row][col] = player

            else: print("That spot is taken!")
        else: print("Invalid Input!")

    else:
        initialtime = time.time()
        aiMoves = best(fit(myGame))
        show(fit(myGame))
        move = random.choice(aiMoves)
        myGame[move[0]][move[1]] = opponent

        newTime = time.time() - initialtime
        print(str(int(newTime * 1000)) + "ms")

    show(myGame)

    if win(myGame) == player:
        print("You won!? HOW???")
    elif win(myGame) == opponent:
        print("You lost. It is to be expected...")
    elif win(myGame) == "draw":
        print("It is a tie. You cannot win.")
