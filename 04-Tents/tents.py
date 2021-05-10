import sys
import numpy as np

# INPUT

empty = 0
tree = -1
tent = 1

problem = []
problems_all = []
tree_list = []
counts = []
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
            counts.append(line)
    else:
        problem.append(tree_list)
        problem.append(counts)
        problems_all.append(problem)
        tree_list = []
        counts = []
problem.append(tree_list)
problem.append(counts)
problems_all.append(problem)


for prob in problems_all:
    tree_list = prob[0]
    tree_array = np.array(prob[0])
    counts = prob[1].copy()
    row_counts = counts[0]
    col_counts = counts[1]

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




    print(tree_array)
