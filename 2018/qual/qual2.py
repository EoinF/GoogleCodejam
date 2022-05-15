# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


def read_strings():
    return input().split(" ")


# endregion


def solve_problem():
    test_cases = int(input())

    for c in range(1, test_cases + 1):
        n = read_int()  # N
        nums = read_ints()
        print(f"Case #{c}: {solve_case(nums)}")


def solve_case(nums: "list[int]"):
    odds = []
    evens = []
    for index, num in enumerate(nums):
        if index % 2 == 1:
            odds.append(num)
        else:
            evens.append(num)

    odds.sort()
    evens.sort()

    for i in range(len(odds)):
        if evens[i] > odds[i]:
            return i * 2
        if i + 1 < len(evens) and odds[i] > evens[i + 1]:
            return (i * 2) + 1

    return "OK"


if __name__ == "__main__":
    solve_problem()
