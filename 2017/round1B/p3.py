from copy import copy
from dataclasses import dataclass
from email import iterators
from sys import stdout
from time import sleep

# region helpers


def read_int():
    return int(input())


def read_ints():
    line = input()
    return [int(s) for s in line.split(" ")]


def read_strings():
    return input().split(" ")


# endregion


@dataclass
class CaseParams:
    n: int
    q: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def get_route_data(
    b,
    h,
    distance,
    horse,
    cache,
    elapsed_time,
    path,
):
    if distance < 0 or horse[0] < distance:
        return None

    time_taken = elapsed_time + (distance / horse[1])

    if path[0] not in cache:
        cache[path[0]] = {}
    if b not in cache[path[0]]:
        cache[path[0]][b] = {}

    if h in cache[path[0]][b] and time_taken > cache[path[0]][b][h]:
        return None

    cache[path[0]][b][h] = time_taken

    new_path = copy(path)
    new_path.append(b)
    return (time_taken, new_path)


def find_fastest_route(u, v, horses, routes, cache):
    starting_horse = horses[u]
    current = (0, starting_horse, u, [u])
    frontier = [current]

    while len(frontier) > 0:
        (elapsed_time, current_horse, h, path) = frontier.pop()
        if path[-1] == v:
            continue

        for dest, distance in enumerate(routes[path[-1]]):
            route_data = get_route_data(
                dest, h, distance, current_horse, cache, elapsed_time, path
            )
            if route_data is not None:
                (time_taken, new_path) = route_data
                # keep horse
                horse_fuel = current_horse[0] - distance
                new_entry = (time_taken, (horse_fuel, current_horse[1]), h, new_path)
                frontier.append(new_entry)
                # take horse
                new_entry = (
                    time_taken,
                    (horses[dest][0], horses[dest][1]),
                    dest,
                    new_path,
                )
                frontier.append(new_entry)


def solve_case(case: CaseParams):
    horses = [read_ints() for _ in range(case.n)]
    routes = [read_ints() for _ in range(case.n)]

    pairs = [read_ints() for _ in range(case.q)]

    cache = {}

    fastest = []
    for p in pairs:
        u = p[0] - 1
        v = p[1] - 1
        find_fastest_route(u, v, horses, routes, cache)
        x = min(list(cache[u][v].values()))
        fastest.append(x)

    return " ".join(str(t) for t in fastest)


if __name__ == "__main__":
    solve_problem()
