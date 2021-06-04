import sys
import numpy as np
import copy

EMPTY = 0
TREE = -1
TENT = 1
CROSS = 2
POSSIBLE = 3

problem = []
problems_all = []
tree_list = []

class Tree:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.tent_row = None
        self.tent_col = None
        self.avail_squares = list()
        self.visited = False


    def placeTent(self, row, col):
        self.tent_row = row
        self.tent_col = col
        # cross out adjacent tiles

class Puzzle:
    def __init__(self, tree_list, row_counts, col_counts):
        self.tree_list = tree_list
        self.tree_array = np.array(tree_list)
        self.row_counts = row_counts
        self.col_counts = col_counts
        self.row_length = len(row_counts)
        self.col_length = len(col_counts)
        self.solved = False

        self.trees = list()

        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.tree_array[row, col] == TREE:
                    self.trees.append(Tree(row, col))

    def crossOutRow(self, row_num):
        for col in range(self.col_length):
            if self.tree_array[row_num, col] == EMPTY:
                self.tree_array[row_num, col] = CROSS

    def crossOutCol(self, col_num):
        for row in range(self.row_length):
            if self.tree_array[row, col_num] == EMPTY:
                self.tree_array[row, col_num] = CROSS

    def crossOutZeroRows(self):
        for row, num in enumerate(self.row_counts):
            if num == 0:
                self.crossOutRow(row)
        for col, num in enumerate(col_counts):
            if num == 0:
                self.crossOutCol(col)

    def topLeft(self, row, col):
        if row == 0 or col == 0:
            return None
        else:
            return self.tree_array[row-1, col-1]

    def topMiddle(self, row, col):
        if row == 0:
            return None
        else:
            return self.tree_array[row-1, col]

    def topRight(self, row, col):
        if row == 0 or col == self.col_length-1:
            return None
        else:
            return self.tree_array[row-1, col+1]

    def middleLeft(self, row, col):
        if col == 0:
            return None
        else:
            return self.tree_array[row, col-1]

    def middleRight(self, row, col):
        if col == self.col_length-1:
            return None
        else:
            return self.tree_array[row, col+1]

    def bottomLeft(self, row, col):
        if row == self.row_length-1 or col == 0:
            return None
        else:
            return self.tree_array[row+1, col-1]

    def bottomMiddle(self, row, col):
        if row == self.row_length-1:
            return None
        else:
            return self.tree_array[row+1, col]

    def bottomRight(self, row, col):
        if row == self.row_length-1 or col == self.col_length-1:
            return None
        else:
            return self.tree_array[row+1, col+1]

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

    def tentsNear(self, row, col):
        if self.topLeft(row, col) == TENT:
            return True
        elif self.topMiddle(row, col) == TENT:
            return True
        elif self.topRight(row, col) == TENT:
            return True
        elif self.middleLeft(row, col) == TENT:
            return True
        elif self.middleRight(row, col) == TENT:
            return True
        elif self.bottomLeft(row, col) == TENT:
            return True
        elif self.bottomMiddle(row, col) == TENT:
            return True
        elif self.bottomRight(row, col) == TENT:
            return True
        return False

    def squaresToPlaceTent(self, row, col):
        squares = []
        row_tents, col_tents = self.countTents()
        if row_tents[row] < self.row_counts[row]:
            if col > 0:
                if col_tents[col-1] < self.col_counts[col-1]:
                    if self.middleLeft(row, col) == EMPTY:
                        if not self.tentsNear(row, col-1):
                            squares.append((row, col-1))
            if col < self.col_length-1:
                if col_tents[col+1] < self.col_counts[col+1]:
                    if self.middleRight(row, col) == EMPTY:
                        if not self.tentsNear(row, col+1):
                            squares.append((row, col+1))
        if col_tents[col] < self.col_counts[col]:
            if row > 0:
                if row_tents[row-1] < self.row_counts[row-1]:
                    if self.topMiddle(row, col) == EMPTY:
                        if not self.tentsNear(row-1, col):
                            squares.append((row-1, col))
            if row < self.row_length-1:
                if row_tents[row+1] < self.row_counts[row+1]:
                    if self.bottomMiddle(row, col) == EMPTY:
                        if not self.tentsNear(row+1, col):
                            squares.append((row+1, col))
        return squares

    def solve(self):
        solved = False
        tree_index = 0
        while not solved:
            c_tree = self.trees[tree_index]
            if not c_tree.visited:
                c_tree.avail_squares = self.squaresToPlaceTent(c_tree.row, c_tree.col)
            if len(c_tree.avail_squares) == 0:
                # Go back to previous tree
                tree_index += -1
                c_tree = self.trees[tree_index]
                # Remove current tent
                self.tree_array[c_tree.tent_row, c_tree.tent_col] = EMPTY
                c_tree.tent_row = None
                c_tree.tent_col = None

                while len(c_tree.avail_squares) == 0:
                    # Keep moving back up
                    c_tree.avail_squares = list()
                    c_tree.visited = False
                    tree_index += -1
                    c_tree = self.trees[tree_index]
                    self.tree_array[c_tree.tent_row, c_tree.tent_col] = EMPTY
                    c_tree.tent_row = None
                    c_tree.tent_col = None

            s = c_tree.avail_squares.pop(0)
            self.tree_array[s[0], s[1]] = TENT
            c_tree.placeTent(s[0], s[1])
            if tree_index == len(self.trees) - 1:
                solved = True
            else:
                tree_index += 1


    def printAnswer(self):
        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.tree_array[row, col] == TENT:
                    print("C", end="")
                if self.tree_array[row, col] == TREE:
                    print("T", end="")
                if self.tree_array[row, col] == EMPTY:
                    print(".", end="")
                if self.tree_array[row, col] == CROSS:
                    print("X", end="")
            print()

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
        puzzle.solve()
        puzzle.printAnswer()
        print()
