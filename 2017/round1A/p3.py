from dataclasses import dataclass
import heapq
from math import ceil, floor
from queue import PriorityQueue

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
    health: int
    attack: int
    knight_health: int
    knight_attack: int
    buff: int
    debuff: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def calculate_turns(case: CaseParams, nb, nd):
    print(f"nb={nb} nd={nd}")
    na = ceil(case.knight_health / (case.attack + case.buff * nb))
    nk = case.health / (case.knight_attack - case.debuff * nd)
    nc = floor((nk * floor((na + nb + nd - 1) / nk)) / (nk - 1))
    print(na, nb, nc, nd, nk)
    return na + nb + nc + nd


def search_next(case: CaseParams):
    min_buffs = 0
    max_buffs = (
        0 if case.buff == 0 else ceil((case.knight_health - case.attack) / case.buff)
    )
    min_debuffs = 0
    max_debuffs = (
        0 if case.debuff == 0 else floor((case.knight_attack - 1) / case.debuff)
    )
    state = []
    max_turns = 10**30
    heapq.heappush(state, (max_turns, [min_buffs, max_buffs, min_debuffs, max_debuffs]))
    lowest_turns = max_turns

    while len(state) > 0:
        (
            current_turns,
            [min_buffs, max_buffs, min_debuffs, max_debuffs],
        ) = heapq.heappop(state)

        print(
            (
                current_turns,
                [min_buffs, max_buffs, min_debuffs, max_debuffs],
            )
        )
        # search on buffs
        mid_buffs = ceil((min_buffs + max_buffs) / 2)
        mid_buffs_turns = calculate_turns(case, mid_buffs, min_debuffs)

        if mid_buffs_turns < current_turns:
            if mid_buffs_turns < lowest_turns:
                lowest_turns = mid_buffs_turns
            if min_buffs != mid_buffs:
                heapq.heappush(
                    state,
                    (mid_buffs_turns, [min_buffs, mid_buffs, min_debuffs, max_debuffs]),
                )
            if max_buffs != mid_buffs:
                heapq.heappush(
                    state,
                    (mid_buffs_turns, [mid_buffs, max_buffs, min_debuffs, max_debuffs]),
                )

        mid_debuffs = ceil((min_debuffs + max_debuffs) / 2)
        mid_debuffs_turns = calculate_turns(case, min_buffs, mid_debuffs)
        if mid_debuffs_turns < current_turns:
            if mid_debuffs_turns < lowest_turns:
                lowest_turns = mid_debuffs_turns
            if min_debuffs != mid_debuffs:
                heapq.heappush(
                    state,
                    (
                        mid_debuffs_turns,
                        [min_buffs, mid_buffs, min_debuffs, max_debuffs],
                    ),
                )
            if max_debuffs != mid_debuffs:
                heapq.heappush(
                    state,
                    (
                        mid_debuffs_turns,
                        [mid_buffs, max_buffs, min_debuffs, max_debuffs],
                    ),
                )

    if lowest_turns == max_turns:
        return "IMPOSSIBLE"
    else:
        return lowest_turns


def solve_case(case: CaseParams):
    return search_next(case)


if __name__ == "__main__":
    solve_problem()
