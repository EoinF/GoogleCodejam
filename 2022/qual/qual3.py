# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


def main():
    test_cases = read_int()

    for case in range(1, test_cases + 1):
        input()  # N
        nums = read_ints()
        print(f"Case #{case}: {solve_problem(nums)}")


def solve_problem(nums: "list[int]"):
    nums.sort()

    straight = 0
    for num in nums:
        if num > straight:
            straight += 1

    return f"{straight}"


main()
