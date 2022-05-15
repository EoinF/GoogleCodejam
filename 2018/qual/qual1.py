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
        [shield, letters] = read_strings()
        print(f"Case #{c}: {solve_case(letters, int(shield))}")


def solve_case(letters: "str", shield: int):
    strength = 1
    damage_dealt = 0

    moves = [c for c in letters]
    for move in moves:
        if move == "C":
            strength *= 2
        else:
            damage_dealt += strength

    hacks = 0
    # print(moves)
    for i in reversed(range(len(moves))):
        if moves[i] == "C":
            strength //= 2
            for j in range(i, len(moves) - 1):
                if damage_dealt <= shield:
                    return hacks
                if moves[j + 1] == "S":
                    temp = moves[j + 1]
                    moves[j + 1] = moves[j]
                    moves[j] = temp
                    damage_dealt -= strength
                    hacks += 1
                else:
                    break

    if damage_dealt <= shield:
        return hacks
    return "IMPOSSIBLE"


if __name__ == "__main__":
    solve_problem()
