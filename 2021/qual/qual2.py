# region helpers


def read_int():
    return int(input())


def read_ints():
    return [int(s) for s in input().split(" ")]


# endregion


def solve_problem():
    test_cases = int(input())

    for case in range(1, test_cases + 1):
        [x, y, letters] = input().split(" ")
        print(f"Case #{case}: {solve_case(int(x), int(y), letters)}")


def calculate_cost(last_known_letter, next_letter, gap_length, x, y):
    cost = 0
    last_known_letter_used = next_letter

    if last_known_letter == next_letter or last_known_letter is None:
        pass
    elif last_known_letter == "C":
        cost += x
    else:
        cost += y

    return [cost, last_known_letter_used]


def solve_case(x: "int", y: "int", letters: "str"):
    cost = 0
    last_known_letter = None
    gap_length = 0
    for letter in letters:
        if letter == "?":
            gap_length += 1
        else:
            if gap_length == 0 and last_known_letter is not None:
                if letter == "C" and last_known_letter == "J":
                    # print(f"no gap, cost={y}")
                    cost += y
                elif letter == "J" and last_known_letter == "C":
                    # print(f"no gap, cost={x}")
                    cost += x
            else:
                [gap_cost, last_known_letter_used] = calculate_cost(
                    last_known_letter, letter, gap_length, x, y
                )

                # print(f"gap, letter={last_known_letter_used} cost={gap_cost}")
                last_known_letter = last_known_letter_used
                gap_length = 0
                cost += gap_cost

            last_known_letter = letter

    return cost


if __name__ == "__main__":
    solve_problem()
