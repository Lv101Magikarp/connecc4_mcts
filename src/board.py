# Board Class source

from copy import deepcopy

class Board:
    def __init__(self, board=None):
        self.turn = None
        self.position = []

        # initialize from parameter
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
        # initialize start position
        else:
            self.turn = 1
            for row in range(6):
                self.position.append([])
                for col in range(7):
                    self.position[row].append(0)

    def printPosition(self):
        print('\n')
        for row in range(6):
            for col in range(7):
                if self.position[row][col] == 0:
                    print('-', end='  ')
                elif self.position[row][col] == -1:
                    print('o', end='  ')
                else:
                    print('x', end='  ')
            print('\n')

    def printPositionWithLegalMoves(self):
        legal_moves = self.legalMoves()
        print('\n')
        for row in range(6):
            for col in range(7):
                printed_legal_move = False
                for i,move in enumerate(legal_moves):
                    if move == (row, col):
                        print(str(i+1), end='  ')
                        printed_legal_move = True
                if printed_legal_move:
                    continue
                elif self.position[row][col] == 0:
                    print('-', end='  ')
                elif self.position[row][col] == -1:
                    print('o', end='  ')
                else:
                    print('x', end='  ')
            print('\n')

    def makeMove(self, move):
        self.position[move[0]][move[1]] = self.turn
        if self.turn == 1:
            self.turn = -1
        else:
            self.turn = 1

    def legalMoves(self):
        moves = []
        # iterate columns bottom up, if an empty space is found it's a possible move
        # and the only possible move for this column
        for col in range(7):
            for row in range(5,-1,-1):
                if self.position[row][col] == 0:
                    moves.append((row, col))
                    break
        return moves

    def checkForTerminalState(self):
        # check for column winners
        for col in range(7):
            connected_pieces = 0
            connected_color = 0
            for row in range(5,-1,-1):
                # count sequentially connected pieces
                if self.position[row][col] == 0:
                    break
                elif self.position[row][col] == connected_color:
                    connected_pieces += 1
                else:
                    connected_pieces = 1
                    connected_color = self.position[row][col]
                # check for 4 connected pieces
                if connected_pieces == 4:
                    return True, connected_color
        # check for row winners
        for row in range(6):
            connected_pieces = 0
            connected_color = 0
            for col in range(7):
                # count sequentially connected pieces
                if self.position[row][col] == 0:
                    connected_pieces = 0
                    connected_color = 0
                if self.position[row][col] == connected_color:
                    connected_pieces += 1
                else:
                    connected_pieces = 1
                    connected_color = self.position[row][col]
                # check for 4 connected pieces
                if connected_pieces == 4:
                    return True, connected_color
        # check for diagonal winners
        # there are 12 diagonals with 4 or more spaces : 6 at pi/4 and 6 at 3pi/4
        for diag in range(12):
            # choose the starting tile
            if diag == 0:
                row = 3
                col = 0
            elif diag == 1:
                row = 4
                col = 0
            elif diag == 2:
                row = 5
                col = 0
            elif diag == 3:
                row = 5
                col = 1
            elif diag == 4:
                row = 5
                col = 2
            elif diag == 5:
                row = 5
                col = 3
            elif diag == 6:
                row = 3
                col = 6
            elif diag == 7:
                row = 4
                col = 6
            elif diag == 8:
                row = 5
                col = 6
            elif diag == 9:
                row = 5
                col = 5
            elif diag == 10:
                row = 5
                col = 4
            elif diag == 11:
                row = 5
                col = 3
            # choose the direction
            if diag < 6:
                inc_row = -1
                inc_col = 1
            else:
                inc_row = -1
                inc_col = -1
            connected_pieces = 0
            connected_color = 0
            # iterate while still in the board
            while row >= 0 and row <= 5 and col >= 0 and col <= 6:
                # count sequentially connected pieces
                if self.position[row][col] == 0:
                    connected_pieces = 0
                    connected_color = 0
                elif self.position[row][col] == connected_color:
                    connected_pieces += 1
                else:
                    connected_pieces = 1
                    connected_color = self.position[row][col]
                # check for 4 connected pieces
                if connected_pieces == 4:
                    return True, connected_color
                row += inc_row
                col += inc_col
        # finally check for a filled board draw or else the game still in progress
        for col in range(7):
            if self.position[0][col] == 0:
                return False, 0
        return True, 0
