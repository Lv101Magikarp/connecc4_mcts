from board import Board

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
        legal_moves = board.legalMoves()
        choice = inputChoice([str(i) for i in range(1, len(legal_moves) + 1)])
        board.makeMove(legal_moves[int(choice) - 1])
        terminal_state, result = board.checkForTerminalState()
    board.printPosition()
    if result == 1:
        print('P1 WON!!! HOORAY!!!')
    elif result == -1:
        print('P2 WON!!! HOORAY!!!')
    else:
        print('The game was drawn! How did yall manage that?')

def run1PGame():
    return

def runAIGame():
    return

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