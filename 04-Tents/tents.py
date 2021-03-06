import sys
import numpy as np

# INPUT

EMPTY = 0
TREE = -1
TENT = 1
CROSS = 2

problem = []
problems_all = []
tree_list = []

def crossOutRow(tree_array, row_num, col_length):
    for col in range(col_length):
        if tree_array[row_num, col] == EMPTY:
            tree_array[row_num, col] = CROSS
    return tree_array

def crossOutCol(tree_array, col_num, row_length):
    for row in range(row_length):
        if tree_array[row, col_num] == EMPTY:
            tree_array[row, col_num] = CROSS
    return tree_array

# First stage, this removes potential locations for tents to go
# by finding the 0's
def crossOutZeroRows(tree_array, row_counts, col_counts):
    for row, num in enumerate(row_counts):
        if num == 0:
            tree_array = crossOutRow(tree_array, row, len(col_counts))
    for col, num in enumerate(col_counts):
        if num == 0:
            tree_array = crossOutCol(tree_array, col, len(row_counts))
    return tree_array

# Second Stage, find cells that are too far away from a tree and so should
# not contain a tent.
def crossOutFarAway(tree_array, row_length, col_length):
    for row in range(row_length):
        for col in range(col_length):
            found_tree = False
            try:
                if tree_array[row - 1, col] == TREE:
                    # left
                    found_tree = True
            except:
                pass
            try:
                if tree_array[row, col - 1] == TREE:
                    # top
                    found_tree = True
            except:
                pass
            try:
                if tree_array[row + 1, col] == TREE:
                    # right
                    found_tree = True
            except:
                pass
            try:
                if tree_array[row, col + 1] == TREE:
                    # bottom
                    found_tree = True
            except:
                pass
            if not found_tree:
                if tree_array[row, col] == EMPTY:
                    tree_array[row, col] = CROSS
    return tree_array

# Count Empty counts the amount of zeroes in each row column.
def countEmpty(tree_array, row_length, col_length):
    row_zeroes = np.count_nonzero(tree_array==EMPTY, axis=1)
    col_zeroes = np.count_nonzero(tree_array==EMPTY, axis=0)
    return row_zeroes, col_zeroes

# Count Tents counts the amount of tents in each row column.
def countTents(tree_array, row_length, col_length):
    row_tents = np.count_nonzero(tree_array==TENT, axis=1)
    col_tents = np.count_nonzero(tree_array==TENT, axis=0)
    return row_tents, col_tents

# Place tents places tents in rows or columns that have free spaces equal to
# the number of tents in that row.
def placeTents(tree_array, row_counts, col_counts):
    row_zeroes, col_zeroes = countEmpty(tree_array, len(row_counts), len(col_counts))
    row_tents, col_tents = countTents(tree_array, len(row_counts), len(col_counts))
    for row, num in enumerate(row_counts):
        if row_tents[row] < num:
            if row_tents[row] + row_zeroes[row] == num:
                for col in range(len(col_counts)):
                    if tree_array[row, col] == EMPTY:
                        tree_array[row, col] = TENT
    for col, num in enumerate(col_counts):
        if col_tents[col] < num:
            if col_tents[col] + col_zeroes[col] == num:
                for row in range(len(row_counts)):
                    if tree_array[row, col] == EMPTY:
                        tree_array[row, col] = TENT
    return tree_array

# Crosses out empty spaces if the row or column has the correct number of tents.
def crossOutFull(tree_array, row_counts, col_counts):
    row_tents, col_tents = countTents(tree_array, len(row_counts), len(col_counts))
    for row, num in enumerate(row_counts):
        if row_tents[row] == num:
            for col in range(len(col_counts)):
                if tree_array[row, col] == EMPTY:
                    tree_array[row, col] = CROSS
    for col, num in enumerate(col_counts):
        if col_tents[col] == num:
            for row in range(len(row_counts)):
                if tree_array[row, col] == EMPTY:
                    tree_array[row, col] = CROSS
    return tree_array

# Cross out spaces that are diagonal, vertical or diagonal to a tent.
def crossOutTentConnection(tree_array, row_length, col_length):
    for row in range(row_length):
        for col in range(col_length):
            if tree_array[row, col] == TENT:
                try:
                    if tree_array[row - 1, col] == EMPTY:
                        # left
                        tree_array[row - 1, col] = CROSS
                except:
                    pass
                try:
                    if tree_array[row - 1, col - 1] == EMPTY:
                        # top left
                        tree_array[row - 1, col - 1] = CROSS
                except:
                    pass
                try:
                    if tree_array[row, col - 1] == EMPTY:
                        # top
                        tree_array[row, col - 1] = CROSS
                except:
                    pass
                try:
                    if tree_array[row + 1, col - 1] == EMPTY:
                        # top right
                        tree_array[row + 1, col - 1] = CROSS
                except:
                    pass
                try:
                    if tree_array[row + 1, col] == EMPTY:
                        # right
                        tree_array[row + 1, col] = CROSS
                except:
                    pass
                try:
                    if tree_array[row + 1, col + 1] == EMPTY:
                        # bottom right
                        tree_array[row + 1, col + 1] = CROSS
                except:
                    pass
                try:
                    if tree_array[row, col + 1] == EMPTY:
                        # bottom
                        tree_array[row, col + 1] = CROSS
                except:
                    pass
                try:
                    if tree_array[row - 1, col + 1] == EMPTY:
                        # bottom left
                        tree_array[row - 1, col + 1] = CROSS
                except:
                    pass
    return tree_array

# Checks if the current puzzle has been solved.
def isSolved(tree_array, row_counts, col_counts):
    row_tents, col_tents = countTents(tree_array, len(row_counts), len(col_counts))
    for row, num in enumerate(row_counts):
        if row_tents[row] != num:
            return False
    for col, num in enumerate(col_counts):
        if col_tents[col] != num:
            return False
    return True

# This needs updating, the logic needs to be much better. JK 31.05.31
# This is also going to be an expensive function.
def cornerCase(tree_array, row_length, col_length):
    for row in range(row_length):
        for col in range(col_length):
            if tree_array[row, col] == TREE:
                # create a n.n matrix for each spot next to each tree.
                # if all the matrices for a tree have an cross in a square, we can place a
                # cross in that square.
                # surely there's a numpy function for this.
    return tree_array

def tryCombinations(tree_array, row_counts, col_counts):
    tree_copy = deepcopy(tree_array)
    row_copy = deepcopy(row_counts)
    col_copy = deepcopy(col_counts)

    row_len = len(row_counts)
    col_len = len(col_counts)
    for i in range(row_len):
        if row_copy[i] != 0:
            j = 0
            while row_copy[i] > 0:
                if tree_copy[i, j] == EMPTY:
                    tree_copy[i, j] = TENT
                    row_copy[i] = row_copy[i] - 1
                    col_copy[j] = col_copy[j] - 1
                    if row_copy[i] == 0:
                        for row in range(row_len):
                            if tree_array[row, j] == EMPTY:
                                tree_array[row, j] = CROSS
                    if col_copy[i] == 0:
                        for col in range(col_len):
                            if tree_array[i, col] == EMPTY:
                                tree_array[i, col] = CROSS


                j += 1



def solveProblem(tree_list, row_counts, col_counts):
    tree_array = np.array(tree_list)

    tree_array = crossOutZeroRows(tree_array, row_counts, col_counts)

    tree_array = crossOutFarAway(tree_array, len(row_counts), len(col_counts))

    tree_array = cornerCase(tree_array, len(row_counts), len(col_counts))

    # In rows and/or columns where the number corresponds to the number of
    #  free cells, you may place a tent in all those free cells.
    while True:
        tree_array = placeTents(tree_array, row_counts, col_counts)
        tree_array = crossOutTentConnection(tree_array, len(row_counts), len(col_counts))
        tree_array = crossOutFull(tree_array, row_counts, col_counts)
        print(row_counts)
        print(col_counts)
        print(tree_array)
        if isSolved(tree_array, row_counts, col_counts):
            print("Solved!!")
            return



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
                # print(problem)
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
        solveProblem(item[0], item[1], item[2])
        #print(item)
