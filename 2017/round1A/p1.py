from cmath import pi, rect
from dataclasses import dataclass

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
    r: int
    c: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}:")
        cake = solve_case(case)
        for r in range(case.r):
            print("".join(cake[r]))


@dataclass
class Initial:
    r: int
    c: int
    value: str


def fill_section(cake, top, left, bottom, right, current_initial):
    for r in range(top, bottom + 1):
        for c in range(left, right + 1):
            cake[r][c] = current_initial


def search_next(
    cake,
    case: CaseParams,
):
    used_initials = []
    for r in range(case.r):
        for c in range(case.c):
            if cake[r][c] != "?" and cake[r][c] not in used_initials:
                current_initial = cake[r][c]
                used_initials.append(current_initial)
                left = c
                right = c
                top = r
                bottom = r
                # find longest row possible
                while left > 0 and cake[r][left - 1] == "?":
                    left -= 1

                while right < case.c - 1 and cake[r][right + 1] == "?":
                    right += 1

                # see if we can extend it upwards
                while top > 0 and all(
                    [cell == "?" for cell in cake[top - 1][left : right + 1]]
                ):
                    top -= 1

                # see if we can extend it downwards
                while bottom + 1 < case.r and all(
                    [cell == "?" for cell in cake[bottom + 1][left : right + 1]]
                ):
                    bottom += 1

                fill_section(cake, top, left, bottom, right, current_initial)


def solve_case(case: CaseParams):
    cake = []
    for r in range(case.r):
        cake.append([])
        line = input()
        for c in range(len(line)):
            cake[r].append(line[c])

    search_next(cake, case)

    return cake


if __name__ == "__main__":
    solve_problem()
