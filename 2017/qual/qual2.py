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
        num = input()
        print(f"Case #{c}: {solve_case(num)}")


def solve_case(num: "str"):
    total = num[-1]
    current = num[-1]

    for i in range(len(num) - 2, -1, -1):
        if num[i] > current:
            current = str(int(num[i]) - 1)
            total = "9" * len(total)
            total = current + total
        else:
            total = num[i] + total
            current = num[i]

    if total.startswith("0"):
        return total[1:]
    return total


if __name__ == "__main__":
    solve_problem()
