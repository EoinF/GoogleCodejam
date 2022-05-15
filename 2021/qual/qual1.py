# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


def solve_problem():
    test_cases = read_int()

    for case in range(1, test_cases + 1):
        input()  # N
        nums = read_ints()
        print(f"Case #{case}: {reverse_sort(nums)}")


def get_min_index(start, nums):
    smallest = start
    for j in range(start, len(nums)):
        if nums[j] < nums[smallest]:
            smallest = j

    return smallest


def reverse_sort(nums: "list[int]"):
    cost = 0

    for i in range(len(nums) - 1):
        j = get_min_index(i, nums)
        num_slice = nums[i : j + 1].copy()
        num_slice.reverse()
        nums = nums[:i] + num_slice + nums[j + 1 :]

        cost += j - i + 1

    return cost


if __name__ == "__main__":
    solve_problem()
