import sys
import random
import copy
import time

# ------------Paramètres Algorithme Génétique--------------------------------------------------------------------------#

PREV = 8
MUTRATE = 5

# ------------Fonctions du problème------------------------------------------------------------------------------------#

def ori_from_col(col):
    if col == 5:
        ori = random.randint(1, 3)
    elif col == 0:
        ori = random.randint(0, 2)
        if ori == 2:
            ori += 1
    else:
        ori = random.randint(0, 3)
    return ori


def input_to_grid():
    Grid = {i: [] for i in range(6)}
    for _ in range(12):
        line = input()
        for i in range(6):
            if line[i] != '.':
                Grid[i] = [int(line[i])] + Grid[i]
    return Grid


def output(genome):
    print(str(genome[0]) + " " + str(genome[0 + PREV]))


def eval_grid(grid, genome, couls):
    Grid = copy.deepcopy(grid)
    res = 0
    for i in range(PREV):
        B, CP, GB = add_to_grid(Grid, genome[i], genome[PREV + i], couls[i])
        if max([len(Grid[i]) for i in Grid]) >= 12:
            return 1
        if CP != 1:
            CP = 2 ** (CP + 1)
        else:
            CP = 0
        res += (10 * B) * (CP + GB)
    return 10 + res


def dfs(grid, x, y, coul, visited=None, su=None):
    if su is None:
        su = {0: set(), 1: set()}
    if visited is None:
        visited = {i: set() for i in range(6)}
    if (x >= 0) & (x <= 5):
        if (y >= 0) & (y < len(grid[x])):
            if y not in visited[x]:
                visited[x].add(y)
                if grid[x][y] == 0:
                    su[1].add((x, y))
                elif grid[x][y] == coul:
                    su[0].add((x, y))
                    dfs(grid, x + 1, y, coul, visited, su)
                    dfs(grid, x, y + 1, coul, visited, su)
                    dfs(grid, x - 1, y, coul, visited, su)
                    dfs(grid, x, y - 1, coul, visited, su)
                    return su
    return {0: set(), 1: set()}


def clean_grid_v2(grid, x1, y1, x2, y2):
    b = 0
    cp = 0
    gb = 0
    nexts = [(x1, y1), (x2, y2)]
    while nexts:
        cp += 1
        delete = set()
        for x, y in nexts:
            if (x, y) in delete:
                continue
            bloc = dfs(grid, x, y, grid[x][y], None, None)
            if len(bloc[0]) >= 4:
                b += len(bloc[0])
                gb += len(bloc[0]) - 4
                delete = delete | bloc[0] | bloc[1]
        delete = list(delete)
        delete = sorted(delete, key=lambda x: x[1], reverse=True)
        for x, y in delete:
            del grid[x][y]
        nexts = []
        for x, y in delete:
            if y < len(grid[x]):
                nexts += [(x, y)]
        print(to_string(grid))
    return [b, cp, gb]


def add_to_grid(grid, col, ori, coul):
    if ori == 0:
        grid[col] += [coul[0]]
        grid[col + 1] += [coul[1]]
        return clean_grid_v2(grid, col, len(grid[col]) - 1, col + 1, len(grid[col + 1]) - 1)
    elif ori == 1:
        grid[col] += [coul[0], coul[1]]
        return clean_grid_v2(grid, col, len(grid[col]) - 2, col, len(grid[col]) - 1)
    elif ori == 2:
        grid[col] += [coul[0]]
        grid[col + -1] += [coul[1]]
        return clean_grid_v2(grid, col, len(grid[col]) - 1, col - 1, len(grid[col - 1]) - 1)
    else:
        grid[col] += [coul[1], coul[0]]
        return clean_grid_v2(grid, col, len(grid[col]) - 2, col, len(grid[col]) - 1)


def to_string(grid):
    res = ""
    for i in grid:
        res += str(i) + " : " + str(grid[i]) + "\n"
    return res


# ------------Fonctions Génétiques-------------------------------------------------------------------------------------#

def randomgen():
    temp = [random.randint(0, 5) for _ in range(PREV)]
    for i in range(PREV):
        temp += [ori_from_col(temp[i])]
    return temp


def fitness(genome, couls, grid):
    return eval_grid(grid, genome, couls)


def mutate(genome):
    for i in range(PREV):
        if random.randrange(0, 100) <= MUTRATE:
            genome[i] = (genome[i] + random.randint(0, 2) - 1) % 6
            genome[i + PREV] = ori_from_col(genome[i])
    return genome


def hill_climbing_mutation(grid, couls, GEN):
    genome = copy.deepcopy(GEN)
    Debut = time.time()
    bestfit = fitness(genome, couls, grid)
    i = 0
    while (time.time() - Debut) <= 0.090:
        i += 1
        new_try = mutate(genome)
        new_try_fit = fitness(new_try, couls, grid)
        if new_try_fit > bestfit:
            genome = new_try
            bestfit = new_try_fit
    print("nb gen testés = " + str(i), file=sys.stderr)
    #print("best fit :" + str(bestfit), file=sys.stderr)
    return genome


def hill_climbing(grid, couls):
    Debut = time.time()
    genome = randomgen()
    bestfit = 0
    i = 0
    while (time.time() - Debut) <= 0.090:
        i += 1
        new_try = randomgen()
        new_try_fit = fitness(new_try, couls, grid)
        if new_try_fit > bestfit:
            genome = new_try
            bestfit = new_try_fit
    print("nb gen testés = " + str(i), file=sys.stderr)
    print("best fit :" + str(bestfit), file=sys.stderr)
    return genome


def next_turn(genome):
    col = random.randint(0, 5)
    ori = ori_from_col(col)
    return genome[1:PREV] + [col] + genome[PREV + 1:2 * PREV] + [ori]


# ---------------------------------------------------------------------------------------------------------------------#

gen = randomgen()

Grid = input_to_grid()
couls = [(random.randint(1, 5), random.randint(1, 5)) for _ in range(PREV)]

print(gen)
print(hill_climbing_mutation(Grid, couls, gen))
print(gen)
"""
for i in range(PREV):
    add_to_grid(Grid, gen[i], gen[PREV + i], couls[i])
"""


"""
......
......
......
......
......
.1....
.1....
.2.1..
.2.1..
12.0..
13.1..
1331.1
"""

"""
......
......
......
......
......
......
......
......
......
0.0...
3.3...
3000..
"""

"""
......
......
......
......
......
......
......
......
......
.111..
.222..
3111..
"""
