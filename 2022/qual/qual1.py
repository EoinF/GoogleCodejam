# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


def main():
    test_cases = int(input())

    for case in range(1, test_cases + 1):
        [r, c] = [int(num) for num in input().split(" ")]
        print(f"Case #{case}: {solve_problem(r, c)}")


def solve_problem(r: "int", c: "int"):
    # handle first row as special case
    line1 = ".." + "-".join(["+"] * c)
    line2 = ".." + ".".join(["|"] * c)

    row_part = ("+-" * c) + "+"
    row_separator = "\n" + ("|." * c) + "|\n"

    remaining_lines = row_separator.join([row_part] * r)

    return "\n".join(["", line1, line2, remaining_lines])


main()
