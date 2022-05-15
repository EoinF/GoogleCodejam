from cmath import pi
from dataclasses import dataclass
from itertools import combinations

# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


def read_strings():
    return input().split(" ")


# endregion


@dataclass
class CaseParams:
    n: int
    k: int


@dataclass
class Pancake:
    r: int
    h: int
    side_area: float

    def __init__(self, r, h):
        self.r = r
        self.h = h
        self.side_area = 2 * pi * r * h
        self.top_area = pi * (r**2)
        print(self.side_area)
        print(self.top_area)


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def get_best_k_minus_1(pancakes: "list[Pancake]", starting_index: int, k: int):
    return max(
        [
            sum(pancakes[i].side_area for i in combo)
            for combo in combinations(range(starting_index, len(pancakes)), k)
        ]
    )


def solve_case(case: CaseParams):
    pancakes = [Pancake(*read_ints()) for _ in range(case.n)]

    pancakes.sort(key=lambda p: p.r, reverse=True)

    cache = {n: {} for n in range(case.n + 1)}

    best_area = 0

    if case.k == case.n:
        return pancakes[0].top_area + sum(p.side_area for p in pancakes)

    for index, p in enumerate(pancakes[: 1 + len(pancakes) - case.k]):
        # solve best k for p
        cache[index][case.k - 1] = get_best_k_minus_1(pancakes, index + 1, case.k - 1)

        current_area = p.side_area + p.top_area + cache[index][case.k - 1]
        if current_area > best_area:
            best_area = current_area

    return best_area


if __name__ == "__main__":
    solve_problem()
