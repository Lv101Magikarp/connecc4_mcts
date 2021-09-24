from board import Board
import math
import time
import random

class MCTSTreeNode:
    def __init__(self, board, move=None, parent=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.child = []
        self.terminal_state, trash = self.board.checkForTerminalState()
        self.score = 0
        self.visits = 0
    
    def printTree(self):
        print(self, 'parent:', self.parent, 'move:', self.move, 'score:', self.score, 'visits:', self.visits)
        for c in self.child:
            c.printTree()

class MCTS:
    def searchBestMove(self, initial_board, mode='i', iterations=1500, timeout_ms=500, exploration_param=math.sqrt(2)):
        self.root = MCTSTreeNode(initial_board)
        if mode == 'i':
            for i in range(iterations):
                self.MCTSIteration(exploration_param)
        elif mode == 't':
            start_time = time.time()
            current_time = time.time()
            while current_time - start_time < timeout_ms/1000:
                self.MCTSIteration(exploration_param)
                current_time = time.time()
        else:
            raise Exception('The MCTS mode must be either \'i\' or \'t\'')
        return self.UCB1BestNode(self.root, exploration_param).move

    def MCTSIteration(self, exploration_param):
        node = self.select(self.root, exploration_param)
        if node.visits == 0:
            score = self.rollout(node.board)
        else:
            self.expand(node)
            node = self.select(node, exploration_param)
            score = self.rollout(node.board)
        self.backpropagate(node, score)

    def select(self, node, exploration_param):
        while node.child:
            node = self.UCB1BestNode(node, exploration_param)
        return node
    
    def expand(self, node):
        if not node.terminal_state:
            legal_moves = node.board.legalMoves()
            for move in legal_moves:
                new_board = Board(node.board)
                new_board.makeMove(move)
                new_node = MCTSTreeNode(new_board, move, node)
                node.child.append(new_node)

    def rollout(self, board):
        rollout_board = Board(board)
        terminal_state, result = rollout_board.checkForTerminalState()
        while terminal_state == False:
            legal_moves = rollout_board.legalMoves()
            rollout_board.makeMove(random.choice(legal_moves))
            terminal_state, result = rollout_board.checkForTerminalState()
        return result
    
    def backpropagate(self, node, score):
        while node is not None:
            node.score += score
            node.visits += 1
            node = node.parent

    def UCB1BestNode(self, node, exploration_param):
        best_score = float('-inf')
        best_nodes = []
        for c in node.child:
            if c.visits == 0:
                score = float('inf')
            else:
                score = node.board.turn*(c.score/c.visits) + exploration_param*math.sqrt(math.log(node.visits)/c.visits)
            if score > best_score:
                best_score = score
                best_nodes = [c]
            elif score == best_score:
                best_nodes.append(c)
        return random.choice(best_nodes)