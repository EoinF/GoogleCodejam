from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def solve_problem():
    test_cases = int(input())

    for case in range(1, test_cases + 1):
        [length, cost] = [int(num) for num in input().split(" ")]
        print(f"Case #{case}: {solve_case(length, cost)}")


def hash_of_array(nums):
    return str.join([str(num) for num in enumerate(nums)], ".")


def solve_case(length: "int", expected_cost: "int"):
    min_possible_cost = length - 1
    sorted_nums = [num + 1 for num in range(length)]

    frontier = PriorityQueue()
    frontier.put(
        PrioritizedItem(
            -min_possible_cost,
            {"i": length - 2, "nums": sorted_nums, "cost": min_possible_cost},
        )
    )

    while not frontier.empty():
        next = frontier.get().item
        i: "int" = next["i"]
        if next["cost"] == expected_cost:
            return " ".join([str(num) for num in next["nums"]])
        if i >= 0 and next["cost"] < expected_cost:
            for j in range(i, length):
                nums_copy: "list[int]" = next["nums"].copy()
                num_slice = nums_copy[i : j + 1].copy()
                num_slice.reverse()
                nums_copy = nums_copy[:i] + num_slice + nums_copy[j + 1 :]

                cost = next["cost"] + j - i
                frontier.put(
                    PrioritizedItem(
                        -cost, {"i": i - 1, "nums": nums_copy, "cost": cost}
                    )
                )

    return "IMPOSSIBLE"


if __name__ == "__main__":
    solve_problem()
