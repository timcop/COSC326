import sys
import numpy as np
import copy

# Etude 04 - Tents and Trees.

# Group: Ethan Fraser 6338284, Jordan Kettles 2147684,
# Magdeline Huang 2824402, Tim Copland 250163

EMPTY = 0
TREE = -1
TENT = 1
CROSS = 2
POSSIBLE = 3

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
            if tree_array[row, col] == EMPTY:
                found_tree = False
                if col > 0:
                    if tree_array[row, col - 1] == TREE:
                        # left
                        found_tree = True
                if row > 0:
                    if tree_array[row - 1, col] == TREE:
                        # top
                        found_tree = True
                if col < col_length - 1 :
                    if tree_array[row, col + 1] == TREE:
                        # right
                        found_tree = True
                if row < row_length - 1:
                    if tree_array[row + 1, col] == TREE:
                        # bottom
                        found_tree = True
                if not found_tree:
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
    placedATent = False
    row_zeroes, col_zeroes = countEmpty(tree_array, len(row_counts), len(col_counts))
    row_tents, col_tents = countTents(tree_array, len(row_counts), len(col_counts))
    for row, num in enumerate(row_counts):
        if row_tents[row] < num:
            if row_tents[row] + row_zeroes[row] == num:
                for col in range(len(col_counts)):
                    if tree_array[row, col] == EMPTY:
                        tree_array[row, col] = TENT
                        placedATent = True
    for col, num in enumerate(col_counts):
        if col_tents[col] < num:
            if col_tents[col] + col_zeroes[col] == num:
                for row in range(len(row_counts)):
                    if tree_array[row, col] == EMPTY:
                        tree_array[row, col] = TENT
                        placedATent = True
    return tree_array, placedATent

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
                if col > 0:
                    if tree_array[row, col - 1] == EMPTY:
                        # left
                        tree_array[row, col - 1] = CROSS
                if col > 0 and row > 0:
                    if tree_array[row - 1, col - 1] == EMPTY:
                        # top left
                        tree_array[row - 1, col - 1] = CROSS
                if row > 0:
                    if tree_array[row - 1, col] == EMPTY:
                        # top
                        tree_array[row - 1, col] = CROSS
                if col < (col_length - 1) and row > 0:
                    if tree_array[row - 1, col + 1] == EMPTY:
                        # top right
                        tree_array[row - 1, col + 1] = CROSS
                if col < col_length - 1:
                    if tree_array[row, col + 1] == EMPTY:
                        # right
                        tree_array[row, col + 1] = CROSS
                if row < (row_length - 1) and col < (col_length - 1):
                    if tree_array[row + 1, col + 1] == EMPTY:
                        # bottom right
                        tree_array[row + 1, col + 1] = CROSS
                if row < row_length - 1:
                    if tree_array[row + 1, col] == EMPTY:
                        # bottom
                        tree_array[row + 1, col] = CROSS
                if row < (row_length - 1) and col > 0:
                    if tree_array[row + 1, col - 1] == EMPTY:
                        # bottom left
                        tree_array[row + 1, col - 1] = CROSS
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

# This function adds a cross in a copy of the tree array at each location
# adjacent to a possible tent.
def excludePossibleAdjacent(tree_array, row, col, row_length, col_length):
    array_copy = copy.deepcopy(tree_array)
    if col > 0:
        #left
        if array_copy[row, col - 1] == EMPTY:
            array_copy[row, col - 1] = POSSIBLE
    if row > 0:
        #top
        if array_copy[row - 1, col] == EMPTY:
            array_copy[row - 1, col] = POSSIBLE
    if col < col_length - 1:
        #right
        if array_copy[row, col + 1] == EMPTY:
            array_copy[row, col + 1] = POSSIBLE
    if row < row_length - 1:
        #bottom
        if array_copy[row + 1, col] == EMPTY:
            array_copy[row + 1, col] = POSSIBLE
    return array_copy

# Exclude All Possible places a cross in the row, col position of the tree
# array if all arrays in the array list also have a cross in that position.
# Returns tree_array.
def excludeAllPossible(tree_array, array_list, row, col, row_length, col_length):
    start_tree = array_list[0]
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            all_elements = True
            for tree in array_list[1:]:
                if i >= 0 and i < row_length and j >= 0 and j < row_length:
                    if tree_array[i, j] == tree[i, j] or tree[i, j] != start_tree[i, j]:
                        all_elements = False
                        break
                    if all_elements:
                        tree_array[i, j] = CROSS

    return tree_array


def excludeCorners(tree_array, row, col, row_length, col_length):
    try:
        if tree_array[row + 1, col] == CROSS:
            tree_array[row_length, col_length]
    except:
        try:
            if tree_array[row, col - 1] == CROSS:
                tree_array[row_length, col_length]
        except:
            tree_array[row-1, col + 1] = CROSS
    try:
        if tree_array[row -1, col] == CROSS:
            tree_array[row_length, col_length]
    except:
        try:
            if tree_array[row, col + 1] == CROSS:
                tree_array[row_length, col_length]
        except:
            tree_array[row+1, col - 1] = CROSS
    #add left and bottom, top and right


# Corner case checks if a square cannot have a tent in it if all possible spots
# for a tree's tent would make it impossible for a tent to be in that spot.
def cornerCase(tree_array, row_length, col_length):
    for row in range(row_length):
        for col in range(col_length):
            if tree_array[row, col] == TREE:
                array_list = list()
                if col > 0:
                    # left
                    if tree_array[row, col - 1] == EMPTY:
                        array_list.append(excludePossibleAdjacent(tree_array, row, col - 1, row_length, col_length))
                if col < col_length - 1:
                    # right
                    if tree_array[row, col + 1] == EMPTY:
                        array_list.append(excludePossibleAdjacent(tree_array, row, col + 1, row_length, col_length))
                if row > 0:
                    # top
                    if tree_array[row - 1, col] == EMPTY:
                        array_list.append(excludePossibleAdjacent(tree_array, row - 1, col, row_length, col_length))
                if row < row_length - 1:
                    # bottom
                    if tree_array[row + 1, col] == EMPTY:
                        array_list.append(excludePossibleAdjacent(tree_array, row + 1, col, row_length, col_length))
                if len(array_list) == 2:
                    tree_array = excludeAllPossible(tree_array, array_list, row, col, row_length, col_length)

    return tree_array

# Nicely prints tree_array, row_counts, and col_counts
def printProblem(tree_array, row_counts, col_counts):
    for col in col_counts:
        print(' ', col, end='')
    print()
    for i, num in enumerate(row_counts):
        print(tree_array[i], " ", num)

def printAnswer(tree_array, row_length, col_length):
    for row in range(row_length):
        for col in range(col_length):
            if tree_array[row, col] == TENT:
                print("C", end="")
            if tree_array[row, col] == TREE:
                print("T", end="")
            if tree_array[row, col] == CROSS:
                print(".", end="")
        print()

def hasEmpties(tree_array, i, j, row_length, col_length):
    for row in range(i - 1, i + 2):
        for col in range(j - 1, j + 2):
            if row >= 0 and row < row_length and col >= 0 and col < col_length:
                if tree_array[row, col] == EMPTY:
                    return True

def placeRandomTent(tree_array, row_counts, col_counts):
    row_length = len(row_counts)
    col_length = len(col_counts)
    i = j = 0
    try:
        while True:
            if tree_array[i, j] == TREE:
                if hasEmpties(tree_array, i, j, row_length, col_length):
                    break
            if i == len(row_counts) - 1:
                i = 0;
                j += 1;
            else:
                i += 1;
    except:
        print("No trees in the array.")
        exit(-1)

    free_positions = list()
    for row in range(i - 1, i + 2):
        for col in range(j - 1, j + 2):
            if row >= 0 and row < row_length and col >= 0 and col < col_length:
                if tree_array[row, col] == EMPTY:
                    free_positions.append([row, col])

    for position in free_positions:
        array_copy = copy.deepcopy(tree_array)
        array_copy[position[0], position[1]] = TENT
        array_copy = solveProblem(array_copy, row_counts, col_counts)
        if array_copy is not None:
            return array_copy
        else:
            continue

def isValid(tree_array, row_counts, col_counts):
    row_zeroes, col_zeroes = countEmpty(tree_array, len(row_counts), len(col_counts))
    row_tents, col_tents = countTents(tree_array, len(row_counts), len(col_counts))
    for row, num in enumerate(row_counts):
        if row_tents[row] != num and row_zeroes[row] == 0:
            return False
    for col, num in enumerate(col_counts):
        if col_tents[col] != num and col_zeroes[col] == 0:
            return False
    return True



def solveProblem(tree_array, row_counts, col_counts):
    placedATent = True
    while placedATent:
        placedATent = False
        tree_array, placedATent = placeTents(tree_array, row_counts, col_counts)
        if placedATent:
            if not isValid(tree_array, row_counts, col_counts):
                return None
        tree_array = crossOutTentConnection(tree_array, len(row_counts), len(col_counts))
        tree_array = crossOutFull(tree_array, row_counts, col_counts)
        tree_array = cornerCase(tree_array, len(row_counts), len(col_counts))
        tree_array, placedATent = placeTents(tree_array, row_counts, col_counts)
        if isValid(tree_array, row_counts, col_counts):
            if isSolved(tree_array, row_counts, col_counts):
                return crossOutFull(tree_array, row_counts, col_counts)
        else:
            return None
    return placeRandomTent(tree_array, row_counts, col_counts)

def startProblem(tree_list, row_counts, col_counts):
    tree_array = np.array(tree_list)
    tree_array = crossOutZeroRows(tree_array, row_counts, col_counts)
    tree_array = crossOutFarAway(tree_array, len(row_counts), len(col_counts))
    answer = solveProblem(tree_array, row_counts, col_counts)
    printAnswer(answer, len(row_counts), len(col_counts))




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
        startProblem(item[0], item[1], item[2])
        print()
