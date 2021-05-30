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

def solveProblem(tree_list, row_counts, col_counts):
    tree_array = np.array(tree_list)

    tree_array = crossOutZeroRows(tree_array, row_counts, col_counts)
    print(tree_array)

    tree_array = crossOutFarAway(tree_array, len(row_counts), len(col_counts))
    print(tree_array)
    ## At this stage we want to loop through the array placing tents
    ## where we think they can go until it's filled up.
    # {JK} Program works up to here... 30/05/21

    # In rows and/or columns where the number corresponds to the number of
    #  free cells, you may place a tent in all those free cells.
    total_tents = sum(row_counts)
    placed = 0
    while placed < total_tents:
        # Perform operation on rows
        ## MARK ALL SURROUNDING TILES WITH -1 AFTER PLACEMENT
        for row, row_num in enumerate(row_counts):
            # If available slots = num then place all tents
            slot_count = 0
            slot_index = []
            for col, col_num in enumerate(col_counts):
                if tree_array[row][col] == 0:
                    slot_count += 1
                    slot_index.append(col)
            if slot_count == row_num:
                for index in slot_index:
                    tree_array[row][index] = 1
                placed += row_num
        # Exact same for columns
        for col, col_num in enumerate(col_counts):
            # If available slots = num then place all tents
            slot_count = 0
            slot_index = []
            for row, row_num in enumerate(row_counts):
                if tree_array[row][col] == 0:
                    slot_count += 1
                    slot_index.append(row)
            if slot_count == col_num:
                for index in slot_index:
                    tree_array[index][col] = 1
                placed += col_num

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
