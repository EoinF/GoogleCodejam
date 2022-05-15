from dataclasses import dataclass
from itertools import combinations
from math import sqrt

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
    p: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def solve_case(case: CaseParams):
    cookies = [read_ints() for _ in range(case.n)]

    p_initial_total = 0
    ds = []
    for [h, w] in cookies:
        p_initial = 2 * h + 2 * w
        p_initial_total += p_initial
        d_min = min(h, w)
        d_max = sqrt(h**2 + w**2)
        ds.append((d_min, d_max))

    target = (case.p - p_initial_total) / 2.0

    cache = [(0, 0)]

    for current_index in range(len(ds)):
        d_min, d_max = ds[current_index]
        merged_list = []
        merge_index = 0
        for c in range(len(cache)):
            new_d_min = d_min + cache[c][0]
            if new_d_min > target:
                continue
            new_d_max = d_max + cache[c][1]

            while merge_index < len(cache) and cache[merge_index][1] < new_d_min:
                merged_list.append(cache[merge_index])
                merge_index += 1

            if merge_index >= len(cache) or (
                cache[merge_index][0] > new_d_min and cache[merge_index][1] < new_d_max
            ):
                merged_list.append((new_d_min, new_d_max))
                merge_index += 1
            else:
                merged_list.append((new_d_min, new_d_max))

        merged_list.extend(cache[merge_index:])
        cache = merged_list

    if cache[-1][0] < target and cache[-1][1] > target:
        return case.p
    else:
        return p_initial_total + cache[-1][1] * 2


if __name__ == "__main__":
    solve_problem()
