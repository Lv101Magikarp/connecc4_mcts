#!/usr/bin/python3

from board import Board
from mcts import MCTS
import argparse

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

def run1PGame(arg):
    # make the player decide who plays first
    print('Do you wish play first? 1 - yeah ofc, 2 - nah I\'m good')
    choice = inputChoice(('1', '2'))
    if choice == '1':
        player_turn = 1
    else:
        player_turn = -1
    mcts = MCTS()
    print('Ze game haz begun')
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
            board.makeMove(mcts.searchBestMove(board, mode=arg['cpu1mode'], iterations=int(arg['cpu1iterations']), timeout_ms=int(arg['cpu1time'])))
            # check for game end
            terminal_state, result = board.checkForTerminalState()
    board.printPosition()
    if result == player_turn:
        print('Ya defeated me *beep boop*')
    elif result == -player_turn:
        print('Indeed the expected outcome *beep boop*')
    else:
        print('The game was drawn! How did yall manage that?')

def runAIGame(arg):
    mcts = MCTS()
    print('Ze game haz begun')
    board = Board()
    terminal_state = False
    result = 0
    while not terminal_state:
        board.printPosition()
        if board.turn == 1:
            print('CPU1 will win *beep boop*')
            board.makeMove(mcts.searchBestMove(board, mode=arg['cpu1mode'], iterations=int(arg['cpu1iterations']), timeout_ms=int(arg['cpu1time'])))
        else:
            print('CPU2 can\'t lose *beep boop*')
            board.makeMove(mcts.searchBestMove(board, mode=arg['cpu2mode'], iterations=int(arg['cpu2iterations']), timeout_ms=int(arg['cpu2time'])))
        # check for game end
        terminal_state, result = board.checkForTerminalState()
    board.printPosition()
    if result == 1:
        print('I told ya, CPU1 is the best *beep boop*')
    elif result == -1:
        print('CPU2 has more transistors than ya fools *beep boop*')
    else:
        print('The game was drawn! How did yall manage that?')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu1mode', default='i', choices=['i', 't'], help='mode for the CPU1 or 1P CPU: [i]terations or [t]ime per move')
    parser.add_argument('--cpu2mode', default='i', choices=['i', 't'], help='mode for the CPU2: [i]terations or [t]ime per move')
    parser.add_argument('--cpu1iterations', default='1500', help='CPU1 iterations per move')
    parser.add_argument('--cpu2iterations', default='1500', help='CPU2 iterations per move')
    parser.add_argument('--cpu1time', default='500', help='CPU1 time per move in ms')
    parser.add_argument('--cpu2time', default='500', help='CPU2 time per move in ms')
    arg = vars(parser.parse_args())

    print('Howdy! How do ya wanna play connecc 4?')
    print('1 - 2P')
    print('2 - 1P vs CPU')
    print('3 - Computer cock fight D:')
    choice = inputChoice(('1', '2', '3'))
    if choice == '1':
        run2PGame()
    elif choice == '2':
        run1PGame(arg)
    elif choice == '3':
        runAIGame(arg)