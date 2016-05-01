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


def eval_grid(grid):
    blocs = 0
    return blocs


def clean_grid(grid, x, y, coul):
    visited = {i: set() for i in range(6)}
    bloc = dfs(grid, x, y, coul, visited)
    if len(bloc) >= 4:
        #print(to_string(grid))
        for x, y in bloc:
            if y < len(grid[x]):
                del grid[x][y]
           # print(to_string(grid))
        for x, y in bloc:
            if y < len(grid[x]):
                clean_grid(grid, x, y, grid[x][y])

def add_to_grid(grid, col, coul):
    grid[col] += [coul, coul]
    clean_grid(grid, col, len(grid[col]) - 1, coul)


def to_string(grid):
    res = ""
    for i in grid:
        res += str(i) + " : " + str(grid[i]) + "\n"
    return res


Grid = {i: [] for i in range(6)}
Visited = {i: set() for i in range(6)}
Grid[2] += [3]
Grid[3] += [3]



add_to_grid(Grid, 0, 2)
print(to_string(Grid))
add_to_grid(Grid, 0, 1)
print(to_string(Grid))
add_to_grid(Grid, 0, 2)
print(to_string(Grid))
add_to_grid(Grid, 2, 1)
print(to_string(Grid))
add_to_grid(Grid, 2, 3)
print(to_string(Grid))
add_to_grid(Grid, 1, 1)
print(to_string(Grid))
