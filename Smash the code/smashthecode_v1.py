import random

# ------------Paramètres Algorithme Génétique--------------------------------------------------------------------------#

NBGENOME = 10
NBGEN = 1000
MUTRATE = 5
CROSSRATE = 65

PREV = 5


# ------------Fonctions du problème------------------------------------------------------------------------------------#

def eval_grid(grid, genome, prevs):
    for i in range(PREV):
        add_to_grid(grid, genome[i], prevs[i])

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
        res = 1
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

def fitness(genome, couls):
    grid = {i: [] for i in range(6)}
    eval_grid(grid, genome, couls)
    return 5

def fitnessPop(population, couls):
    return [fitness(population[i], couls)]

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

def select(population, couls):
    temp = []
    fitnesspop = fitnessPop(population, couls)
    sumfit = sum(fitnesspop)
    for _ in range(len(population)):
        G = random.randrange(0, int(sumfit))
        res = 0
        i = 0
        while (res < G):
            res += fitnesspop[i]
            i += 1
        temp.append(population[i-1])
    return temp

def to_string_pop(population, couls):
    for ind in population:
        print(str(ind) + " " + str(fitness(ind, couls)))

# ---------------------------------------------------------------------------------------------------------------------#

Grid = {i: [] for i in range(6)}

"""
couls = [random.randint(1, 5) for _ in range(PREV)]

pop = randompop()

for i in range(NBGEN):
    pop = crossover(pop)
    pop = mutatepop(pop)
    pop = select(pop, couls)
to_string_pop(pop, couls)
"""
Grid[1] += [3]
Grid[2] += [3]
Grid[3] += [3]

add_to_grid(Grid, 0, 2)
add_to_grid(Grid, 0, 2)
add_to_grid(Grid, 0, 2)
add_to_grid(Grid, 2, 1)
add_to_grid(Grid, 2, 3)
print(to_string(Grid))

add_to_grid(Grid, 1, 1)