# simple pathfinder 
from copy import deepcopy


def get_neighbors(position, tiles, mapSize):
    neighbors = [
        (position[0], position[1] - 1),
        (position[0] + 1, position[1]),
        (position[0], position[1] + 1),
        (position[0] - 1, position[1])
    ]

    to_remove = []
    for neighbor in neighbors:
        if neighbor[0] < 0:
            to_remove.append(neighbor)
            continue

        elif neighbor[0] >= mapSize[1]:
            to_remove.append(neighbor)
            continue

        if neighbor[1] < 0:
            to_remove.append(neighbor)
            continue

        elif neighbor[1] >= mapSize[0]:
            to_remove.append(neighbor)
            continue

        if not tiles[neighbor[1]][neighbor[0]] in [0, 2, 3]:
            to_remove.append(neighbor)
    
    for neighbor in to_remove:
        neighbors.remove(neighbor)
    
    return neighbors


def find_path(start, target, tiles):
    #tiles[start[1]][start[0]]
    new_tiles = deepcopy(tiles)

    activeTiles = [[start, []]]
    new_active = [1]
    while new_active != []:
        new_active = []
        for tile in activeTiles:
            neighbors = get_neighbors(tile[0], new_tiles, (len(tiles), len(tiles[0])))
            
            for neighbor in neighbors:

                new_active.append(
                    [neighbor, tile[1] + [neighbor]]
                )
                

                if neighbor[0] == target[0] and neighbor[1] == target[1]:
                    return tile[1] + [neighbor]
                else:
                    new_tiles[neighbor[1]][neighbor[0]] = 1

        activeTiles = new_active
                
    return None
