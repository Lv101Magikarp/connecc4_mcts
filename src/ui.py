from board import Board
from mcts import MCTS

def inputChoice(choices):
    choice = input()
    while choice not in choices:
        print('huh??? Please type a valid choice from these:', choices)
        choice = input()
    return choice

def run2PGame():
    print('Ze game haz begun: P1 = x, P2 = o')
    board = Board()
    terminal_state = False
    result = 0
    while not terminal_state:
        if board.turn == 1:
            print('P1, make a move marked by the numbers below:')
        else:
            print('P2, make a move marked by the numbers below:')
        board.printPositionWithLegalMoves()
        # make the player input a legal move
        legal_moves = board.legalMoves()
        choice = inputChoice([str(i) for i in range(1, len(legal_moves) + 1)])
        board.makeMove(legal_moves[int(choice) - 1])
        # check for game end
        terminal_state, result = board.checkForTerminalState()
    board.printPosition()
    if result == 1:
        print('P1 WON!!! NAISU!!!')
    elif result == -1:
        print('P2 WON!!! HOORAY!!!')
    else:
        print('The game was drawn! How did yall manage that?')

def run1PGame():
    # make the player decide who plays first
    print('Do you wish play first? 1 - yeah ofc, 2 - nah I\'m good')
    choice = inputChoice(('1', '2'))
    if choice == '1':
        player_turn = 1
    else:
        player_turn = -1
    mcts = MCTS()
    print('Ze game haz begun: P1 = x, P2 = o')
    board = Board()
    terminal_state = False
    result = 0
    while not terminal_state:
        board.printPosition()
        if board.turn == player_turn:
            print('It\'s your turn, make a move marked by the numbers below:')
            board.printPositionWithLegalMoves()
            # make the player input a legal move
            legal_moves = board.legalMoves()
            choice = inputChoice([str(i) for i in range(1, len(legal_moves) + 1)])
            board.makeMove(legal_moves[int(choice) - 1])
            # check for game end
            terminal_state, result = board.checkForTerminalState()
        else:
            print('Now it\'s mah turn *beep boop*')
            board.makeMove(mcts.searchBestMove(board))
            # check for game end
            terminal_state, result = board.checkForTerminalState()
    board.printPosition()
    if result == player_turn:
        print('Ya defeated me *beep boop*')
    elif result == -player_turn:
        print('Indeed the expected outcome *beep boop*')
    else:
        print('The game was drawn! How did yall manage that?')

def runAIGame():
    pass

if __name__ == '__main__':
    print('Howdy! How do ya wanna play connecc 4?')
    print('1 - 2P')
    print('2 - 1P vs CPU')
    print('3 - Computer cock fight D:')
    choice = inputChoice(('1', '2', '3'))
    if choice == '1':
        run2PGame()
    elif choice == '2':
        run1PGame()
    elif choice == '3':
        runAIGame()