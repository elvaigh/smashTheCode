import random
import copy
# ------------Paramètres Algorithme Génétique--------------------------------------------------------------------------#

NBGENOME = 20
NBGEN = 20
MUTRATE = 5
CROSSRATE = 65

PREV = 8

# res = [B, CP, ]

# ------------Fonctions du problème------------------------------------------------------------------------------------#

def input_to_grid():
    Grid = {i: [] for i in range(6)}
    for _ in range(12):
        line = input()
        for i in range(6):
            if line[i] != '.':
                Grid[i] = [int(line[i])] + Grid[i]
    return Grid


def eval_grid(grid, genome, couls):
    Grid = copy.deepcopy(grid)
    res = 0
    for i in range(PREV):
        res += add_to_grid(Grid, genome[i], couls[i])
    #print(to_string(grid))
    return res

def dfs(grid, x, y, coul, visited, remove={i: set() for i in range(6)}):
    if (x >= 0) & (x <= 5):
        if (y >= 0) & (y < len(grid[x])):
            if y not in visited[x]:
                visited[x].add(y)
                if grid[x][y] == coul:
                    remove[x].add(y)
                    su = [(x, y)]
                    su += dfs(grid, x + 1, y, coul, visited)
                    su += dfs(grid, x, y + 1, coul, visited)
                    su += dfs(grid, x - 1, y, coul, visited)
                    su += dfs(grid, x, y - 1, coul, visited)
                    return su
    return ()


def clean_grid(grid, x, y, coul):
    res = 0
    visited = {i: set() for i in range(6)}
    bloc = sorted(dfs(grid, x, y, coul, visited), key=lambda x: x[1], reverse=True)
    if len(bloc) >= 4:
        res = len(bloc)
        for x, y in bloc:
            if y < len(grid[x]):
                del grid[x][y]
        for x, y in bloc:
            if y < len(grid[x]):
                res += clean_grid(grid, x, y, grid[x][y])
    return res


def add_to_grid(grid, col, coul):
    grid[col] += [coul, coul]
    nbblocks = clean_grid(grid, col, len(grid[col]) - 1, coul)
    return nbblocks


def to_string(grid):
    res = ""
    for i in grid:
        res += str(i) + " : " + str(grid[i]) + "\n"
    return res


# ------------Fonctions Génétiques-------------------------------------------------------------------------------------#

def randomgen():
    return [random.randint(0, 5) for _ in range(PREV)]

def fitness(genome, couls, grid):
    return eval_grid(grid, genome, couls)

def fitnessPop(population, couls, grid):
    return [fitness(population[i], couls, grid) for i in range(NBGENOME)]

def randompop():
    population = [randomgen() for _ in range(NBGENOME)]
    return population

def crossover(population):
    temp = []
    for k in range(len(population) // 2):
        p1, p2 = list(population[2 * k]), list(population[2 * k + 1])
        if random.randint(0, 100) < CROSSRATE:
            pas = random.randint(1, PREV - 1)
            temp += [p1[:pas] + p2[pas:], p2[:pas] + p1[pas:]]
        else:
            temp += [p1, p2]
    return temp

def mutatepop(population):
    return [mutate(i) for i in population]

def mutate(genome):
    for i in range(PREV):
        if random.randrange(0, 100) <= MUTRATE:
            genome[i] = random.randint(0, 5)
    return genome

def bestgenome(population, couls, grid):
    temp = fitnessPop(population, couls, grid)
    return population[temp.index(max(temp))]

def select(population, couls, grid):
    temp = []
    fitnesspop = fitnessPop(population, couls, grid)
    sumfit = (sum(fitnesspop), 1)[sum(fitnesspop) == 0]
    for _ in range(len(population)):
        G = random.randrange(0, int(sumfit))
        res = 0
        i = 0
        while (res < G):
            res += fitnesspop[i]
            i += 1
        temp.append(population[i-1])
    return temp

def to_string_pop(population, couls, grid):
    for ind in population:
        print(str(ind) + " " + str(fitness(ind, couls, grid)))

def algo_gen(grid, couls):
    pop = randompop()
    for i in range(NBGEN):
        pop = crossover(pop)
        pop = mutatepop(pop)
        pop = select(pop, couls, grid)
    to_string_pop(pop, couls, Grid)
    gen = bestgenome(pop, couls, grid)
    return gen

def next_turn(genome):
    return genome[1:] + [random.randint(0,5)]

# ---------------------------------------------------------------------------------------------------------------------#


Grid = input_to_grid()

couls = [random.randint(1, 5) for _ in range(PREV)]
print(couls)

print(to_string(Grid))

gen = algo_gen(Grid, couls)
next_gen = next_turn(gen)

print(gen)
print(fitness(gen, couls, Grid))


"""
couls = [random.randint(1, 5) for _ in range(PREV)]
add_to_grid(Grid, 0, 2)
add_to_grid(Grid, 0, 1)
add_to_grid(Grid, 0, 2)
add_to_grid(Grid, 2, 1)
add_to_grid(Grid, 2, 3)
add_to_grid(Grid, 1, 1)
genome = [0, 0, 0, 2, 2, 1]
couls = [2, 1, 2, 1, 3, 1]
print(fitness(genome, couls))
print(to_string(Grid))
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
...3..
...3..
.3.1..
.331..
"""


print(gen)
print(next_turn(gen))
