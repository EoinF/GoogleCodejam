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
    n: int
    m: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def solve_case(case: CaseParams):
    nums = read_ints()

    initial_sum = sum(nums)
    initial_squared_sums = sum([num * num for num in nums])

    if initial_sum**2 == initial_squared_sums:
        return 0

    low = -(10**18)
    high = 10**18

    while low <= high:
        mid = (low + high) // 2

        left_side = (initial_sum + mid) ** 2
        right_side = initial_squared_sums + (mid * mid)

        if left_side == right_side:
            return mid

        if (initial_sum > 0 and left_side > right_side) or (
            initial_sum < 0 and right_side > left_side
        ):
            high = mid - 1
        else:
            low = mid + 1

    return "IMPOSSIBLE"


if __name__ == "__main__":
    solve_problem()
