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
    p: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def solve_case(case: CaseParams):
    recipe = read_ints()

    min_allowed = [0.9 * r for r in recipe]
    max_allowed = [1.1 * r for r in recipe]

    current_packet_index = [0] * case.n

    current_max_portions = 1
    current_min_portions = 1
    total_packaged = 0

    packets = []
    for _ in range(case.n):
        row = read_ints()
        row.sort()
        packets.append(row)
    amount = packets[0][current_packet_index[0]]
    current_min_portions = max(1, ceil(amount / max_allowed[0]))
    current_max_portions = max(1, floor(amount / min_allowed[0]))

    while True:
        # find a packet from each ingredient
        i = 0
        while i < case.n:
            if current_packet_index[i] >= case.p:
                return total_packaged
            amount = packets[i][current_packet_index[i]]
            min_portions = ceil(amount / max_allowed[i])
            max_portions = floor(amount / min_allowed[i])

            while (
                max_portions < current_min_portions
                or amount < min_portions * min_allowed[i]
                or amount > max_portions * max_allowed[i]
            ):
                # print(amount < min_portions * min_allowed[i])
                # print(amount > max_portions * max_allowed[i])
                current_packet_index[i] += 1
                if current_packet_index[i] >= case.p:
                    return total_packaged
                amount = packets[i][current_packet_index[i]]
                min_portions = ceil(amount / max_allowed[i])
                max_portions = floor(amount / min_allowed[i])

            if min_portions > current_max_portions:
                current_min_portions = min_portions
                current_max_portions = max_portions
                i = 0  # restart with new portion amount
            else:
                if max_portions < current_max_portions:
                    current_max_portions = max_portions
                if min_portions > current_min_portions:
                    current_min_portions = min_portions
                i += 1
            current_min_portions = min_portions
        # after while (we found a common arrangement for each ingredient)

        total_packaged += 1
        for c in range(len(current_packet_index)):
            current_packet_index[c] += 1
    return total_packaged


if __name__ == "__main__":
    solve_problem()
