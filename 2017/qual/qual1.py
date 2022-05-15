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
    s: str
    k: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        [s, k] = read_strings()

        case = CaseParams(s, int(k))
        print(f"Case #{c}: {solve_case(case)}")


def flip(s, i, k):
    new_segment = ""
    for index in range(k):
        new_segment += "-" if s[i + index] == "+" else "+"

    return s[:i] + new_segment + s[i + k :]


def solve_case(case: CaseParams):
    i = 0

    s = case.s
    flips = 0

    while i < len(s) - (case.k - 1):
        if s[i] == "-":
            s = flip(s, i, case.k)
            flips += 1
        i += 1

    if "-" in s:
        return "IMPOSSIBLE"

    return flips


if __name__ == "__main__":
    solve_problem()
