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
    d: int
    n: int


def solve_problem():
    test_cases = read_int()

    for c in range(1, test_cases + 1):
        case = CaseParams(*read_ints())
        print(f"Case #{c}: {solve_case(case)}")


def solve_case(case: CaseParams):
    [position, speed] = read_ints()
    speeds = [speed]
    positions = [position]
    for _ in range(case.n - 1):
        [position, speed] = read_ints()
        index = 0
        while index < len(positions) and positions[index] > position:
            index += 1

        positions.insert(index, position)
        speeds.insert(index, speed)

    s_max = speeds[0]
    start_position = positions[0]
    end_position = case.d
    for i in range(case.n - 1):
        if speeds[i + 1] > speeds[i]:
            t = (positions[i] - positions[i + 1]) / (speeds[i + 1] - speeds[i])
            meeting_position = positions[i] + speeds[i] * t
            if t > 0 and meeting_position < end_position:
                t = (end_position - positions[i]) / speeds[i]
                s_max = (end_position - positions[i + 1]) / t
                start_position = positions[i + 1]
                end_position = meeting_position
            else:
                s_max = speeds[i + 1]
                start_position = positions[i + 1]
        else:
            s_max = speeds[i + 1]
            start_position = positions[i + 1]

    t = (case.d - start_position) / s_max

    desired_speed = (start_position / t) + s_max

    return str(desired_speed)


if __name__ == "__main__":
    solve_problem()
