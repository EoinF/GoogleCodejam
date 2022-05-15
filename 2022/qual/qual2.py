# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


def main():
    test_cases = int(input())

    for case in range(1, test_cases + 1):
        p1 = [int(num) for num in input().split(" ")]
        p2 = [int(num) for num in input().split(" ")]
        p3 = [int(num) for num in input().split(" ")]

        print(f"Case #{case}: {solve_problem([p1, p2, p3])}")


def solve_problem(nums: "list[list[int]]"):
    smallest_common_values = []
    target_total = 10**6
    for i in range(4):
        smallest_common_values.append(min([nums[p][i] for p in range(3)]))

    if sum(smallest_common_values) < target_total:
        return "IMPOSSIBLE"

    total = smallest_common_values[0]
    i = 1
    while total < target_total:
        total += smallest_common_values[i]
        i += 1

    smallest_common_values[i - 1] -= total - target_total

    return " ".join([str(num) for num in smallest_common_values[:i]]) + " 0" * (
        1 + len(nums) - i
    )


main()
