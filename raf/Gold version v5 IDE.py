import sys
import random
import copy
import time
from operator import itemgetter

# ------------Paramètres Algorithme Génétique--------------------------------------------------------------------------#

PREV = 5
NBGENOME = 46
CROSSRATE = 20
MUTRATE = 15


# ------------Fonctions du problème------------------------------------------------------------------------------------#

def ori_from_col(col):
    if col == 5:
        return random.randint(1, 3)
    elif col == 0:
        ori = random.randint(0, 2)
        if ori == 2:
            return ori + 1
        return ori
    return random.randint(0, 3)


def input_to_grid(inp=None):
    Grid = {i: [] for i in range(6)}
    Grid[6] = [-1] * 6
    if inp is None:
        for j in range(12):
            line = input()
            for i in range(6):
                if line[i] != '.':
                    if Grid[6][i] == -1: Grid[6][i] = 12 - j
                    Grid[i] = [int(line[i])] + Grid[i]
        return Grid
    for j in range(12):
        line = inp[j]
        for i in range(6):
            if line[i] != '.':
                if Grid[6][i] == -1: Grid[6][i] = 12 - j
                Grid[i] = [int(line[i])] + Grid[i]
    return Grid


def output(genome):
    print(str(genome[0]) + " " + str(genome[0 + PREV]))


def eval_grid(grid, genome, couls):
    Grid = copy.deepcopy(grid)
    res = 0
    for i in range(PREV):
        B, CP, CB, GB = add_to_grid(Grid, genome[i], genome[PREV + i], couls[i])
        if [B, CP, CB, GB] == [-1,-1,-1,-1]:
            return 5
        CP = (2 ** (CP + 1), 0)[CP == 1]
        CB = (2 ** (CB - 1), 0)[CB == 1]
        temp = (10 * B) * (CP + CB + GB)
        if CP == 4:
            temp *= 5
        res += temp
    return 40 + res


def dfs(grid, x, y, coul, visited=None, su=None):
    if su is None:
        su = {0: set(), 1: set()}
    if visited is None:
        visited = {i: set() for i in range(6)}
    if (x >= 0) & (x <= 5):
        if (y >= 0) & (y < grid[6][x]):
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
    couls = set()
    nexts = [(x1, y1), (x2, y2)]
    while nexts:
        cp += 1
        delete = set()
        for x, y in nexts:
            if (x, y) in delete:
                continue
            bloc = dfs(grid, x, y, grid[x][y], None, None)
            if len(bloc[0]) >= 4:
                couls.add(grid[x][y])
                b += len(bloc[0])
                gb += len(bloc[0]) - 4
                delete = delete | bloc[0] | bloc[1]
        delete = sorted(list(delete), key=lambda k: k[1], reverse=True)
        for x, y in delete:
            del grid[x][y]
            grid[6][x] -= 1
        nexts = []
        for x, y in delete:
            if y < grid[6][x]:
                nexts += [(x, y)]
                # print(to_string(grid))
    return [b, cp, len(couls), gb]


def add_to_grid(grid, col, ori, coul):
    if ori == 0:
        grid[col] += [coul[0]]
        grid[col + 1] += [coul[1]]
        grid[6][col] += 1
        grid[6][col + 1] += 1
        if (grid[6][col] > 11) | (grid[6][col + 1] > 11):
            return [-1,-1,-1,-1]
        return clean_grid_v2(grid, col, grid[6][col] - 1, col + 1, grid[6][col + 1] - 1)
    elif ori == 1:
        grid[col] += [coul[0], coul[1]]
        grid[6][col] += 2
        if grid[6][col] > 11:
            return [-1,-1,-1,-1]
        return clean_grid_v2(grid, col, grid[6][col] - 2, col, grid[6][col] - 1)
    elif ori == 2:
        grid[col] += [coul[0]]
        grid[col + -1] += [coul[1]]
        grid[6][col] += 1
        grid[6][col - 1] += 1
        if (grid[6][col] > 11) | (grid[6][col - 1] > 11):
            return [-1,-1,-1,-1]
        return clean_grid_v2(grid, col, grid[6][col] - 1, col - 1, grid[6][col - 1] - 1)
    else:
        grid[col] += [coul[1], coul[0]]
        grid[6][col] += 2
        if grid[6][col] > 11:
            return [-1,-1,-1,-1]
        return clean_grid_v2(grid, col, grid[6][col] - 2, col, grid[6][col] - 1)


def to_string(grid):
    res = ""
    for i in range(6):
        res += str(i) + " : " + str(grid[i]) + "\n"
    res += str("hights : " + str(grid[6]))
    return res


# ------------Fonctions Génétiques-------------------------------------------------------------------------------------#

def genome_to_string(genome):
    chaine = (str(w) for w in genome)
    return "".join(chaine)


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
            genome[i] = random.randint(0, 5)
            genome[i + PREV] = ori_from_col(genome[i])
    return genome


def fitnessPop(population, couls, grid, tested):
    temp = []
    for i in range(NBGENOME):
        genstr = genome_to_string(population[i])
        if genstr not in tested:
            tested[genstr] = fitness(population[i], couls, grid)
        temp.append(tested[genstr])
    return temp, tested


def randompop(k):
    return [randomgen() for _ in range(k)]


def crossover(population):
    temp = []
    for k in range(NBGENOME // 2):
        p1, p2 = list(population[2 * k]), list(population[2 * k + 1])
        if random.randint(0, 100) < CROSSRATE:
            pas = random.randint(1, PREV - 1)
            temp += [p1[:pas] + p2[pas:PREV] + p1[PREV:PREV + pas] + p2[PREV + pas:2 * PREV]]
            temp += [p2[:pas] + p1[pas:PREV] + p2[PREV:PREV + pas] + p1[PREV + pas:2 * PREV]]
        else:
            temp += [p1, p2]
    return temp


def mutatepop(population):
    return [mutate(i) for i in population]


def bestgenome(population, couls, grid):
    temp = fitnessPop(population, couls, grid)
    return population[temp.index(max(temp))]


def select(population, couls, grid, tested):
    fitnesspop, tested = fitnessPop(population, couls, grid, tested)
    bestfit = max(fitnesspop)
    bestgen = population[fitnesspop.index(bestfit)]
    temp = [bestgen]
    sumfit = int((sum(fitnesspop), 1)[sum(fitnesspop) == 0])
    for _ in range(NBGENOME - 1):
        G = random.randrange(0, sumfit)
        res = 0
        i = 0
        while res < G:
            res += fitnesspop[i]
            i += 1
        temp.append(population[i - 1])
    return temp, (bestgen, bestfit)


def to_string_pop(population, couls, grid):
    for ind in population:
        print(str(ind) + " " + str(fitness(ind, couls, grid)))


def to_string_pop_v2(population):
    for indiv in population:
        print(str(indiv))


def next_turn(genome):
    col = random.randint(0, 5)
    ori = ori_from_col(col)
    return genome[1:PREV] + [col] + genome[PREV + 1:2 * PREV] + [ori]


def algo_gen(grid, couls, i, previous):
    temps = 0.097
    if i == 1: temps = 0.47
    pop = previous + randompop(NBGENOME - len(previous))
    k = 0
    debut = time.time()
    bestgens = []
    nexts = []
    tested = dict()
    while (time.time() - debut) <= temps:
        k += 1
        pop = crossover(pop)
        if (time.time() - debut + 0.001) > (temps): break
        pop = mutatepop(pop)
        if (time.time() - debut + 0.015) > (temps): break
        pop, bestgen = select(pop, couls, grid, tested)
        bestgens.append(bestgen)
        nexts.append(next_turn(bestgen[0]))
    print("nb de fitness enregistrées :" + str(len(tested)), file=sys.stderr)
    print("nb generation testés =  " + str(k), file=sys.stderr)
    print(time.time() - debut, file=sys.stderr)
    best = max(bestgens, key=itemgetter(1))
    print(best, file=sys.stderr)
    return best, nexts


# ---------------------------------------------------------------------------------------------------------------------#

gen = randomgen()
i = 0
previous = []

while True:
    i += 1
    couls = []
    for i in range(8):
        color_a, color_b = [int(j) for j in input().split()]
        if i < PREV: couls.append((color_a, color_b))

    Grid = input_to_grid()

    for i in range(12):
        row = input()

    # Solution du tour précédent
    gen = next_turn(gen)
    fitgen = fitness(gen, couls, Grid)

    # Nouvel essai (via algo-gen)
    best, previous = algo_gen(Grid, couls, i, previous)
    new_try_gen, new_try_fit = best

    print("next turn gen :" + str(gen) + " " + str(fitgen), file=sys.stderr)
    print("new try G A   :" + str(new_try_gen) + " " + str(new_try_fit), file=sys.stderr)

    if new_try_fit > fitgen:
        gen = new_try_gen

    output(gen)
