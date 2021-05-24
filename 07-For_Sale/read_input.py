import sys

games_all = []
game = []

for line in sys.stdin:
    if not line.isspace():
        line = line.split()
        game.append(line)
    else:
        games_all.append(game)
        game = []


strat1_scores = []
strat2_scores = []
strat3_scores = []
strat4_scores = []
strat5_scores = []
strat6_scores = []
# print(games_all)
for game in games_all:
    count = 1
    print(game)
    for line in game:
        if line[0] == 'Strat1':
            strat1_scores.append(count)
            count+= 1
        elif line[0] == 'Strat2':
            strat2_scores.append(count)
            count+=1
        elif line[0] == 'Strat3':
            strat3_scores.append(count)
            count+=1
        elif line[0] == 'Strat4':
            strat4_scores.append(count)
            count+=1
        elif line[0] == 'Strat5':
            strat5_scores.append(count)
            count+=1
        elif line[0] == 'Strat6':
            strat6_scores.append(count)
            count+=1
