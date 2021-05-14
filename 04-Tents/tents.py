import sys
import numpy as np

# INPUT

empty = 0
tree = -1
tent = 1

problem = []
problems_all = []
tree_list = []

def solveProblem(tree_list, row_counts, col_counts):
    tree_array = np.array(tree_list)
    # First stage, this removes potential locations for tents to go
    # by finding the 0's
    for row, num in enumerate(row_counts):
        if num == "0":
            tree_array[row] = -1  #* np.ones(len(col_counts))
    for col, num in enumerate(col_counts):
        if num == '0':
            tree_array[:, col] = -1

    for row, row_num in enumerate(row_counts):
        if row_num == '0':
            tree_array[row] = -1
        else:
            for col, col_num in enumerate(col_counts):
                if col_num == '0':
                    tree_array[:, col] = -1
                else:
                    # Check if tree is adjacent.
                    found_tree = False
                    # Need to wrap in try/excpet as can get out of bounds error
                    while True:
                        try:
                            if tree_list[row - 1][col] == -1:
                                found_tree = True
                                break
                        except:
                            pass
                        try:
                            if tree_list[row][col - 1] == -1:
                                found_tree = True
                                break
                        except:
                            pass
                        try:
                            if tree_list[row + 1][col] == -1:
                                found_tree = True
                                break
                        except:
                            pass
                        try:
                            if tree_list[row][col + 1] == -1:
                                found_tree = True
                                break
                        except:
                            pass
                        break
                    if not found_tree:
                        tree_array[row][col] = -1
        ## At this stage we want to loop through the array placing tents
        ## where we think they can go until it's filled up.
    total_tents = sum(row_counts)
    placed = 0
    print(tree_array)
    while placed < total_tents:
        print(placed)
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
                        row.append(empty)
                    elif character == 'T':
                        row.append(tree)
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
                    problems_all.append(problem.copy())
                    problem.clear()
                    second_row = False

    for item in problems_all:
        #solveProblem(item[0], item[1], item[2])
        print(item)
