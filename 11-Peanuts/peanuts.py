import numpy as np
import sys

# Each problem has n = #Peanuts, m = #Pretzels.
# Make an (n + 1) x (m + 1) array whose elements are good = 1, bad = -1.

class Peanuts:
    CONST_GOOD = 1
    CONST_BAD = -1

    def __init__(self, num_peanuts: int, num_pretzels: int, rules: list):
        self.num_peanuts = num_peanuts
        self.num_pretzels = num_pretzels
        self.rules = rules
        self.game_array = np.zeros((self.num_peanuts + 1, self.num_pretzels + 1)) # Make array of all zeros
        self.move_to_make = [0, 0] #Initialise

    def Create_Array(self):
        self.game_array[0,0] = self.CONST_BAD # (0, 0) corresponds to an empty bowl so always bad!

        # i = peanuts, j = pretzels
        for i in range(self.num_peanuts + 1):
            for j in range(self.num_pretzels + 1):
                # Check where each rule takes us in the array.
                # Rules list consists of tuples (n, m) for n = preanuts, m = pretzels allowed to take
                found_good_move = False
                for rule in self.rules:
                    if ((i - rule[0] >= 0) and (j - rule[1] >= 0)): # Then the rule is possible
                        pea_pos = i - rule[0]
                        pret_pos = j - rule[1]

                        if self.game_array[pea_pos, pret_pos] == self.CONST_BAD:
                            found_good_move = True
                            self.game_array[i, j] = self.CONST_GOOD
                            self.move_to_make = rule # Record the rule, we will update this later for final square
                            #self.winning_rules[i][j] = rule
                            break # We can move on once a good move is found!


                if not found_good_move:
                    self.game_array[i, j] = self.CONST_BAD

                #Final square, want to record the good move
                if i == self.num_peanuts and j == self.num_pretzels:
                    if not found_good_move:
                        self.move_to_make = [0, 0]




 ## Input
problems = []
count = 0
curr_prob = []
curr_rules = []
for line in sys.stdin:
    if line.isspace():
        curr_prob.append(curr_rules)
        count = 0
        problems.append(curr_prob)
        curr_prob = []
        curr_rules = []
    else:
        if count == 0:
            line = line.split()
            curr_prob.append(line)
        else:
            line = line.split()
            curr_rules.append(line)
        count+= 1
curr_prob.append(curr_rules)
problems.append(curr_prob)


for prob in problems:
    num_peanuts = int(prob[0][0])
    num_pretzels = int(prob[0][1])
    rules = prob[1]
    rules_list = []
    rules_list.append([1, 0])
    rules_list.append([0, 1])

    for rule in rules:
        pea_rule = rule[0]
        pret_rule = rule[1]

        # Bit of a headache, for = we can just add the rule, for < or > we want to add each possible rule.
        # We make use of ranges and bounds.
        if pea_rule[0] == '=':
            if pret_rule[0] == '=':
                rules_list.append([int(pea_rule[1]), int(pret_rule[1])])
            elif pret_rule[0] == '<':
                bound = int(pret_rule[1])
                for y in range(bound):
                    rules_list.append([int(pea_rule[1]), y])
            elif pret_rule[0] == '>':
                lower_bound = int(pret_rule[1]) + 1
                upper_bound = num_pretzels + 1
                for y in range(lower_bound, upper_bound):
                    rules_list.append([int(pea_rule[1]), y])

        elif pea_rule[0] == '<':
            pea_bound = int(pea_rule[1])
            for x in range(pea_bound):
                if pret_rule[0] == '=':
                    rules_list.append([x, int(pret_rule[1])])
                elif pret_rule[0] == '<':
                    pret_bound = int(pret_rule[1])
                    for y in range(pret_bound):
                        rules_list.append([int(pea_rule[1]), y])
                elif pret_rule[0] == '>':
                    pret_lower_bound = int(pret_rule[1]) + 1
                    pret_upper_bound = num_pretzels + 1
                    for y in range(pret_lower_bound, pret_upper_bound):
                        rules_list.append([int(pea_rule[1]), y])

        elif pea_rule[0] == '>':
            pea_lower_bound = int(pea_rule[1]) + 1
            pea_upper_bound = num_peanuts + 1

            for x in range(pea_lower_bound, pea_upper_bound):
                if pret_rule[0] == '=':
                    rules_list.append([x, int(pret_rule[1])])
                elif pret_rule[0] == '<':
                    pret_bound = int(pret_rule[1])
                    for y in range(pret_bound):
                        rules_list.append([x, y])
                elif pret_rule[0] == '>':
                    pret_lower_bound = int(pret_rule[1]) + 1
                    pret_upper_bound = num_pretzels + 1
                    for y in range(pret_lower_bound, pret_upper_bound):
                        rules_list.append([x, y])

    problem = Peanuts(num_peanuts, num_pretzels, rules_list)
    problem.Create_Array()

    print(str(problem.move_to_make[0]) + ' ' + str(problem.move_to_make[1]))
