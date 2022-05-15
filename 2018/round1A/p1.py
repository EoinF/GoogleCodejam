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
    r: int
    c: int
    h: int
    v: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def get_horizontal_cuts(grid, v_start, v_end, target, h):
    h_cut_ranges = []
    last_h_cut_start = 0
    chips_count = 0

    for r in range(len(grid)):
        row = grid[r]
        chips_count += sum(row[v_start:v_end])
        if chips_count == 0 and last_h_cut_start > 0:
            h_cut_ranges[-1][1] += 1
        else:
            last_h_cut_start = 0
        if chips_count > target:
            return None
        elif chips_count == target:
            chips_count = 0
            h_cut_ranges.append([r + 1, r + 1])
            last_h_cut_start = r + 1

    if len(h_cut_ranges) != h + 1 or chips_count != 0:
        return None
    return h_cut_ranges[:-1]  # last cut is just the end of the slice


def check_v_combo(grid, v_combo, target, h):
    # first figure out positions of horizontal cuts
    v_cut = v_combo[0]
    v_start = 0
    v_end = v_cut + 1
    h_cuts_ranges = get_horizontal_cuts(grid, v_start, v_end, target, h)

    if h_cuts_ranges is None:
        return False

    for v_cut in v_combo[1:]:
        v_start = v_end
        v_end = v_cut + 1
        h_cuts_other = get_horizontal_cuts(grid, v_start, v_end, target, h)

        if h_cuts_other is None:
            return False
        for index, [h_start, h_end] in enumerate(h_cuts_ranges):
            if h_cuts_other[index][1] < h_start or h_cuts_other[index][0] > h_end:
                return False

    # check the last portion
    h_cuts_other = get_horizontal_cuts(grid, v_end, len(grid[0]), target, h)

    if h_cuts_other is None:
        return False
    for index, [h_start, h_end] in enumerate(h_cuts_ranges):
        if h_cuts_other[index][1] < h_start or h_cuts_other[index][0] > h_end:
            return False

    return True


def search_next(grid, v: int, h: int, target: int):
    vertical_combos = combinations(range(len(grid[0]) - 1), v)

    for v_combo in vertical_combos:
        if check_v_combo(grid, v_combo, target, h):
            return True

    return False


def solve_case(case: CaseParams):
    grid = []
    total = 0

    for r in range(case.r):
        grid.append([])
        chips = input()
        for c in chips:
            chip = 1 if c == "@" else 0
            total += chip
            grid[r].append(chip)

    if total == 0:
        return "POSSIBLE"

    target = total // ((case.h + 1) * (case.v + 1))

    if target == 0 or total / target != ((case.h + 1) * (case.v + 1)):
        return "IMPOSSIBLE"

    if search_next(grid, case.v, case.h, int(target)):
        return "POSSIBLE"
    else:
        return "IMPOSSIBLE"


if __name__ == "__main__":
    solve_problem()
