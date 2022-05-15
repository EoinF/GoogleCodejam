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
        letters = read_strings()
        print(f"Case #{c}: {solve_case(letters)}")


def solve_case(letters: "list[str]"):

    return ""


if __name__ == "__main__":
    solve_problem()
