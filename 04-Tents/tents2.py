import sys
import numpy as np
import copy

EMPTY = 0
TREE = -1
TENT = 1
CROSS = 2
POSSIBLE = 3


class Tree:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.tent_row = -1
        self.tent_col = -1

    def placeTent(self, row, col):
        self.tent_row = row
        self.tent_col = col

class Puzzle:
    def __init__(self, tree_list, row_counts, col_counts):
        self.tree_list = tree_list
        self.tree_array = np.array(tree_list)
        self.row_counts = row_counts
        self.col_counts = col_counts
        self.row_length = len(row_counts)
        self.col_length = len(col_counts)
        self.solved = False


    def crossOutRow(self, row_num):
        for col in range(self.col_length):
            if self.tree_array[row_num, col] == EMPTY:
                self.tree_array[row_num, col] = CROSS

    def crossOutCol(self, col_num):
        for row in range(self.row_length):
            if self.tree_array[row, col_num] == EMPTY:
                self.tree_array[row, col_num] = CROSS

    # First stage, this removes potential locations for tents to go
    # by finding the 0's
    def crossOutZeroRows(self):
        for row, num in enumerate(self.row_counts):
            if num == 0:
                self.crossOutRow(row)
        for col, num in enumerate(col_counts):
            if num == 0:
                self.crossOutCol(col)

    def crossOutFarAway(self):
        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.tree_array[row, col] == EMPTY:
                    found_tree = False
                    if col > 0:
                        if self.tree_array[row, col - 1] == TREE:
                            # left
                            found_tree = True
                    if row > 0:
                        if self.tree_array[row - 1, col] == TREE:
                            # top
                            found_tree = True
                    if col < self.col_length - 1 :
                        if self.tree_array[row, col + 1] == TREE:
                            # right
                            found_tree = True
                    if row < self.row_length - 1:
                        if self.tree_array[row + 1, col] == TREE:
                            # bottom
                            found_tree = True
                    if not found_tree:
                            self.tree_array[row, col] = CROSS

    # Count Empty counts the amount of zeroes in each row column.
    def countEmpty(self):
        row_zeroes = np.count_nonzero(self.tree_array==EMPTY, axis=1)
        col_zeroes = np.count_nonzero(self.tree_array==EMPTY, axis=0)
        return row_zeroes, col_zeroes

    # Count Tents counts the amount of tents in each row column.
    def countTents(self):
        row_tents = np.count_nonzero(self.tree_array==TENT, axis=1)
        col_tents = np.count_nonzero(self.tree_array==TENT, axis=0)
        return row_tents, col_tents

    def countTrees(self):
        row_tents = np.count_nonzero(self.tree_array==TREE, axis=1)
        col_tents = np.count_nonzero(self.tree_array==TREE, axis=0)
        return row_tents, col_tents

    # Returns a boolean whether we placed a tent or not
    def placeTents(self):
        row_zeroes, col_zeroes = self.countEmpty()
        row_tents, col_tents = self.countTents()
        for row, num in enumerate(self.row_counts):
            if row_tents[row] != num:
                if row_zeroes[row] + row_tents[row] == num:
                    for col in range(self.col_length):
                        if self.tree_array[row, col] == EMPTY:
                            self.tree_array[row, col] = TENT
        row_zeroes, col_zeroes = self.countEmpty()
        row_tents, col_tents = self.countTents()
        for col, num in enumerate(self.col_counts):
            if col_tents[col] != num:
                if col_zeroes[col] + col_tents[col] == num:
                    for row in range(self.row_length):
                        if self.tree_array[row, col] == EMPTY:
                            self.tree_array[row, col] = TENT

    # Crosses out empty spaces if the row or column has the correct number of tents.
    def crossOutFull(self):
        row_tents, col_tents = self.countTents()
        for row, num in enumerate(self.row_counts):
            if row_tents[row] == num:
                for col in range(len(self.col_counts)):
                    if self.tree_array[row, col] == EMPTY:
                        self.tree_array[row, col] = CROSS
        for col, num in enumerate(self.col_counts):
            if col_tents[col] == num:
                for row in range(len(self.row_counts)):
                    if self.tree_array[row, col] == EMPTY:
                        self.tree_array[row, col] = CROSS

    # Cross out spaces that are adjacent or diagonal
    def crossOutTentConnection(self):
        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.tree_array[row, col] == TENT:
                    if col > 0:
                        if self.tree_array[row, col - 1] == EMPTY:
                            # left
                            self.tree_array[row, col - 1] = CROSS
                    if col > 0 and row > 0:
                        if self.tree_array[row - 1, col - 1] == EMPTY:
                            # top left
                            self.tree_array[row - 1, col - 1] = CROSS
                    if row > 0:
                        if self.tree_array[row - 1, col] == EMPTY:
                            # top
                            self.tree_array[row - 1, col] = CROSS
                    if col < (self.col_length - 1) and row > 0:
                        if self.tree_array[row - 1, col + 1] == EMPTY:
                            # top right
                            self.tree_array[row - 1, col + 1] = CROSS
                    if col < self.col_length - 1:
                        if self.tree_array[row, col + 1] == EMPTY:
                            # right
                            self.tree_array[row, col + 1] = CROSS
                    if row < (self.row_length - 1) and col < (self.col_length - 1):
                        if self.tree_array[row + 1, col + 1] == EMPTY:
                            # bottom right
                            self.tree_array[row + 1, col + 1] = CROSS
                    if row < self.row_length - 1:
                        if self.tree_array[row + 1, col] == EMPTY:
                            # bottom
                            self.tree_array[row + 1, col] = CROSS
                    if row < (self.row_length - 1) and col > 0:
                        if self.tree_array[row + 1, col - 1] == EMPTY:
                            # bottom left
                            self.tree_array[row + 1, col - 1] = CROSS

    # Checks if the current puzzle has been solved.
    def isSolved(self):
        row_tents, col_tents = self.countTents()
        solved = True
        for row, num in enumerate(self.row_counts):
            if row_tents[row] != num:
                solved = False
                break
        for col, num in enumerate(self.col_counts):
            if col_tents[col] != num:
                solved = False
                break
        self.solved = solved

    def leftEmpty(self, row, col):
        try:
            if self.tree_array[row, col-1] != TENT:
                return False
            else:
                return True
        except IndexError:
            return False

    def rightEmpty(self, row, col):
        try:
            if self.tree_array[row, col+1] != TENT:
                return False
            else:
                return True
        except IndexError:
            return False

    def topEmpty(self, row, col):
        try:
            if self.tree_array[row-1, col] != TENT:
                return False
            else:
                return True
        except IndexError:
            return False

    def bottomEmpty(self, row, col):
        try:
            if self.tree_array[row+1, col] != TENT:
                return False
            else:
                return True
        except IndexError:
            return False

    def cornerCases(self):
        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.tree_array[row, col] == TREE:
                    if not self.leftEmpty(row, col):
                        if not self.topEmpty(row, col):
                            if col < self.col_length -1 and row < self.row_length-1:
                                if self.tree_array[row+1, col+1] == EMPTY:
                                    self.tree_array[row+1, col+1] = CROSS
                        if not self.bottomEmpty(row, col):
                            if col < self.col_length -1 and row > 0:
                                if self.tree_array[row-1, col+1] == EMPTY:
                                    self.tree_array[row-1, col+1] = CROSS
                    if not self.rightEmpty(row, col):
                        if not self.topEmpty(row, col):
                            if col > 0 and row < self.row_length-1:
                                if self.tree_array[row+1, col-1] == EMPTY:
                                    self.tree_array[row+1, col-1] = CROSS
                        if not self.bottomEmpty(row, col):
                            if col > 0 and row > 0:
                                if self.tree_array[row-1, col-1] == EMPTY:
                                    self.tree_array[row-1, col-1] = CROSS

    def printAnswer(self):
        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.tree_array[row, col] == TENT:
                    print("C", end="")
                if self.tree_array[row, col] == TREE:
                    print("T", end="")
                if self.tree_array[row, col] == CROSS:
                    print(".", end="")
                if self.tree_array[row, col] == EMPTY:
                    print("_", end="")

            print()

    def availableSpaces(self):
        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.tree_array[row, col] == EMPTY:
                    return True

    def availableRow(self, row):
        for col in range(self.col_counts):
            if self.tree_array[row, col] == EMPTY:
                return True

    def tryCombinations(self):
        row_zeros, col_zeros = self.countEmpty()
        row_trees, col_trees = self.countTrees()
        row_tents, col_tents = self.countTents()
        for row, num in enumerate(self.row_counts):
            # Then need to place tents in this row
            if self.row_counts[row] != row_tents[row]:
                for col in range(self.col_counts):
                    pass

    def initialRules(self):
        self.crossOutFull()
        self.crossOutFarAway()
        # self.cornerCases()
        self.placeTents()
        self.crossOutTentConnection()
        # self.printAnswer()

    def loopRules(self):
        self.crossOutFull()
        # self.cornerCases()
        self.crossOutTentConnection()
        # self.printAnswer()
        self.placeTents()
        # self.printAnswer()




def solve(puzzle):
    puzzle_copy = copy.deepcopy(puzzle)
    puzzle.initialRules()
    puzzle.isSolved()
    while not(puzzle_copy.tree_array == puzzle.tree_array).all() and not puzzle.solved:
        puzzle_copy = copy.deepcopy(puzzle)
        puzzle.loopRules()
        puzzle.isSolved()
    if not puzzle.solved:
        print("CAN'T SOLVE")
        puzzle.printAnswer()
        pass
    if puzzle.solved:
        puzzle.printAnswer()

problem = []
problems_all = []
tree_list = []

if __name__ == "__main__":
    second_row = False
    for line in sys.stdin:
        if not line.isspace():
            line = line.split()

            if len(line) == 1: # Then trees and dot line
                row = []
                for character in line[0]:
                    if character == '.':
                        row.append(EMPTY)
                    elif character == 'T':
                        row.append(TREE)
                tree_list.append(row)
            else:
                if not second_row:
                    problem.append(tree_list.copy())
                    problem.append(list(int(j) for j in line))
                    tree_list.clear()
                    second_row = True
                elif second_row:
                    problem.append(list(int(j) for j in line))
                    if len(problem) != 3:
                        print("Bad format")
                        problem.clear()
                        second_row = False
                    else:
                        problems_all.append(problem.copy())
                        problem.clear()
                        second_row = False

    for item in problems_all:
        item[1].reverse()
        puzzle = Puzzle(item[0], item[1], item[2])
        solve(puzzle)
        print()
