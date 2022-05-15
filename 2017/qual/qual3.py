from dataclasses import dataclass
from math import ceil, floor

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
    q: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        [n, q] = read_ints()

        case = CaseParams(n, q)
        print(f"Case #{c}: {solve_case(case)}")
        return


def solve_case(case: CaseParams):
    buckets = [case.n]

    for k in range(case.q):
        n = buckets.pop(0)
        left = ceil((n - 1) / 2)
        right = floor((n - 1) / 2)
        buckets.append(min(left, right))
        buckets.append(max(left, right))
        print(buckets)

    return f"{left} {right}"


if __name__ == "__main__":
    solve_problem()
