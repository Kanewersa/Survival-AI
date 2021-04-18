from collections import deque as Queue


def valid_neighbor(n, game_map, visited):
    if n[0] < 0 or n[1] < 0 or n[0] >= game_map.width or n[1] >= game_map.height:
        return False
    if visited[n[0]][n[1]]:
        return False
    if game_map.is_colliding(n):
        return False

    return True


def breadth_first_search(game_map, start, target):
    visited = [[False for _ in range(game_map.width)] for _ in range(game_map.height)]
    q = Queue()
    came_from = dict()
    came_from[start] = (-1, -1)

    q.append(start)
    visited[start[0]][start[1]] = True

    while len(q) > 0:
        cell = q.popleft()

        if cell == target:
            break

        neighbors = [
            (cell[0] - 1, cell[1]),
            (cell[0], cell[1] + 1),
            (cell[0] + 1, cell[1]),
            (cell[0], cell[1] - 1),
        ]

        for neighbor in neighbors:
            if valid_neighbor(neighbor, game_map, visited):
                q.append(neighbor)
                visited[neighbor[0]][neighbor[1]] = True
                came_from[neighbor] = cell

    path = list()
    current = target
    if came_from.get(start, None) is not None:
        path.append(start)
        return path

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    return path
